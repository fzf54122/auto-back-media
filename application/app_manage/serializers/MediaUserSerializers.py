# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: MediaUserSerializers.py
# @Email: fzf54122@163.com
# @Description: MediaUserSerializers数据验证模式定义

from uuid import UUID


from datetime import datetime
from typing import Any, Optional
from pydantic import Field

from fast_generic_api.core.serializers import CoreSerializers

class MediaUserSerializers(CoreSerializers):
    uuid: UUID
    project_name: str | None = None
    media_type: str | None = None
    media_username: str | None = None
    media_passwd: str | None = None
    last_login: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MediaUserCreateSerializers(CoreSerializers):
    project_name: str = Field(..., description="平台名称", json_schema_extra={'example': "抖音"})
    media_type: str = Field(..., description="媒体类型", json_schema_extra={'example': "短视频"})
    media_username: str = Field(..., description="媒体账号", json_schema_extra={'example': "user123"})
    media_passwd: str = Field(..., description="媒体密码", json_schema_extra={'example': "password123"})

class MediaUserUpdateSerializers(CoreSerializers):
    project_name: Optional[str] = Field(None, description="平台名称", json_schema_extra={'example': "抖音"})
    media_type: Optional[str] = Field(None, description="媒体类型", json_schema_extra={'example': "短视频"})
    media_username: Optional[str] = Field(None, description="媒体账号", json_schema_extra={'example': "user123"})
    media_passwd: Optional[str] = Field(None, description="媒体密码", json_schema_extra={'example': "password123"})
    last_login: Optional[datetime] = Field(None, description="最后使用时间")