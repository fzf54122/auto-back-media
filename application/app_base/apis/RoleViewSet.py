from fastapi import APIRouter, Depends, Request


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson, get_current_username
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import RoleModel
from application.app_base.schemas import (RoleSchemas,
                                          RoleCreateSchemas,
                                          RoleUpdateSchemas)
from application.app_base.services import RoleService

router = APIRouter(tags=['角色管理'])
service = RoleService()
class RoleViewSet(CustomViewSet,
                  GenericViewSet):
    """角色视图集"""
    router = router
    prefix = "/roles"
    model = RoleModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = RoleSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return RoleCreateSchemas
        elif self.action == 'update':
            return RoleUpdateSchemas
        return super().get_serializer_class()
    
    async def get(self,request: Request):
        qs = self.model.all()
        # 应用 ordering
        if self.ordering:
            qs = qs.order_by(*self.ordering)
        # 使用过滤器
        if self.filter_class:
            qs = self.filter_class(request, qs)
        qs = await service.handle_get_list(qs=qs)
        # 使用分页器
        if self.pagination_class:
            
            return AutoResponse(await self.pagination_class.paginate(request, qs, self.get_serializer))
        
        return AutoResponse(qs)