# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: TaskManageSerializers.py
# @Email: fzf54122@163.com
# @Description: TaskManageSerializers数据验证模式定义

from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import Field
from fast_generic_api.core.serializers import CoreSerializers

# 基础的 Task 管理类，包含所有通用字段
class TaskManageSerializers(CoreSerializers):
    uuid: UUID = None    # 由数据库自动生成，不需要传入
    project_name: Optional[str] = None
    media_type: Optional[str] = None
    media_username: Optional[str] = None
    task_topic: Optional[str] = None
    crontab_time: Optional[datetime] = None  # 使用 datetime 类型
    last_time: Optional[datetime] = None     # 使用 datetime 类型
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # class Config:
    #     orm_mode = True  # 使Pydantic与ORM模型兼容，允许通过数据库模型填充数据

# 创建任务时的 Pydantic 模型
class TaskManageCreateSerializers(CoreSerializers):
    project_name: str = Field(..., description="平台名称")
    media_type: str = Field(..., description="媒体类型")
    media_username: str = Field(..., description="媒体账号")
    task_topic: str = Field(..., description="任务话题")
    crontab_time: Optional[datetime] = Field(None, description="任务时间")
    last_time: Optional[datetime] = Field(None, description="上次任务更新时间")

# 更新任务时的 Pydantic 模型
class TaskManageUpdateSerializers(CoreSerializers):
    project_name: Optional[str] = Field(None, description="平台名称")
    media_type: Optional[str] = Field(None, description="媒体类型")
    media_username: Optional[str] = Field(None, description="媒体账号")
    task_topic: Optional[str] = Field(None, description="任务话题")
    crontab_time: Optional[datetime] = Field(None, description="任务时间")
    last_time: Optional[datetime] = Field(None, description="上次任务更新时间")
