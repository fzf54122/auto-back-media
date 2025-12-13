# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_roles.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from uuid import UUID

@patch("application.app_base.apis.RoleViewSet.model")
@patch("application.app_base.apis.RoleViewSet.get_queryset")
@patch("application.app_base.apis.RoleViewSet.filter_class")
@patch("application.app_base.apis.RoleViewSet.pagination_class")
@patch("commons.core.permission.DependPermisson")
def test_get_roles_list(mock_permission, mock_pagination, mock_filter, mock_get_queryset, mock_model, client: TestClient):
    """测试获取角色列表"""
    # 模拟角色数据
    mock_role1 = MagicMock()
    mock_role1.id = 1
    mock_role1.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_role1.name = "管理员"
    mock_role1.remark = "系统管理员角色"
    mock_role1.created_at = "2023-01-01T00:00:00"
    mock_role1.to_dict.return_value = {
        "id": 1,
        "uuid": "12345678-1234-5678-1234-567812345678",
        "name": "管理员",
        "remark": "系统管理员角色",
        "created_at": "2023-01-01T00:00:00"
    }
    
    mock_role2 = MagicMock()
    mock_role2.id = 2
    mock_role2.uuid = UUID("87654321-4321-8765-4321-567812345678")
    mock_role2.name = "普通用户"
    mock_role2.remark = "普通用户角色"
    mock_role2.created_at = "2023-01-02T00:00:00"
    mock_role2.to_dict.return_value = {
        "id": 2,
        "uuid": "87654321-4321-8765-4321-567812345678",
        "name": "普通用户",
        "remark": "普通用户角色",
        "created_at": "2023-01-02T00:00:00"
    }
    
    # 设置模拟返回
    mock_get_queryset.return_value = [mock_role1, mock_role2]
    mock_filter.return_value.qs.return_value = [mock_role1, mock_role2]
    mock_paginated_response = MagicMock()
    mock_paginated_response.return_value = {"code": 0, "data": [mock_role1.to_dict(), mock_role2.to_dict()]}
    mock_pagination.paginate.return_value = mock_paginated_response
    
    # 发送请求
    response = client.get("/api/roles/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]) == 2
    
    # 验证方法调用
    mock_get_queryset.assert_called_once()

@patch("application.app_base.apis.RoleViewSet.get_object")
@patch("commons.core.permission.DependPermisson")
def test_get_role_detail(mock_permission, mock_get_object, client: TestClient):
    """测试获取单个角色详情"""
    # 模拟角色数据
    mock_role = MagicMock()
    mock_role.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_role.name = "管理员"
    mock_role.remark = "系统管理员角色"
    
    # 设置模拟返回
    mock_get_object.return_value = mock_role
    
    # 发送请求
    response = client.get("/api/roles/12345678-1234-5678-1234-567812345678/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法调用
    mock_get_object.assert_called_once()

@patch("application.app_base.apis.RoleViewSet.model")
@patch("application.app_base.apis.RoleViewSet.handle_data")
@patch("commons.core.permission.DependPermisson")
def test_create_role(mock_permission, mock_handle_data, mock_model, client: TestClient):
    """测试创建角色"""
    # 模拟创建的角色
    mock_created_role = MagicMock()
    mock_created_role.id = 1
    mock_model.create.return_value = mock_created_role
    mock_handle_data.return_value = {"name": "新角色", "remark": "新创建的角色"}
    
    # 创建角色请求数据
    create_data = {
        "name": "新角色",
        "remark": "新创建的角色"
    }
    
    # 发送请求
    response = client.post("/api/roles/", json=create_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "创建成功"
    
    # 验证方法调用
    mock_handle_data.assert_called_once_with(create_data)
    mock_model.create.assert_called_once_with(**mock_handle_data.return_value)

@patch("application.app_base.apis.RoleViewSet.get_object")
@patch("application.app_base.apis.RoleViewSet.handle_data")
@patch("commons.core.permission.DependPermisson")
def test_update_role(mock_permission, mock_handle_data, mock_get_object, client: TestClient):
    """测试更新角色"""
    # 模拟角色数据
    mock_role = MagicMock()
    mock_role.from_dict.return_value = True
    mock_get_object.return_value = mock_role
    mock_handle_data.return_value = {"name": "更新角色", "remark": "更新后的角色备注"}
    
    # 更新角色请求数据
    update_data = {
        "name": "更新角色",
        "remark": "更新后的角色备注"
    }
    
    # 发送请求
    response = client.put("/api/roles/12345678-1234-5678-1234-567812345678/", json=update_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "更新成功"
    
    # 验证方法调用
    mock_get_object.assert_called_once()
    mock_handle_data.assert_called_once_with(update_data)
    mock_role.from_dict.assert_called_once_with(**mock_handle_data.return_value)