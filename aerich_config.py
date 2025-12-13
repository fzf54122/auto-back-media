# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: aerich_config.py
# @Email: fzf54122@163.com
# @Description: 数据库迁移配置文件
import os
import sys

from conf import settings

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "application"))

TORTOISE_ORM = settings.TORTOISE_ORM