# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: apis.py
# @Email: fzf54122@163.com
# @Description: 全局API路由注册文件，整合所有应用模块的路由

__all__ = ["api_router"]

from fastapi import APIRouter

from application.app_base.apis import api_router as base_router
from application.app_system.apis import api_router as system_router
from application.app_manage.apis import api_router as manager_router

api_router = APIRouter()

api_router.include_router(system_router)
api_router.include_router(base_router)
api_router.include_router(manager_router)