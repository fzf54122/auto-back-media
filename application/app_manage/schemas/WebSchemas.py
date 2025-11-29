#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/10/28 20:10
# @Author  : Administrator
# @File    : WebSchemas.py
# @Project : auto-back-media
# @email   : fzf54122@163.com
from uuid import UUID
from typing import Optional
from commons.core.schemas import AutoSchemas

# ==========================
# 基础模型
# ==========================
class WebSchemas(AutoSchemas):
    uuid : UUID = None
    project_type: Optional[str] = None
    project_url: Optional[str] = None
    description: Optional[str] = None


# ==========================
# 创建/更新模型
# ==========================
class WebCreateSchemas(WebSchemas):
    pass  # 可以继承 WebBase 字段

class WebUpdateSchemas(AutoSchemas):
    project_type: Optional[str] = None
    project_url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
