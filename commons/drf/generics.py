from typing import Optional
from fastapi import APIRouter


class GenericViewSet:
    prefix: Optional[str] = None
    router: Optional[APIRouter] = None
    loop_uuid_field: Optional[str] = None  # 用于路径参数替代 pk
    permissions: list = []
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
