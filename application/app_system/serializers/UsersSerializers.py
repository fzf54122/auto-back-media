# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: UsersSerializers.py
# @Email: fzf54122@163.com
# @Description: UsersSerializers数据验证模式定义

import re
from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import EmailStr, Field, field_validator
from fast_generic_api.core.serializers import CoreSerializers



class UsersSerializers(CoreSerializers):
    uuid: UUID = None
    email: EmailStr | None = None
    username: str | None = None
    alias: str | None = None
    phone: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_deleted: bool | None = False
    created_at: datetime | None = None
    roles: list[int]  | None = None
    updated_at: datetime | None = None
    last_login: datetime | None = None

class UsersCreateSerializers(CoreSerializers):
        email: str = Field(..., json_schema_extra={'example': "admin@qq.com"})
        username: str = Field(
            ...,
            min_length=3,
            max_length=20,
            pattern="^[a-zA-Z0-9_]+$",
            description="用户名（3-20位字母数字下划线）",
            json_schema_extra={'example': "admin"}
        )
        password: str = Field(
            ...,
            min_length=8,
            description="密码（至少8位，包含字母和数字）",
            json_schema_extra={'example': "AdminPass123"}
        )
        alias: str | None = Field(None, description="姓名", json_schema_extra={'example': "系统管理员"})
        phone: str | None = Field(None, description="电话", json_schema_extra={'example': "13800138000"})
        is_active: bool | None = True
        is_superuser: bool | None = False
        roles: list[int] | None = None
        @field_validator("password")
        @classmethod
        def validate_password_strength(cls, v):
            """验证密码强度"""
            if len(v) < 8:
                raise ValueError("密码长度至少8位")

            if not re.search(r"[A-Za-z]", v):
                raise ValueError("密码必须包含字母")

            if not re.search(r"\d", v):
                raise ValueError("密码必须包含数字")

            # 可选：检查特殊字符
            # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            #     raise ValueError('密码建议包含特殊字符')

            return v

        @field_validator("username")
        @classmethod
        def validate_username(cls, v):
            """验证用户名格式"""
            if not re.match(r"^[a-zA-Z0-9_]+$", v):
                raise ValueError("用户名只能包含字母、数字和下划线")
            return v


class UsersUpdateSerializers(UsersSerializers):
    ...

class UsersUpdatePasswordSerializers(CoreSerializers):
    old_password: str = Field(description="旧密码")
    new_password: str = Field(
        min_length=8, description="新密码（至少8位，包含字母和数字）"
    )

    @field_validator("new_password")
    @classmethod
    def validate_new_password_strength(cls, v):
        """验证新密码强度"""
        if len(v) < 8:
            raise ValueError("新密码长度至少8位")

        if not re.search(r"[A-Za-z]", v):
            raise ValueError("新密码必须包含字母")

        if not re.search(r"\d", v):
            raise ValueError("新密码必须包含数字")

        return v
    