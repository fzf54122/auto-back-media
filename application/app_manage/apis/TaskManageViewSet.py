# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: TaskManageViewSet.py
# @Email: fzf54122@163.com
# @Description: 任务管理视图集，处理任务的CRUD操作

from fastapi import APIRouter, Depends
from fast_generic_api.generics import GenericAPIView,CustomViewSet

from commons.core.permission import DependPermisson
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_manage.models import TaskManageModel
from application.app_manage.serializers import (TaskManageSerializers,
                                                TaskManageCreateSerializers,
                                                TaskManageUpdateSerializers, )

router = APIRouter(tags=['任务管理'])

class TaskManageViewSet(CustomViewSet,
                  GenericAPIView):
    """任务管理视图集"""
    router = router
    prefix = "/task_manage"
    queryset = TaskManageModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = TaskManageSerializers           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskManageCreateSerializers
        elif self.action == 'update':
            return TaskManageUpdateSerializers
        return super().get_serializer_class()