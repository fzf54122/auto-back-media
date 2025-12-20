# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: MenuViewSet.py
# @Email: fzf54122@163.com
# @Description: 菜单管理视图集，处理菜单的CRUD操作和树形结构构建

from fastapi import APIRouter, Request, Body
from fast_generic_api.generics import GenericAPIView,CustomViewSet
from fast_generic_api.core.response import CoreResponse

from commons.core.permission import DependPermisson

from application.app_base.models import MenuModel
from application.app_base.serializers import (MenuSerializers,
                                              MenuCreateSerializers,
                                              MenuUpdateSerializers)

router = APIRouter(tags=['菜单管理'])
class MenuViewSet(CustomViewSet,
                  GenericAPIView):
    """菜单管理视图集"""
    router = router
    prefix = "/menus"
    queryset = MenuModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = MenuSerializers           # ✅ 列表/详情默认序列化器
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return MenuCreateSerializers
        elif self.action == 'update':
            return MenuUpdateSerializers
        return super().get_serializer_class()

    async def list(self, request: Request):
        """获取菜单列表"""
        qs = self.filter_queryset(await self.get_queryset())

        async def build_tree(items, parent_id=0):
            tree = []
            for item in items:
                if item.parent_id == parent_id:
                    item_dict = await item.to_dict()  # 转成 dict
                    # 递归生成子菜单
                    item_dict['children'] = await build_tree(items, item.id)
                    tree.append(item_dict)
            return tree

        tree = await build_tree(qs)
        data = await self.get_serializer(tree, many=True)
        return CoreResponse(data=data)
