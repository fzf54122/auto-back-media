# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: AuditLogViewSet.py
# @Email: fzf54122@163.com
# @Description: 审计日志管理视图集，处理审计日志的查询和管理

from fastapi import APIRouter
from fast_generic_api.generics import ListViewSet

from commons.core.permission import DependPermisson

from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.filters import AuditLogFilter
from application.app_base.models import AuditLogModel
from application.app_base.serializers import (AuditLogSerializers, )


router = APIRouter(tags=['审计日志'])
class AuditLogViewSet(ListViewSet,):
    router = router
    prefix = "/audit-log"
    queryset = AuditLogModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = AuditLogSerializers           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = AuditLogFilter
    permissions = [DependPermisson]