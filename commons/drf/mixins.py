from typing import Any, Optional
from fastapi import Body, Request
from pydantic import BaseModel
from tortoise.queryset import QuerySet
from tortoise.models import Model
from tortoise.fields.relational import ManyToManyRelation
from commons.core.response import AutoResponse  # 你的统一返回封装



class ListModelMixin:
    action = "list"

    async def get(self, request: Request):
        """
        获取对象列表
        - 支持分页
        """
        qs = self.get_queryset(request)
        # 应用 ordering
        if self.ordering:
            qs = qs.order_by(*self.ordering)
        # 使用过滤器
        if self.filter_class:
            qs = self.filter_class(request, qs)
        # 使用分页器
        if self.pagination_class:
            return AutoResponse(await self.pagination_class.paginate(request, qs, self.get_serializer))
        # 不分页的情况（备用）
        serializer = self.get_serializer(qs, many=True)
        return AutoResponse(serializer)


class RetrieveModelMixin:
    action = "retrieve"

    async def retrieve(self, request: Request):
        """
        获取单个对象详情
        - 根据 UUID 或 PK 自动识别
        """
        self._request = request
        obj = await self.get_object()
        return AutoResponse(self.get_serializer(obj).data)


class CreateModelMixin:
    action = "create"

    async def post(self, request: Request, data=Body(...)):
        """
        创建对象
        - 支持传入 dict 或 Pydantic 模型
        """
        obj = await self.model.create(**self.handle_data(data))
        serializer = self.get_serializer(obj)
        return AutoResponse(serializer)


class UpdateModelMixin:
    action = "update"

    async def update(self, request: Request, data=Body(...)):
        """
        更新对象
        - 完整更新，根据 UUID 或 PK 自动识别对象
        """
        self._request = request
        obj = await self.get_object()
        await obj.update_from_dict(self.handle_data(data)).save()
        serializer = self.get_serializer(obj)
        return AutoResponse(serializer)


class PartialUpdateModelMixin:
    action = "partial_update"

    async def partial_update(self, request: Request, data=Body(...)):
        """
        部分更新对象
        - 支持部分字段更新
        """
        self._request = request
        obj = await self.get_object()
        await obj.update_from_dict(self.handle_data(data)).save()
        serializer = self.get_serializer(obj)
        return AutoResponse(serializer)


class DestroyModelMixin:
    action = "destroy"

    async def destroy(self, request: Request):
        """
        删除单个对象
        - 根据 UUID 或 PK 自动识别对象
        """
        self._request = request
        obj = await self.get_object()
        await obj.update_from_dict({"is_deleted": True}).save()
        return AutoResponse({"删除成功": f"{obj.uuid}"})
    
class DestroyManyModelMixin:
    action = "destroy_many"
    async def destroy_many(self, uuids: list[str] = Body(...)):
        """
        批量删除对象
        - 接收 UUID 列表进行批量删除
        """
        qs = self.model.filter(**{f"{self.loop_uuid_field}__in": uuids})

        objs = await qs
        if not objs:
            return AutoResponse({"message": "没有找到对应对象"}, code=404)

        # 批量更新 is_deleted = True
        await qs.update(is_deleted=True)

        deleted_uuids = [obj.uuid for obj in objs]
        return AutoResponse({"message": "批量删除成功", "deleted": deleted_uuids})
