from datetime import datetime
from typing import List, Any
from uuid import UUID
from pydantic import Field, field_serializer
from commons.core.schemas import AutoSchemas

from application.app_base.schemas.APISchemas import APISchemas

class RoleSchemas(AutoSchemas):
    uuid: UUID | None = None
    name: str | None = None
    desc: str = ""
    is_active: bool = True
    menus: list | None = None       # 类型 list，None 默认
    apis: list | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RoleCreateSchemas(AutoSchemas):
    name: str = Field(..., description="角色名称", json_schema_extra={'example': "管理员"})
    desc: str = Field("", description="角色描述", json_schema_extra={'example': "管理员角色"})
    is_active: bool = Field(True, description="是否激活", json_schema_extra={'example': True})
    menus: list[int] = []  # 输出菜单 ID 列表
    apis: list[int] = []   # 输出 API ID 列表
    
class RoleUpdateSchemas(RoleCreateSchemas):
    pass
