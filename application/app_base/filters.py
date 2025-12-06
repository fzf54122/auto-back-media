from tortoise.queryset import QuerySet
from typing import Dict, Any, Callable

from commons.core.filter import TortoiseFilterSet

from application.app_base.models import RoleModel


class RoleFilter(TortoiseFilterSet):
    model = RoleModel

    filters = {
        "name": lambda qs, field, value: qs.filter(**{f"{field}__contains": value}),
        "desc": lambda qs, field, value: qs.filter(**{f"{field}__contains": value}),
        "is_active": lambda qs, field, value: qs.filter(**{f"{field}__contains": value}),
    }

    def __init__(self, queryset: QuerySet = None, data: Dict[str, Any] = None):
        queryset = queryset or RoleModel.filter(is_deleted=False)
        super().__init__(queryset, data)
