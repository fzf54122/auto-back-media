# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: Role.py
# @Email: fzf54122@163.com
# @Description: Role数据模型定义

from tortoise import fields

from application.models import CoreModel,table_prefix

class RoleModel(CoreModel):
    """
    权限模型
    """
    name = fields.CharField(max_length=20, null=True, description="角色名称")

    desc = fields.CharField(max_length=500, null=True, description="角色描述")
    menus = fields.ManyToManyField("models.MenuModel", related_name="role_menus")
    apis = fields.ManyToManyField("models.ApiModel", related_name="role_apis")

    class Meta:
        table = table_prefix + "role"