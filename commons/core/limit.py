# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: limit.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

from slowapi import Limiter
from slowapi.util import get_remote_address
from conf import settings

limiter = Limiter(key_func=get_remote_address)
def apply_rate_limit(rate="5/minute"):
    """根据环境应用限流装饰器"""

    def decorator(func):
        if settings.DEBUG:
            return func  # 测试环境不应用限流
        return limiter.limit(rate)(func)
    return decorator