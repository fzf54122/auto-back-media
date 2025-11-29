#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/10/27 21:38
# @Author  : Administrator
# @File    : api.py
# @Project : auto-back-media
# @email   : fzf54122@163.com
from fastapi.routing import APIRoute

from commons.logger import logger
from application.app_base.base import AutoService

from application.app_base.models import ApiModel
from application.app_base.schemas import (APISchemas,
                                          APICreateSchemas,
                                          APIUpdateSchemas)


class ApiService(AutoService):
    def __init__(self):
        super().__init__(model=ApiModel)

    async def refresh_api(self):
        from application import app

        routes = app.routes
        # 定义要排除的路由路径
        exclude_paths = {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico"
        }

        # 删除废弃API数据
        all_api_list = []
        for route in app.routes:
            # 同步所有APIRoute，但排除特定的路由
            if isinstance(route, APIRoute) and route.path not in exclude_paths:
                all_api_list.append((list(route.methods)[0], route.path_format))

        delete_api = []
        for api in await ApiModel.all():
            if (api.method, api.path) not in all_api_list:
                delete_api.append((api.method, api.path))

        for item in delete_api:
            method, path = item
            logger.debug(f"API Deleted {method} {path}")
            await ApiModel.filter(method=method, path=path).delete()

        for route in routes:
            if isinstance(route, APIRoute) and route.path not in exclude_paths:
                method = list(route.methods)[0]
                path = route.path_format
                summary = route.summary or "无描述"
                tags = list(route.tags)[0] if route.tags else "未分类"

                api_obj = await ApiModel.filter(method=method, path=path).first()
                if api_obj:
                    await api_obj.update_from_dict(
                        dict(
                            method=method,
                            path=path,
                            summary=summary,
                            tags=tags,
                        )
                    ).save()
                else:
                    logger.debug(f"API Created {method} {path}")
                    await ApiModel.create(
                        **dict(
                            method=method,
                            path=path,
                            summary=summary,
                            tags=tags,
                        )
                    )