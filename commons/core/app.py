# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: app.py
# @Email: fzf54122@163.com
# @Description: 应用核心功能实现

from functools import partial

from aerich import Command
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from tortoise.expressions import Q

from conf import settings
from commons.logger import logger

from .exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
    GlobalExceptionHandle
)
from .middlewares import (
    BackGroundTaskMiddleware,
    HttpAuditLogMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from .cache import cache_manager
from .limit import limiter


from application.apis import api_router
from application.app_base.models import (ApiModel, 
                                         MenuModel, 
                                         RoleModel)
from application.app_base.enums import MenuType
from application.app_base.services import ApiService
from application.app_system.services import UserService
from application.app_system.serializers import UsersCreateSerializers

api_service = ApiService()
user_service = UserService()
def make_middlewares():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS_LIST,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        Middleware(SecurityHeadersMiddleware),  # 安全头中间件
        Middleware(RequestLoggingMiddleware),  # 请求日志中间件
        Middleware(BackGroundTaskMiddleware),
        Middleware(
            HttpAuditLogMiddleware,
            methods=["GET", "POST", "PUT", "DELETE"],
            exclude_paths=[
                "/api/v1/base/access_token",
                "/docs",
                "/openapi.json",
            ],
        ),
    ]
    return middleware


def register_exceptions(app: FastAPI):
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(ResponseValidationError, ResponseValidationHandle)
    # 注册限流异常处理
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_exception_handler(Exception, GlobalExceptionHandle)

def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)


async def init_superuser():
    logger.info("🔧 开始初始化超级管理员用户...")
    user = await user_service.model.exists()

    if not user:
        await user_service.create_user(
            UsersCreateSerializers(
                username="admin",
                email="admin@admin.com",
                password="fzf991013",
                alias="系统管理员",
                phone="13800138000",
                is_active=True,
                is_superuser=True,
            )
        )
        logger.info("✅ 超级管理员用户创建成功 - 用户名: admin")
    else:
        logger.info("ℹ️ 超级管理员用户已存在，跳过创建")


async def init_menus():
    logger.info("🔧 开始初始化系统菜单...")
    menus = await MenuModel.exists()
    if not menus:
        parent_menu = await MenuModel.create(
            menu_type=MenuType.CATALOG,
            name="系统管理",
            path="/system",
            order=1,
            parent_id=0,
            icon="carbon:gui-management",
            is_hidden=False,
            component="Layout",
            keepalive=False,
            redirect="/system/user",
        )
        children_menu = [
            MenuModel(
                menu_type=MenuType.MENU,
                name="用户管理",
                path="user",
                order=1,
                parent_id=parent_menu.id,
                icon="material-symbols:person-outline-rounded",
                is_hidden=False,
                component="/system/user",
                keepalive=False,
            ),
            MenuModel(
                menu_type=MenuType.MENU,
                name="角色管理",
                path="role",
                order=2,
                parent_id=parent_menu.id,
                icon="carbon:user-role",
                is_hidden=False,
                component="/system/role",
                keepalive=False,
            ),
            MenuModel(
                menu_type=MenuType.MENU,
                name="菜单管理",
                path="menu",
                order=3,
                parent_id=parent_menu.id,
                icon="material-symbols:list-alt-outline",
                is_hidden=False,
                component="/system/menu",
                keepalive=False,
            ),
            MenuModel(
                menu_type=MenuType.MENU,
                name="API管理",
                path="api",
                order=4,
                parent_id=parent_menu.id,
                icon="ant-design:api-outlined",
                is_hidden=False,
                component="/system/api",
                keepalive=False,
            ),
            MenuModel(
                menu_type=MenuType.MENU,
                name="部门管理",
                path="dept",
                order=5,
                parent_id=parent_menu.id,
                icon="mingcute:department-line",
                is_hidden=False,
                component="/system/dept",
                keepalive=False,
            ),
            MenuModel(
                menu_type=MenuType.MENU,
                name="审计日志",
                path="auditlog",
                order=6,
                parent_id=parent_menu.id,
                icon="ph:clipboard-text-bold",
                is_hidden=False,
                component="/system/auditlog",
                keepalive=False,
            ),
        ]
        await MenuModel.bulk_create(children_menu)
        await MenuModel.create(
            menu_type=MenuType.MENU,
            name="一级菜单",
            path="/top-menu",
            order=2,
            parent_id=0,
            icon="material-symbols:featured-play-list-outline",
            is_hidden=False,
            component="/top-menu",
            keepalive=False,
            redirect="",
        )
        logger.info("✅ 系统菜单初始化成功 - 菜单数量: 8")
    else:
        logger.info("ℹ️ 系统菜单已存在，跳过初始化")


