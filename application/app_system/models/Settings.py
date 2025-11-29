#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/10/26 21:36
# @Author  : Administrator
# @File    : SettingsModel.py
# @Project : auto-back-media
# @email   : fzf54122@163.com
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