from enum import Enum, StrEnum


class MethodType(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class MenuType(StrEnum):
    CATALOG = "catalog"  # 目录
    MENU = "menu"  # 菜单