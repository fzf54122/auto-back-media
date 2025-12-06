from typing import Optional,Any

from fastapi import APIRouter,Request
from tortoise.expressions import Q
from tortoise.queryset import QuerySet
from tortoise.models import Model
from pydantic import BaseModel




class GenericViewSet:
    prefix: Optional[str] = None
    router: Optional[APIRouter] = None
    loop_uuid_field: Optional[str] = None  # 用于路径参数替代 pk
    permissions: list = []

    model: type[Model]
    action: Optional[str] = None

    pagination_class = None            # 分页器
    filter_class = None                # 过滤器
    serializer_class: type[BaseModel]  # 序列化器
    _request = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not cls.router or not cls.prefix:
            return

        instance = cls()

        # 映射方法到 HTTP 方法
        method_map = {
            "destroy_many": "DELETE",
            "get": "GET",
            "retrieve": "GET",
            "post": "POST",
            "update": "PUT",
            "partial_update": "PATCH",
            "destroy": "DELETE",
        }

        for method_name, http_method in method_map.items():
            if not hasattr(instance, method_name):
                continue

            endpoint = getattr(instance, method_name)

            # 读取装饰器注入的元信息
            summary = getattr(endpoint, "_summary", None)
            description = getattr(endpoint, "_description", None)
            tags = getattr(endpoint, "_tags", None)
            responses = getattr(endpoint, "_responses", None)

            # 构造路径
            path = cls.prefix
            if method_name in ["list", "create"]:
                path += f"/{method_name}/"
            elif method_name == "destroy_many":
                path += f"/destroy/many/"
            elif method_name in ["retrieve", "update", "partial_update", "destroy"]:
                param_name = cls.loop_uuid_field or "pk"
                path += f"/{{{param_name}}}/"

            # 注册路由（补充元参数）
            cls.router.add_api_route(
                path,
                endpoint,
                methods=[http_method],
                name=method_name,
                summary=summary,
                description=description,
                tags=tags,
                responses=responses,
                dependencies=cls.permissions,
            )


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
        
        return self.model.all(Q(is_deleted=False))

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

    def handle_data(self,obj) -> dict:
        if not isinstance(obj, dict):
            obj_dict = obj.model_dump(exclude_unset=True)
        else:
            obj_dict = obj
        return obj_dict
