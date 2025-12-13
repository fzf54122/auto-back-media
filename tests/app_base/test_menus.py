# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_menus.py
# @Email: fzf54122@163.com
# @Description: 菜单管理视图集测试 - 使用通用测试模板

import pytest
from httpx import AsyncClient

from tests.base_test import BaseTestViewSet
from tests.mock_data import mock_menus
from application.app_base.models import MenuModel


class TestMenuViewSet(BaseTestViewSet):
    """菜单管理视图集测试类 - 继承自通用测试基类"""
    
    # 配置测试基本信息
    model = MenuModel
    mock_data = mock_menus
    api_prefix = "/api/menus"
    
    # 必填字段默认值
    required_fields = {
        "component": "Layout"
    }
    
    # 字段映射配置
    field_mapping = {
        "menu_type": {
            "1": "catalog",
            "2": "menu"
        }
    }
    
    # 可以选择性重写父类方法以实现自定义测试逻辑
    # @pytest.mark.asyncio
    # async def test_get_menu_list(self, async_client: AsyncClient, auth_headers):
    #     """自定义获取菜单列表测试"""
    #     # 自定义测试逻辑
    #     pass