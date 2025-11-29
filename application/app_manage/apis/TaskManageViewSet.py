from fastapi import APIRouter, Depends


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson, get_current_username
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_manage.models import TaskManageModel
from application.app_manage.schemas import (TaskManageSchemas,
                                            TaskManageCreateSchemas,
                                            TaskManageUpdateSchemas,)

router = APIRouter(tags=['任务管理'])

class TaskManageViewSet(CustomViewSet,
                  GenericViewSet):
    """任务管理视图集"""
    router = router
    prefix = "/task_manage"
    model = TaskManageModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = TaskManageSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]
    
    def get_serializer_class(self):
        if self.action == 'post':
            return TaskManageCreateSchemas
        elif self.action == 'update':
            return TaskManageUpdateSchemas
        return super().get_serializer_class()