# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: filters.py
# @Email: fzf54122@163.com
# @Description: 数据过滤类定义

from tortoise.queryset import QuerySet
from typing import Dict, Any, Callable

from fast_generic_api.core.filter import CoreFilterSet

from application.app_base.models import RoleModel


class RoleFilter(CoreFilterSet):
    model = RoleModel

    filters = {
        "name": lambda qs, field, value: qs.filter(**{f"{field}__contains": value}),
        "desc": lambda qs, field, value: qs.filter(**{f"{field}__contains": value}),
        "is_active": lambda qs, field, value: qs.filter(**{f"{field}__contains": value}),
    }

    def __init__(self, queryset: QuerySet = None, data: Dict[str, Any] = None):
        queryset = queryset or RoleModel.filter(is_deleted=False)
        super().__init__(queryset, data)
