from fastapi import APIRouter

from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_manage.models import WebModel
from application.app_manage.schemas import (WebSchemas,
                                            WebCreateSchemas,
                                            WebUpdateSchemas,)
from commons.core.permission import DependPermisson
router = APIRouter(tags=['网站管理'])

class WebViewSet(CustomViewSet,
                  GenericViewSet):
    """网站管理视图集"""
    router = router
    prefix = "/web"
    model = WebModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = WebSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return WebCreateSchemas
        elif self.action == 'update':
            return WebUpdateSchemas
        return super().get_serializer_class()