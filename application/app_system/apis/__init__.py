# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: __init__.py
# @Email: fzf54122@163.com
# @Description: 系统管理模块API路由注册文件

__all__ = ["api_router"]

from fastapi import APIRouter
from .LoginViewSet import router as login_router
from .UserViewSet import router as user_router
from .SettingsViewSet import router as settings_router


api_router = APIRouter()
api_router.include_router(login_router)
api_router.include_router(user_router)
api_router.include_router(settings_router)