from fastapi import APIRouter


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson
from commons.drf import ListModelMixin,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import AuditLogModel
from application.app_base.schemas import (AuditLogSchemas,)


router = APIRouter(tags=['审计日志'])
class AuditLogViewSet(ListModelMixin,
                      GenericViewSet):
    router = router
    prefix = "/audit-log"
    model = AuditLogModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = AuditLogSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]