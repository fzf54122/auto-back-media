from uuid import UUID
from datetime import datetime
from pydantic import Field
from commons.core.schemas import AutoSchemas


class AuditLogSchemas(AutoSchemas):
    user_id: int | None = Field(description="用户ID")
    username: str | None = Field(description="用户名")
    module: str | None = Field(description="功能模块")
    summary: str | None = Field(description="操作描述")
    method: str = Field(description="请求方法")
    path: str = Field(description="请求路径")
    status: int = Field(description="响应状态码")
    response_time: float = Field(description="响应时间（毫秒）")
    ip: str | None = Field(description="IP地址")
    created_at: datetime | None = Field(description="创建时间")