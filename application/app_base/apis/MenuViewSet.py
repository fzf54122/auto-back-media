# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: MenuViewSet.py
# @Email: fzf54122@163.com
# @Description: 菜单管理视图集，处理菜单的CRUD操作和树形结构构建

from fastapi import APIRouter, Request, Body
from fast_generic_api.generics import GenericAPIView,CustomViewSet
from fast_generic_api.core.response import CoreResponse

from commons.core.permission import DependPermisson

from application.app_base.models import MenuModel
from application.app_base.serializers import (MenuSerializers,
                                              MenuCreateSerializers,
                                              MenuUpdateSerializers)

router = APIRouter(tags=['菜单管理'])
class MenuViewSet(CustomViewSet,
                  GenericAPIView):
    """菜单管理视图集"""
    router = router
    prefix = "/menus"
    queryset = MenuModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = MenuSerializers           # ✅ 列表/详情默认序列化器
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return MenuCreateSerializers
        elif self.action == 'update':
            return MenuUpdateSerializers
        return super().get_serializer_class()