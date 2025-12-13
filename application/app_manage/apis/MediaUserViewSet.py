# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: MediaUserViewSet.py
# @Email: fzf54122@163.com
# @Description: 媒体用户管理视图集，处理媒体用户的CRUD操作

from fastapi import APIRouter, Depends
from fast_generic_api.generics import GenericAPIView,CustomViewSet

from commons.core.permission import DependPermisson
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_manage.models import MediaUserModel
from application.app_manage.serializers import (MediaUserSerializers,
                                                MediaUserCreateSerializers,
                                                MediaUserUpdateSerializers, )

router = APIRouter(tags=['媒体账号管理'])

class MediaUserViewSet(CustomViewSet,
                  GenericAPIView):
    """媒体账号管理视图集"""
    router = router
    prefix = "/media_users"
    queryset = MediaUserModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = MediaUserSerializers           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return MediaUserCreateSerializers
        elif self.action == 'update':
            return MediaUserUpdateSerializers
        return super().get_serializer_class()