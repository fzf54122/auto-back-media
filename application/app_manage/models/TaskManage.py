# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: TaskManage.py
# @Email: fzf54122@163.com
# @Description: TaskManage数据模型定义

from tortoise import fields

from application.app_manage.enums import TaskManageStatus
from application.models import CoreModel,table_prefix

class TaskManageModel(CoreModel):
    project_name = fields.CharField(max_length=255,description='平台名称', null=True)
    media_type = fields.CharField(max_length=255,description='媒体类型', null=True)
    media_username = fields.CharField(max_length=255,description='媒体账号', null=True)
    task_topic = fields.CharField(max_length=255,description='任务话题', null=True)
    crontab_time = fields.DatetimeField(null=True, description="最后使用时间")
    last_time = fields.DatetimeField(null=True, description="最后使用时间")

    status = fields.IntField(choices=TaskManageStatus.choice(), default=TaskManageStatus.NOT_STARTED,
                             description="任务状态")
    class Meta:
        table = table_prefix + "media_tasks"