async def init_apis():
    logger.info("🔧 开始初始化API数据...")
    apis = await api_service.model.exists()
    if not apis:
        await api_service.refresh_api()
        api_count = await ApiModel.all().count()
        logger.info(f"✅ API数据初始化成功 - API数量: {api_count}")
    else:
        # 即使API已存在，也强制刷新以确保新接口被添加
        await api_service.refresh_api()
        api_count = await ApiModel.all().count()
        logger.info(f"ℹ️ API数据已刷新 - 当前API数量: {api_count}")


async def init_db():
    command = Command(tortoise_config=settings.TORTOISE_ORM, location=settings.LOCATION)
    try:
        await command.init_db(safe=True)
    except FileExistsError:
        pass

    await command.init()
    try:
        await command.migrate(no_input=True)
    except AttributeError as e:
        logger.error(f"数据库迁移失败: {e}")
        logger.warning("请手动检查数据库和migrations状态")
        # 不再自动删除migrations文件夹，避免意外丢失迁移历史
        # 如需重置migrations，请手动执行：rm -rf migrations && uv run aerich init-db
        raise RuntimeError("数据库迁移失败，请检查数据库连接和migrations状态") from e
    await command.upgrade(run_in_transaction=True)


async def init_roles():
    logger.info("🔧 开始初始化用户角色...")
    roles = await RoleModel.exists()
    if not roles:
        admin_role = await RoleModel.create(
            name="管理员",
            desc="管理员角色",
            is_default=False,
            is_active=True,
        )
        user_role = await RoleModel.create(
            name="普通用户",
            desc="普通用户角色",
            is_default=True,
            is_active=True,
        )


        # 分配所有API给管理员角色
        all_apis = await ApiModel.all()
        await admin_role.apis.add(*all_apis)
        # 分配所有菜单给管理员和普通用户
        all_menus = await MenuModel.all()
        await admin_role.menus.add(*all_menus)
        await user_role.menus.add(*all_menus)

        # 为普通用户分配基本API
        basic_apis = await ApiModel.filter(Q(method__in=["GET"]) | Q(tags="基础模块"))
        await user_role.apis.add(*basic_apis)

        logger.info("✅ 用户角色初始化成功 - 角色: 管理员, 普通用户")
    else:
        role_count = await RoleModel.all().count()
        logger.info(f"ℹ️ 用户角色已存在，跳过初始化 - 当前角色数量: {role_count}")


async def init_data():
    logger.info("#"*40)
    logger.info("🚀 系统初始化开始...")
    # 初始化Redis连接
    await cache_manager.connect()
    logger.info("🔧 开始数据库初始化和迁移...")
    await init_db()
    logger.info("✅ 数据库初始化完成")

    await init_superuser()
    await init_menus()
    await init_apis()
    await init_roles()

    logger.info("🎉 系统初始化完成！")
    logger.info("#"*40)

async def startup():
    """应用启动事件"""
    logger.info("🚀 Fast API应用启动中...")
    # 初始化数据库
    await init_data()


async def shutdown_event():
    # 断开Redis连接
    await cache_manager.disconnect()
    logger.info("🛑 Fast API应用关闭中...")
async def shutdown():
    """应用关闭事件"""
    await shutdown_event()
    

async def init_app(app: FastAPI):
    """应用启动时初始化"""
    # 注册启动和关闭事件
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
    logger.info("🎉 Fast API应用启动完成！")


async def stop_app(app: FastAPI):
    """应用关闭时清理"""
    logger.info("🔧 开始停止系统服务...")
    logger.info("👋 系统服务已关闭")


def register_startup_event(app: FastAPI):
    """注册启动和关闭事件"""
    app.add_event_handler("startup", partial(init_app, app))
    app.add_event_handler("shutdown", partial(stop_app, app))