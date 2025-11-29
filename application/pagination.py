from commons.core.pagination import LimitOffsetPagination

class LimitOffsetFreePagination(LimitOffsetPagination):
    max_limit = None


class LimitOffsetMax2000Pagination(LimitOffsetPagination):
    max_limit = 2000


class LimitOffsetMaxDefaultPagination(LimitOffsetPagination):
    max_limit = 10

class LimitOffsetMax1tPagination(LimitOffsetPagination):
    max_limit = 1