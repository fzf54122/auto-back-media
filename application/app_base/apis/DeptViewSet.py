# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: DeptViewSet.py
# @Email: fzf54122@163.com
# @Description: 部门管理视图集，处理部门的CRUD操作和部门关系管理

from fastapi import APIRouter
from fast_generic_api.generics import GenericAPIView,CustomViewSet
from fast_generic_api.core.response import CoreResponse

from commons.core.permission import DependPermisson

from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import DeptsModel,DeptClosure
from application.app_base.serializers import (DeptSerializers,
                                              DeptCreateSerializers,
                                              DeptUpdateSerializers)
from application.app_base.services import DeptsService

service = DeptsService()

router = APIRouter(tags=['部门管理'])
class DeptViewSet(CustomViewSet,
                  GenericAPIView):
    """部门管理视图集"""
    router = router
    prefix = "/depts"
    queryset = DeptsModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = DeptSerializers           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return DeptCreateSerializers
        elif self.action == 'update':
            return DeptUpdateSerializers
        return super().get_serializer_class()
    

    async def create(self, data):
        """创建部门并更新部门关系"""
        if data.parent_id != 0:
            # 验证父部门是否存在
            parent_dept = await self.queryset.get_or_none(id=data.parent_id)
            if not parent_dept:
                return CoreResponse(code=400, status="error", msg="父部门不存在")
        
        new_instance = await self.queryset.create(**data.model_dump())
        # 创建部门关系
        await service.update_dept_closure(new_instance)
        return CoreResponse(data=new_instance)

    async def update(self, uuid, data):
        # 获取实例
        instance = await self.queryset.get_or_none(uuid=uuid)
        if not instance:
            return CoreResponse(code=400, status="error", msg="部门不存在")
        # 更新普通字段
        update_data = data.model_dump(exclude_unset=True)
        await instance.update_from_dict(update_data)
        # 更新部门关系
        await service.update_dept_closure(instance)
        # 返回更新后的数据
        result = await instance.to_dict()  # 使用你 CoreModel 的 to_dict
        return CoreResponse(data=result)
    

    async def destroy(self, request):
        """逻辑删除部门"""
        instance = await self.queryset.get_or_none(uuid=request.path_params["uuid"])
        if not instance:
            return CoreResponse(code=400, status="error", msg="部门不存在")
        await instance.delete()
        await DeptClosure.filter(descendant=instance.id).update(is_deleted=True)
        return CoreResponse("部门删除成功")