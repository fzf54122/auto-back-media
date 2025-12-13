# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: Settings.py
# @Email: fzf54122@163.com
# @Description: Settings数据模型定义

from tortoise import fields

from application.models import CoreModel,table_prefix


class SettingsModel(CoreModel):
    """系统设置表"""
    key = fields.CharField(max_length=100, unique=True, description="设置键")
    value = fields.CharField(max_length=100, unique=True, description="设置值")
    description = fields.CharField(max_length=500, null=True, description="设置描述")
    is_public = fields.BooleanField(default=True, description="是否公开设置")
    category = fields.CharField(max_length=50, default="general", description="设置分类")

    class Meta:
        table = table_prefix + "settings"