# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: AuditLogSerializers.py
# @Email: fzf54122@163.com
# @Description: AuditLogSerializers数据验证模式定义

from datetime import datetime
from pydantic import Field
from fast_generic_api.core.serializers import CoreSerializers


class AuditLogSerializers(CoreSerializers):
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