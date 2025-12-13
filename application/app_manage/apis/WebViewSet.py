# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: WebViewSet.py
# @Email: fzf54122@163.com
# @Description: 网站管理视图集，处理网站的CRUD操作

from fastapi import APIRouter, Depends
from fast_generic_api.generics import GenericAPIView,CustomViewSet

from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_manage.models import WebModel
from application.app_manage.serializers import (WebSerializers,
                                                WebCreateSerializers,
                                                WebUpdateSerializers, )
from commons.core.permission import DependPermisson
router = APIRouter(tags=['网站管理'])

class WebViewSet(CustomViewSet,
                  GenericAPIView):
    """网站管理视图集"""
    router = router
    prefix = "/webs"
    queryset = WebModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = WebSerializers           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return WebCreateSerializers
        elif self.action == 'update':
            return WebUpdateSerializers
        return super().get_serializer_class()