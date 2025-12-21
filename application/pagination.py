# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: pagination.py
# @Email: fzf54122@163.com
# @Description: 分页功能实现

from fast_generic_api.core.pagination import CorePagination


class LimitOffsetFreePagination(CorePagination):
    max_limit = None


class LimitOffsetMax2000Pagination(CorePagination):
    max_limit = 2000


class LimitOffsetMaxDefaultPagination(CorePagination):
    max_limit = 20

class LimitOffsetMax1tPagination(CorePagination):
    max_limit = 1