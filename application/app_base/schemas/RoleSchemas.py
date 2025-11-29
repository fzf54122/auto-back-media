from datetime import datetime
from uuid import UUID
from pydantic import Field
from commons.core.schemas import AutoSchemas

class RoleSchemas(AutoSchemas):
    uuid: UUID
    name: str
    desc: str = ""
    is_default: bool = False
    is_active: bool = True
    users: list | None = []
    menus: list | None = []
    apis: list | None = []
    created_at: datetime | None
    updated_at: datetime | None


class RoleCreateSchemas(AutoSchemas):
    name: str = Field(..., description="角色名称", json_schema_extra={'example': "管理员"})
    desc: str = Field("", description="角色描述", json_schema_extra={'example': "管理员角色"})
    is_default: bool = Field(False, description="是否为默认角色", json_schema_extra={'example': False})
    is_active: bool = Field(True, description="是否激活", json_schema_extra={'example': True})

class RoleUpdateSchemas(AutoSchemas):
    uuid: UUID = Field(..., description="角色ID", json_schema_extra={'example': 1})
    name: str = Field(..., description="角色名称", json_schema_extra={'example': "管理员"})
    desc: str = Field("", description="角色描述", json_schema_extra={'example': "管理员角色"})
    is_default: bool = Field(False, description="是否为默认角色", json_schema_extra={'example': False})
    is_active: bool = Field(True, description="是否激活", json_schema_extra={'example': True})