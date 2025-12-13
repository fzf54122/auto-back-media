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
    user_id: int | None = None
    username: str | None = None
    module: str | None = None
    summary: str | None = None
    method: str | None = None
    path: str | None = None
    status: int | None = None
    response_time: float | None = None
    ip: str | None = None
    created_at: datetime | None = None
