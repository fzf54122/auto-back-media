# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: AuditLog.py
# @Email: fzf54122@163.com
# @Description: AuditLog数据模型定义

from tortoise import fields

from application.models import CoreModel,table_prefix

class AuditLogModel(CoreModel):
    user_id = fields.IntField(null=True, description="用户ID")
    username = fields.CharField(max_length=64, null=True, description="用户名称")
    module = fields.CharField(max_length=64, null=True, description="功能模块")
    summary = fields.CharField(max_length=128, null=True, description="请求描述")
    method = fields.CharField(max_length=10, null=True, description="请求方法")
    path = fields.CharField(max_length=255, null=True, description="请求路径")
    status = fields.IntField(null=True, description="状态码")
    response_time = fields.IntField(null=True, description="响应时间(单位ms)")
    request_args = fields.JSONField(null=True, description="请求参数")
    response_body = fields.JSONField(null=True, description="返回数据")

    class Meta:
        table = table_prefix + "audit_log"
