# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_menus.py
# @Email: fzf54122@163.com
# @Description: 菜单管理视图集测试

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from tests.mock_data import mock_menus
from application.app_base.models import MenuModel


class TestMenuViewSet:
    """菜单管理视图集测试类"""

    @pytest.fixture(autouse=True)
    async def setup(self, clean_database):
        """测试前置条件：清理数据库并初始化测试数据"""
        # clean_database已经是异步fixture，不需要await
        
        # 批量创建测试菜单，只保留必要字段
        for menu_data in mock_menus:
            # 只保留必要的字段，移除自动生成的字段，并添加必填的component字段
            # 将menu_type从字符串"1"或"2"转换为正确的枚举值
            menu_type = "catalog" if menu_data["menu_type"] == "1" else "menu"
            menu_create_data = {
                "name": menu_data["name"],
                "path": menu_data["path"],
                "menu_type": menu_type,
                "parent_id": menu_data["parent_id"],
                "order": menu_data["order"],
                "icon": menu_data["icon"],
                "component": "Layout"
            }
            await MenuModel.create(**menu_create_data)

    @pytest.mark.asyncio
    async def test_get_menu_list(self, async_client: AsyncClient, auth_headers):
        """测试获取菜单列表"""
        response = await async_client.get(
            "/api/menus/list/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]) >= 1

    @pytest.mark.asyncio
    async def test_create_menu(self, async_client: AsyncClient, auth_headers):
        """测试创建菜单"""
        new_menu = {
            "name": "测试菜单",
            "path": "/test",
            "menu_type": "catalog",
            "parent_id": 0,
            "order": 4,
            "icon": "test",
            "component": "Layout"
        }
        
        response = await async_client.post(
            "/api/menus/create/",
            json=new_menu,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["name"] == new_menu["name"]

    @pytest.mark.asyncio
    async def test_get_menu_detail(self, async_client: AsyncClient, auth_headers):
        """测试获取菜单详情"""
        # 获取第一个菜单的ID
        menu = await MenuModel.all().first()
        
        response = await async_client.get(
            f"/api/menus/{menu.uuid}/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["uuid"] == str(menu.uuid)

    @pytest.mark.asyncio
    async def test_update_menu(self, async_client: AsyncClient, auth_headers):
        """测试更新菜单"""
        # 获取第一个菜单的ID
        menu = await MenuModel.all().first()
        
        update_data = {
            "name": "更新后的菜单名称",
            "path": "/updated",
            "menu_type": "menu",
            "order": 2,
            "icon": "updated"
        }
        
        response = await async_client.put(
            f"/api/menus/{menu.uuid}/",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["name"] == update_data["name"]

    @pytest.mark.asyncio
    async def test_delete_menu(self, async_client: AsyncClient, auth_headers):
        """测试删除菜单"""
        # 获取第一个菜单的ID
        menu = await MenuModel.all().first()
        
        response = await async_client.delete(
            f"/api/menus/{menu.uuid}/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        
        # 验证菜单已被删除
        deleted_menu = await MenuModel.all().filter(uuid=menu.uuid).first()
        assert deleted_menu is None