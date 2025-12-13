# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: RoleSerializers.py
# @Email: fzf54122@163.com
# @Description: RoleSerializers数据验证模式定义

from datetime import datetime
from typing import List, Any, Optional
from uuid import UUID
from pydantic import Field
from fast_generic_api.core.serializers import CoreSerializers

class RoleSerializers(CoreSerializers):
    uuid: UUID | None = None
    name: str | None = None
    desc: Optional[str] = Field(default="", allow_none=True)
    is_active: bool = True
    menus: list | None = None       # 类型 list，None 默认
    apis: list | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RoleCreateSerializers(CoreSerializers):
    name: str = Field(..., description="角色名称", json_schema_extra={'example': "管理员"})
    desc: str = Field("", description="角色描述", json_schema_extra={'example': "管理员角色"})
    is_active: bool = Field(True, description="是否激活", json_schema_extra={'example': True})
    menus: list[int] = []  # 输出菜单 ID 列表
    apis: list[int] = []   # 输出 API ID 列表
    
class RoleUpdateSerializers(RoleCreateSerializers):
    pass