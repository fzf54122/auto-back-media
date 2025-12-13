# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: __init__.py
# @Email: fzf54122@163.com
# @Description: 基础功能模块API路由注册文件

__all__ = ["api_router"]

from fastapi import APIRouter
from .RoleViewSet import router as role_router
from .MenuViewSet import router as menu_router
from .DeptViewSet import router as dept_router
from .AuditLogViewSet import router as audit_log_router
from .FilesViewSet import router as files_router

api_router = APIRouter()
api_router.include_router(role_router)
api_router.include_router(menu_router)
api_router.include_router(dept_router)
api_router.include_router(audit_log_router)
api_router.include_router(files_router)