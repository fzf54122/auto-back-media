# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: service.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

from typing import TypeVar
from tortoise.models import Model

ModelType = TypeVar("ModelType", bound=Model)

class AutoService:
    def __init__(self, model: type[ModelType]):
        self.model = model