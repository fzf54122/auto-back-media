# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_menus.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from uuid import UUID

@patch("application.app_base.apis.MenuViewSet.model")
@patch("commons.core.permission.DependPermisson")
def test_get_menu_tree(mock_permission, mock_model, client: TestClient):
    """测试获取菜单树结构"""
    # 模拟菜单数据
    mock_menu1 = MagicMock()
    mock_menu1.id = 1
    mock_menu1.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_menu1.name = "首页"
    mock_menu1.path = "/dashboard"
    mock_menu1.remark = "首页菜单"
    mock_menu1.menu_type = "C"
    mock_menu1.icon = "home"
    mock_menu1.order = 1
    mock_menu1.parent_id = 0
    mock_menu1.is_hidden = False
    mock_menu1.component = "Dashboard"
    mock_menu1.keepalive = True
    mock_menu1.redirect = None
    mock_menu1.is_deleted = False
    
    mock_menu2 = MagicMock()
    mock_menu2.id = 2
    mock_menu2.uuid = UUID("87654321-4321-8765-4321-567812345678")
    mock_menu2.name = "用户管理"
    mock_menu2.path = "/users"
    mock_menu2.remark = "用户管理菜单"
    mock_menu2.menu_type = "C"
    mock_menu2.icon = "user"
    mock_menu2.order = 2
    mock_menu2.parent_id = 1
    mock_menu2.is_hidden = False
    mock_menu2.component = "Users"
    mock_menu2.keepalive = True
    mock_menu2.redirect = None
    mock_menu2.is_deleted = False
    
    # 设置模拟返回
    mock_queryset = MagicMock()
    mock_queryset.order_by.return_value = [mock_menu1, mock_menu2]
    mock_model.filter.return_value = mock_queryset
    
    # 发送请求
    response = client.get("/api/menus/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]) > 0
    
    # 验证方法调用
    mock_model.filter.assert_called_once_with(is_deleted=False)
    mock_queryset.order_by.assert_called_once()

@patch("application.app_base.apis.MenuViewSet.get_object")
@patch("commons.core.permission.DependPermisson")
def test_get_menu_detail(mock_permission, mock_get_object, client: TestClient):
    """测试获取菜单详情"""
    # 模拟菜单数据
    mock_menu = MagicMock()
    mock_menu.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_menu.name = "首页"
    mock_menu.path = "/dashboard"
    
    # 设置模拟返回
    mock_get_object.return_value = mock_menu
    
    # 发送请求
    response = client.get("/api/menus/12345678-1234-5678-1234-567812345678/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法调用
    mock_get_object.assert_called_once()

@patch("application.app_base.apis.MenuViewSet.model")
@patch("application.app_base.apis.MenuViewSet.handle_data")
@patch("commons.core.permission.DependPermisson")
def test_create_menu(mock_permission, mock_handle_data, mock_model, client: TestClient):
    """测试创建菜单"""
    # 模拟创建的菜单
    mock_created_menu = MagicMock()
    mock_created_menu.id = 1
    mock_model.create.return_value = mock_created_menu
    mock_handle_data.return_value = {"name": "新菜单", "path": "/new-menu"}
    
    # 创建菜单请求数据
    create_data = {
        "name": "新菜单",
        "path": "/new-menu",
        "menu_type": "C",
        "icon": "new",
        "order": 3,
        "parent_id": 0,
        "component": "NewComponent"
    }
    
    # 发送请求
    response = client.post("/api/menus/", json=create_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "创建成功"
    
    # 验证方法调用
    mock_handle_data.assert_called_once_with(create_data)
    mock_model.create.assert_called_once_with(**mock_handle_data.return_value)

@patch("application.app_base.apis.MenuViewSet.get_object")
@patch("application.app_base.apis.MenuViewSet.handle_data")
@patch("commons.core.permission.DependPermisson")
def test_update_menu(mock_permission, mock_handle_data, mock_get_object, client: TestClient):
    """测试更新菜单"""
    # 模拟菜单数据
    mock_menu = MagicMock()
    mock_menu.update_from_dict.return_value = True
    mock_get_object.return_value = mock_menu
    mock_handle_data.return_value = {"name": "更新菜单", "path": "/updated-menu"}
    
    # 更新菜单请求数据
    update_data = {
        "name": "更新菜单",
        "path": "/updated-menu",
        "icon": "updated"
    }
    
    # 发送请求
    response = client.put("/api/menus/12345678-1234-5678-1234-567812345678/", json=update_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "更新成功"
    
    # 验证方法调用
    mock_get_object.assert_called_once()
    mock_handle_data.assert_called_once_with(update_data)
    mock_menu.update_from_dict.assert_called_once_with(**mock_handle_data.return_value)