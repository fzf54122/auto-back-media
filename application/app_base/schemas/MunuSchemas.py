from uuid import UUID
from pydantic import Field
from application.app_base.enums import MenuType
from commons.core.schemas import AutoSchemas



class MenuSchemas(AutoSchemas):
    uuid: UUID
    name: str
    path: str
    remark: dict | None
    menu_type: MenuType | None
    icon: str | None
    order: int
    parent_id: int
    is_hidden: bool
    component: str
    keepalive: bool
    redirect: str | None
    children: list["MenuSchemas"] | None

class MenuSchemasCreate(MenuSchemas):
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


class MenuSchemasUpdate(MenuSchemas):
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