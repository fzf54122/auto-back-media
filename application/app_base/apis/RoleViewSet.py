from fastapi import APIRouter, Depends, Request, Body

from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import RoleModel
from application.app_base.schemas import (RoleSchemas,
                                          RoleCreateSchemas,
                                          RoleUpdateSchemas)

from application.app_base.filters import RoleFilter
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
    ordering = ["created_at"]
    loop_uuid_field = "uuid"
    serializer_class = RoleSchemas           # ✅ 列表/详情默认序列化器
    serializer_create_class = RoleCreateSchemas
    serializer_update_class = RoleUpdateSchemas
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = RoleFilter
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return self.serializer_create_class
        elif self.action == 'update':
            return self.serializer_update_class
        return self.serializer_class


    async def get(self,request: Request):
        qs = self.get_queryset()

        # 过滤查询集
        if self.filter_class:
            filter_set = self.filter_class(qs, request.query_params)
            qs = filter_set.qs()
        objs = await qs

        result = []
        for obj in objs:
            obj_dict = await obj.to_dict(m2m=True)  # m2m=True 可以序列化 ManyToManyField
            result.append(obj_dict)
        # 使用分页器
        if self.pagination_class:
            return AutoResponse(await self.pagination_class.paginate(request, result, self.get_serializer))

        return AutoResponse(result)

    async def post(self,request: Request, data=Body(...)):
        """
        创建角色
        """
        obj = await self.model.create(**self.handle_data(data))

        return AutoResponse(msg='创建成功', data={"id": obj.id})

    async def update(self,request: Request, data=Body(...)):
        """
        更新角色
        """
        self._request = request
        obj = await self.get_object()
        await obj.from_dict(self.handle_data(data))
        return AutoResponse(msg="更新成功", data={"id": obj.id})
