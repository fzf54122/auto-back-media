# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: Web.py
# @Email: fzf54122@163.com
# @Description: Web数据模型定义

from tortoise import fields

from application.models import CoreModel,table_prefix


class WebModel(CoreModel):
    """网站记录表"""
    project_type = fields.CharField(max_length=50, description="平台类型", db_index=True)
    project_url = fields.CharField(max_length=100, null=True, description="平台URL")
    description = fields.TextField(null=True, description="项目描述")
    is_active = fields.BooleanField(default=True, description="是否激活")
    is_deleted = fields.BooleanField(default=False, description="软删除标记")
    class Meta:
        table = table_prefix + "webs"