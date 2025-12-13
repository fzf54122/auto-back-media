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

    def _build_menu_tree(self, menus):
        """
        将平面菜单列表转换为树形结构
        """
        menu_dict = {}
        root_menus = []

        # 先将所有菜单放入字典中，使用 id 作为键
        for menu in menus:
            menu["children"] = []
            menu_dict[menu["id"]] = menu

        # 构建树形结构
        for menu in menus:
            parent_id = menu["parent_id"]
            if parent_id == 0:
                # 根菜单
                root_menus.append(menu)
            else:
                # 查找父菜单并添加为子菜单
                parent_menu = menu_dict.get(parent_id)
                if parent_menu:
                    parent_menu["children"].append(menu)

        return root_menus

    async def list(self,request: Request):
        """
        获取菜单列表，构建菜单树结构
        """
        # 获取所有菜单数据
        qs = self.queryset.filter(is_deleted=False)

        # 应用排序
        if self.ordering:
            qs = qs.order_by(*self.ordering)

        # 获取所有菜单对象
        menus = await qs

        # 将菜单转换为字典列表，方便构建树形结构
        menu_list = []
        for menu in menus:
            menu_dict = {
                "id": menu.id,  # 添加 id 字段，用于构建树形结构
                "uuid": menu.uuid,
                "name": menu.name,
                "path": menu.path,
                "remark": menu.remark,
                "menu_type": menu.menu_type,
                "icon": menu.icon,
                "order": menu.order,
                "parent_id": menu.parent_id,
                "is_hidden": menu.is_hidden,
                "component": menu.component,
                "keepalive": menu.keepalive,
                "redirect": menu.redirect,
                "children": []
            }
            menu_list.append(menu_dict)

        # 构建菜单树
        menu_tree = self._build_menu_tree(menu_list)

        # 序列化并返回
        serializer = self.get_serializer(menu_tree, many=True)
        return CoreResponse(serializer)

    async def retrieve(self, request: Request):
        """
        获取菜单详情
        """
        self.request = request
        obj = await self.get_object()
        serializer = self.get_serializer(obj)
        return CoreResponse(serializer)

    async def create(self,request: Request, data=Body(...)):
        """
        创建菜单
        """
        obj = await self.queryset.create(**self.serialize_input_data(data))

        return CoreResponse(msg='创建成功', data={"id": obj.id})

    async def update(self,request: Request, data=Body(...)):
        """
        更新菜单
        """
        self.request = request
        obj = await self.get_object()
        await obj.update_from_dict(self.serialize_input_data(data)).save()
        return CoreResponse(msg='更新成功', data={"id": obj.id})