from fastapi import APIRouter, Depends


from commons.core.response import AutoResponse
from commons.core.permission import get_current_username
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import RoleModel
from application.app_base.schemas import (RoleSchemas,
                                          RoleCreateSchemas,
                                          RoleUpdateSchemas)
from application.app_system.services import UserService
router = APIRouter(tags=['角色管理'])
service = UserService()

class RoleViewSet(CustomViewSet,
                  GenericViewSet):
    """角色视图集"""
    router = router
    prefix = "/roles"
    model = RoleModel
    filter_fields = []
    ordering = ["created_at"]
    loop_uuid_field = "uuid"
    serializer_class = RoleSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None

    def get_serializer_class(self):
        if self.action == 'post':
            return RoleCreateSchemas
        elif self.action == 'update':
            return RoleUpdateSchemas
        return super().get_serializer_class()