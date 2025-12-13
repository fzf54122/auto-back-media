# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: Api.py
# @Email: fzf54122@163.com
# @Description: Api数据模型定义

from tortoise import fields

from application.models import CoreModel,table_prefix
from application.app_base.enums import MethodType

class ApiModel(CoreModel):
    """
    API模型
    """
    path = fields.CharField(max_length=100, description="API路径")
    method = fields.CharEnumField(MethodType, description="请求方法")
    summary = fields.CharField(max_length=500, description="请求简介")
    tags = fields.CharField(max_length=100, description="API标签")

    class Meta:
        table = table_prefix + "api"