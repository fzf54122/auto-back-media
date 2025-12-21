# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: DeptSerializers.py
# @Email: fzf54122@163.com
# @Description: DeptSerializers数据验证模式定义

from uuid import UUID
from pydantic import Field
from typing import Optional
from fast_generic_api.core.serializers import CoreSerializers


class DeptSerializers(CoreSerializers):
    """部门管理序列化器"""
    id : int
    uuid:UUID = Field(..., description="部门ID")
    name: str = Field(..., description="部门名称", example="研发中心")
    desc: Optional[str] = Field(default="", description="备注", example="研发中心", allow_none=True)
    order: int = Field(0, description="排序")
    parent_id: int = Field(0, description="父部门ID")
    is_active:bool |None = None
    created_at:str = None
    updated_at:str = None

class DeptCreateSerializers(DeptSerializers):
    """部门管理创建序列化器"""
    pass

class DeptUpdateSerializers(DeptSerializers):
    """部门管理更新序列化器"""
    uuid: UUID