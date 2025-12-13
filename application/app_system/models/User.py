# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: User.py
# @Email: fzf54122@163.com
# @Description: User数据模型定义

from tortoise import fields

from application.models import CoreModel,table_prefix

class UserModel(CoreModel):
    """用户表"""
    username = fields.CharField(max_length=20, unique=True, description="用户名称")
    alias = fields.CharField(max_length=30, null=True, description="姓名")
    email = fields.CharField(max_length=255, unique=True, description="邮箱")
    phone = fields.CharField(max_length=20, null=True, description="电话")
    password = fields.CharField(max_length=128, null=True, description="密码")
    is_active = fields.BooleanField(default=True, description="是否激活")
    is_deleted = fields.BooleanField(default=False, description="软删除标记")
    is_superuser = fields.BooleanField(default=False, description="是否为超级管理员")
    roles = fields.ManyToManyField("models.RoleModel", related_name="user_roles")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")

    class Meta:
        table = table_prefix + "user"