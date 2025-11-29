from typing import Any, Optional
from fastapi import Body, Request
from pydantic import BaseModel
from tortoise.queryset import QuerySet
from tortoise.models import Model
from tortoise.fields.relational import ManyToManyRelation
from commons.core.response import AutoResponse  # 你的统一返回封装


class DataMixin:
    
    def handle_data(self,obj) -> dict:
        if not isinstance(obj, dict):
            obj_dict = obj.model_dump(exclude_unset=True)
        else:
            obj_dict = obj
        return obj_dict


class CRUDMixinBase(DataMixin):
    model: type[Model]
    loop_uuid_field: Optional[str] = None
    action: Optional[str] = None

    pagination_class = None            # 分页器
    filter_class = None                # 过滤器
    serializer_class: type[BaseModel]  # 序列化器
    _request = None

    def get_serializer_class(self):
        """根据 action 返回对应 Pydantic 类"""
        return getattr(self, "serializer_class")

    def get_serializer(self, instance: Any, many: bool = False):
        """把 ORM 对象转换为 Pydantic 实例"""
        cls = self.get_serializer_class()
        if many:
            return [cls.model_validate(obj) for obj in instance]
        return cls.model_validate(instance)
    
    def get_queryset(self, request: Request) -> QuerySet:
        """
        返回基础 QuerySet，可被 filter_queryset 进一步过滤
        """
        if not self.model:
            raise ValueError("model must be defined")
        # 基础 QuerySet
        return self.model.all()

    def filter_queryset(self, request: Request, qs):
        return qs


    async def get_object(self ):
        obj_id = self._request.path_params.get(self.loop_uuid_field or "pk")
        obj = await self.model.get(**{self.loop_uuid_field or "id": obj_id })

        if not obj:
            raise Exception(f"{self.model.__name__} object not found")
        return obj

    def get_pagination(self, request: Request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        return page, page_size

class ListModelMixin(CRUDMixinBase):
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


class RetrieveModelMixin(CRUDMixinBase):
    action = "retrieve"

    async def retrieve(self, request: Request):
        """
        获取单个对象详情
        - 根据 UUID 或 PK 自动识别
        """
        self._request = request
        obj = await self.get_object()
        return AutoResponse(self.get_serializer(obj).data)


class CreateModelMixin(CRUDMixinBase):
    action = "create"

    async def post(self, request: Request, data=Body(...)):
        """
        创建对象
        - 支持传入 dict 或 Pydantic 模型
        """
        obj = await self.model.create(**self.handle_data(data))
        serializer = self.get_serializer(obj)
        return AutoResponse(serializer)


class UpdateModelMixin(CRUDMixinBase):
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


class PartialUpdateModelMixin(CRUDMixinBase):
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


class DestroyModelMixin(CRUDMixinBase):
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
    
class DestroyManyModelMixin(CRUDMixinBase):
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
