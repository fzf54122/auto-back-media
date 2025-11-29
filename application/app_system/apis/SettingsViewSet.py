from fastapi import APIRouter, Depends


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson, get_current_username
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_system.models import SettingsModel
from application.app_system.schemas import (SettingsSchemas,
                                            SettingsCreateSchemas,
                                            SettingsUpdateSchemas,)

router = APIRouter(tags=['系统设置'])


class SettingsViewSet(CustomViewSet,
                  GenericViewSet):
    """系统设置视图集"""
    router = router
    prefix = "/settings"
    model = SettingsModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = SettingsSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return SettingsCreateSchemas
        elif self.action == 'update':
            return SettingsUpdateSchemas
        return super().get_serializer_class()