from typing import Any
from datetime import datetime

from pydantic import Field
from commons.core.schemas import AutoSchemas

class CredentialsSchema(AutoSchemas):
    username: str = Field(..., description="用户名称", json_schema_extra={'example': "admin"})
    password: str = Field(..., description="密码", json_schema_extra={'example': "请输入正确的测试密码"})



class JWTOut(AutoSchemas):
    access_token: str
    refresh_token: str
    username: str
    token_type: str = "bearer"
    expires_in: int  # 过期时间（秒）
    user_uuid: Any = None


class JWTPayload(AutoSchemas):
    user_id: int
    username: str
    is_superuser: bool
    exp: datetime
    token_type: str = "access"  # access 或 refresh


class RefreshTokenRequest(AutoSchemas):
    refresh_token: str = Field(..., description="刷新令牌")


class TokenRefreshOut(AutoSchemas):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 新access_token过期时间（秒）
