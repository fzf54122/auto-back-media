from tortoise import fields

from application.models import CoreModel,table_prefix
from application.app_base.enums import MenuType

class MenuModel(CoreModel):
    """
    菜单模型
    """
    name = fields.CharField(max_length=20, description="菜单名称")
    remark = fields.JSONField(null=True, description="保留字段")
    menu_type = fields.CharEnumField(MenuType, null=True, description="菜单类型")
    icon = fields.CharField(max_length=100, null=True, description="菜单图标")
    path = fields.CharField(max_length=100, description="菜单路径")
    order = fields.IntField(default=0, description="排序")
    parent_id = fields.IntField(default=0, description="父菜单ID")
    is_hidden = fields.BooleanField(default=False, description="是否隐藏")
    component = fields.CharField(max_length=100, description="组件")
    keepalive = fields.BooleanField(default=True, description="存活")
    redirect = fields.CharField(max_length=100, null=True, description="重定向")

    class Meta:
        table = table_prefix + "menu"