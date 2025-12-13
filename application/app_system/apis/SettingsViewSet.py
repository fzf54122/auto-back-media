# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: SettingsViewSet.py
# @Email: fzf54122@163.com
# @Description: 系统设置视图集，处理系统配置的CRUD操作

from fastapi import APIRouter
from fast_generic_api.generics import GenericAPIView,CustomViewSet

from commons.core.permission import DependPermisson

from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_system.models import SettingsModel
from application.app_system.serializers import (SettingsSerializers,
                                                SettingsCreateSerializers,
                                                SettingsUpdateSerializers, )

router = APIRouter(tags=['系统设置'])


class SettingsViewSet(CustomViewSet,
                  GenericAPIView):
    """系统设置视图集"""
    router = router
    prefix = "/settings"
    queryset = SettingsModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = SettingsSerializers           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return SettingsCreateSerializers
        elif self.action == 'update':
            return SettingsUpdateSerializers
        return super().get_serializer_class()