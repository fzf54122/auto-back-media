# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: __init__.py
# @Email: fzf54122@163.com
# @Description: 模型导入文件

__all__ = [
    "MediaUserModel",
    'TaskManageModel',
    'WebModel',
]

from .MediaUser import MediaUserModel
from .TaskManage import TaskManageModel
from .Web import WebModel