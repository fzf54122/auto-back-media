# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: __init__.py
# @Email: fzf54122@163.com
# @Description: 管理模块API路由注册文件

__all__ = ["api_router"]

from fastapi import APIRouter
from .WebViewSet import router as web_router
from .MediaUserViewSet import router as media_user_router
from .TaskManageViewSet import router as task_router


api_router = APIRouter()

api_router.include_router(web_router)
api_router.include_router(media_user_router, prefix="/media_users")
api_router.include_router(task_router, prefix="/task_manage")
