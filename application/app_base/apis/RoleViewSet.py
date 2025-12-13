# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: RoleViewSet.py
# @Email: fzf54122@163.com
# @Description: 角色管理视图集，处理角色的CRUD操作和权限管理

import os
from fastapi import APIRouter, Depends, Request, Body
from fast_generic_api.generics import GenericAPIView,CustomViewSet
from fast_generic_api.core.response import CoreResponse

from commons.core.permission import DependPermisson
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import RoleModel
from application.app_base.serializers import (RoleSerializers,
                                              RoleCreateSerializers,
                                              RoleUpdateSerializers)

from application.app_base.filters import RoleFilter
from application.app_base.services import RoleService

router = APIRouter(tags=['角色管理'])
service = RoleService()
class RoleViewSet(CustomViewSet,
                  GenericAPIView):
    """角色视图集"""
    router = router
    prefix = "/roles"
    queryset = RoleModel
    filter_fields = []
    ordering = ["created_at"]
    loop_uuid_field = "uuid"
    serializer_class = RoleSerializers           # ✅ 列表/详情默认序列化器
    serializer_create_class = RoleCreateSerializers
    serializer_update_class = RoleUpdateSerializers
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = RoleFilter
    permissions = [] if os.getenv('DISABLE_AUTH') == 'true' else [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_create_class
        elif self.action == 'update':
            return self.serializer_update_class
        return super().get_serializer_class()