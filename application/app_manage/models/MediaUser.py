# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: MediaUser.py
# @Email: fzf54122@163.com
# @Description: MediaUser数据模型定义

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/10/29 20:47
# @Author  : Administrator
# @File    : MediaUserModel.py
# @Project : auto-back-media
# @email   : fzf54122@163.com
from tortoise import fields

from application.app_manage.enums import MediaUserStatus
from application.models import CoreModel,table_prefix

class MediaUserModel(CoreModel):
    project_name = fields.CharField(max_length=255,description='平台名称', null=True)
    media_type = fields.CharField(max_length=255,description='媒体类型', null=True)
    media_username = fields.CharField(max_length=255,description='媒体账号', null=True)
    media_passwd = fields.CharField(max_length=255, description='媒体密码',null=True)
    last_login = fields.DatetimeField(null=True, description="最后使用时间")
    token = fields.CharField(max_length=255, description="用户Token", null=True, default=None)
    status = fields.IntField(choices=MediaUserStatus.choice(), default=MediaUserStatus.NOT_ACTIVE,
                             description="用户状态")

    class Meta:
        table = table_prefix + "media_user"

    async def save(self, *args, **kwargs):
        # 如果 token 存在且状态是未激活，自动将状态设置为激活
        if self.token:
            self.status = MediaUserStatus.ACTIVE
        return await super().save(*args, **kwargs)

