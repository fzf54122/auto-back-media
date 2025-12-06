from fastapi import APIRouter


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import MenuModel
from application.app_base.schemas import (MenuSchemas,
                                          MenuSchemasCreate,
                                          MenuSchemasUpdate)

router = APIRouter(tags=['菜单管理'])
class MenuViewSet(CustomViewSet,
                  GenericViewSet):
    """菜单管理视图集"""
    router = router
    prefix = "/menus"
    model = MenuModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = MenuSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return MenuSchemasCreate
        elif self.action == 'update':
            return MenuSchemasUpdate
        return super().get_serializer_class()