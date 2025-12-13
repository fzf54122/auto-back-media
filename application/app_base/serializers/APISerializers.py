# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: APISerializers.py
# @Email: fzf54122@163.com
# @Description: APISerializers数据验证模式定义

from pydantic import Field
from fast_generic_api.core.serializers import CoreSerializers

from ..enums import MethodType

class APISerializers(CoreSerializers):
    path: str = Field(..., description="API路径", json_schema_extra={'example': "/api/v1/user/list"})
    summary: str = Field("", description="API简介", json_schema_extra={'example': "查看用户列表"})
    method: MethodType = Field(..., description="API方法", json_schema_extra={'example': "GET"})
    tags: str = Field(..., description="API标签", json_schema_extra={'example': "User"})


class APICreateSerializers(APISerializers): ...


class APIUpdateSerializers(APISerializers):
    id: int
