# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: SettingsSerializers.py
# @Email: fzf54122@163.com
# @Description: SettingsSerializers数据验证模式定义

from uuid import UUID
from datetime import datetime
from typing import Any, Optional
from pydantic import Field

from fast_generic_api.core.serializers import CoreSerializers
class SettingsSerializers(CoreSerializers):
    uuid: UUID = None
    key: str = 0
    value: Optional[Any] = None
    description: Optional[str] = None
    is_public: bool = False
    category: str = "general"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SettingsCreateSerializers(CoreSerializers):
    uid: UUID = None
    key: str = Field(..., description="设置键", json_schema_extra={'example': "site_name"})
    value: Any = Field(..., description="设置值", json_schema_extra={'example': "我的网站"})
    description: Optional[str] = Field(None, description="设置描述", json_schema_extra={'example': "网站名称"})
    is_public: bool = Field(False, description="是否公开设置", json_schema_extra={'example': False})
    category: str = Field("general", description="设置分类", json_schema_extra={'example': "site"})


class SettingsUpdateSerializers(CoreSerializers):
    value: Any = Field(..., description="设置值")
    description: Optional[str] = Field(None, description="设置描述")
    is_public: Optional[bool] = Field(None, description="是否公开设置")
    category: Optional[str] = Field(None, description="设置分类")

