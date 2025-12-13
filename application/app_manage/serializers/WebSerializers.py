# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: WebSerializers.py
# @Email: fzf54122@163.com
# @Description: WebSerializers数据验证模式定义

from uuid import UUID
from typing import Optional
from fast_generic_api.core.serializers import CoreSerializers

# ==========================
# 基础模型
# ==========================
class WebSerializers(CoreSerializers):
    uuid : UUID = None
    project_type: Optional[str] = None
    project_url: Optional[str] = None
    description: Optional[str] = None


# ==========================
# 创建/更新模型
# ==========================
class WebCreateSerializers(WebSerializers):
    pass  # 可以继承 WebBase 字段

class WebUpdateSerializers(CoreSerializers):
    project_type: Optional[str] = None
    project_url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
