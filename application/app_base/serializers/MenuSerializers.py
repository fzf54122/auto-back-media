# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: MenuSerializers.py
# @Email: fzf54122@163.com
# @Description: MunuSerializers数据验证模式定义

from uuid import UUID
from pydantic import Field
from application.app_base.enums import MenuType
from fast_generic_api.core.serializers import CoreSerializers



class MenuSerializers(CoreSerializers):
    # id: int = None
    uuid: UUID = None
    name: str = None
    path: str = "/menu"
    ordering: list[str] = None
    remark: dict | None = None
    menu_type: MenuType | None = None
    icon: str | None = None
    order: int = 0
    parent_id: int = 0
    is_hidden: bool = False
    component: str = None
    keepalive: bool = False
    redirect: str | None = None
    children: list["MenuSerializers"] | None = None

class MenuCreateSerializers(MenuSerializers):
    menu_type: MenuType = Field(default=MenuType.CATALOG.value)
    name: str = Field(example="用户管理")
    icon: str | None = "ph:user-list-bold"
    path: str = Field(example="/system/user")
    order: int | None = Field(example=1)
    parent_id: int | None = Field(example=0, default=0)
    is_hidden: bool | None = False
    component: str = Field(default="Layout", example="/system/user")
    keepalive: bool | None = True
    redirect: str | None = ""


class MenuUpdateSerializers(MenuSerializers):
    uuid: int
    menu_type: MenuType | None = Field(example=MenuType.CATALOG.value)
    name: str | None = Field(example="用户管理")
    icon: str | None = "ph:user-list-bold"
    path: str | None = Field(example="/system/user")
    order: int | None = Field(example=1)
    parent_id: int | None = Field(example=0)
    is_hidden: bool | None = False
    component: str = Field(example="/system/user")
    keepalive: bool | None = False
    redirect: str | None = ""