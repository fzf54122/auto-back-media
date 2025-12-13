# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: LoginSerializers.py
# @Email: fzf54122@163.com
# @Description: LoginSerializers数据验证模式定义

from typing import Any
from datetime import datetime

from pydantic import Field
from fast_generic_api.core.serializers import CoreSerializers

class CredentialsSerializers(CoreSerializers):
    username: str = Field(..., description="用户名称", json_schema_extra={'example': "admin"})
    password: str = Field(..., description="密码", json_schema_extra={'example': "请输入正确的测试密码"})



class JWTOut(CoreSerializers):
    access_token: str
    refresh_token: str
    username: str
    token_type: str = "bearer"
    expires_in: int  # 过期时间（秒）
    user_uuid: Any = None


class JWTPayload(CoreSerializers):
    user_id: int
    username: str
    is_superuser: bool
    exp: datetime
    token_type: str = "access"  # access 或 refresh


class RefreshTokenRequest(CoreSerializers):
    refresh_token: str = Field(..., description="刷新令牌")


class TokenRefreshOut(CoreSerializers):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 新access_token过期时间（秒）
