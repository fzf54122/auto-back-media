# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: RoleViewSet.py
# @Email: fzf54122@163.com
# @Description: 角色管理视图集，处理角色的CRUD操作和权限管理

from fastapi import APIRouter, Depends, Request, Body
from fast_generic_api.generics import GenericAPIView,CustomViewSet
from fast_generic_api.core.response import CoreResponse

from commons.core.permission import DependPermisson
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import RoleModel
from application.app_base.serializers import (RoleSerializers,
                                              RoleCreateSerializers,
                                              RoleUpdateSerializers)

from application.app_base.filters import RoleFilter
from application.app_base.services import RoleService

router = APIRouter(tags=['角色管理'])
service = RoleService()
class RoleViewSet(CustomViewSet,
                  GenericAPIView):
    """角色视图集"""
    router = router
    prefix = "/roles"
    queryset = RoleModel
    filter_fields = []
    ordering = ["created_at"]
    loop_uuid_field = "uuid"
    serializer_class = RoleSerializers           # ✅ 列表/详情默认序列化器
    serializer_create_class = RoleCreateSerializers
    serializer_update_class = RoleUpdateSerializers
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = RoleFilter
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_create_class
        elif self.action == 'update':
            return self.serializer_update_class
        return super().get_serializer_class()


    async def list(self, request: Request):
        qs = self.queryset.filter(is_deleted=False)

        # 应用排序
        if self.ordering:
            qs = qs.order_by(*self.ordering)
        
        # 过滤查询集
        if self.filter_class:
            filter_set = self.filter_class(qs, request.query_params)
            qs = filter_set.qs
        
        objs = await qs

        result = []
        for obj in objs:
            obj_dict = await obj.to_dict(m2m=True)  # m2m=True 可以序列化 ManyToManyField
            result.append(obj_dict)
            
        # 使用分页器
        if self.pagination_class:
            return CoreResponse(await self.pagination_class.paginate(request, result, self.get_serializer))

        return CoreResponse(result)
    
    async def retrieve(self, request: Request):
        """
        获取角色详情
        """
        self.request = request
        obj = await self.get_object()
        serializer = self.get_serializer(obj)
        return CoreResponse(serializer)

    async def create(self, request: Request, data=Body(...)):
        """
        创建角色
        """
        obj = await self.queryset.create(**self.serialize_input_data(data))

        return CoreResponse(msg='创建成功', data={"id": obj.id})

    async def update(self, request: Request, data=Body(...)):
        """
        更新角色
        """
        self.request = request
        obj = await self.get_object()
        await obj.update_from_dict(self.serialize_input_data(data)).save()
        return CoreResponse(msg="更新成功", data={"id": obj.id})
    
    async def destroy(self, request: Request):
        """
        逻辑删除角色
        """
        self.request = request
        obj = await self.get_object()
        await obj.update(is_deleted=True)
        return CoreResponse(msg="删除成功")