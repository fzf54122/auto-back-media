# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_depts.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from uuid import UUID

@patch("application.app_base.apis.DeptsViewSet.queryset")
@patch("commons.core.permission.DependPermisson")
def test_get_depts_list(mock_permission, mock_queryset, client: TestClient):
    """测试获取部门列表"""
    # 模拟部门数据
    mock_dept1 = MagicMock()
    mock_dept1.id = 1
    mock_dept1.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_dept1.name = "技术部"
    mock_dept1.remark = "技术开发部门"
    mock_dept1.parent_id = 0
    mock_dept1.created_at = "2023-01-01T00:00:00"
    
    mock_dept2 = MagicMock()
    mock_dept2.id = 2
    mock_dept2.uuid = UUID("87654321-4321-8765-4321-567812345678")
    mock_dept2.name = "前端组"
    mock_dept2.remark = "前端开发组"
    mock_dept2.parent_id = 1
    mock_dept2.created_at = "2023-01-02T00:00:00"
    
    # 设置模拟返回
    mock_queryset.filter.return_value.order_by.return_value = [mock_dept1, mock_dept2]
    
    # 发送请求
    response = client.get("/api/depts/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法调用
    mock_queryset.filter.assert_called_once()

@patch("application.app_base.apis.DeptsViewSet.queryset")
@patch("application.app_base.apis.DeptsViewSet.service")
@patch("commons.core.permission.DependPermisson")
def test_create_dept(mock_permission, mock_service, mock_queryset, client: TestClient):
    """测试创建部门"""
    # 模拟创建的部门
    mock_created_dept = MagicMock()
    mock_created_dept.id = 1
    mock_created_dept.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_created_dept.name = "新部门"
    mock_created_dept.parent_id = 0
    mock_queryset.create.return_value = mock_created_dept
    
    # 创建部门请求数据
    create_data = {
        "name": "新部门",
        "remark": "新创建的部门",
        "parent_id": 0
    }
    
    # 发送请求
    response = client.post("/api/depts/", json=create_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法调用
    mock_queryset.create.assert_called_once_with(**create_data)
    mock_service.update_dept_closure.assert_called_once_with(mock_created_dept)

@patch("application.app_base.apis.DeptsViewSet.queryset")
@patch("application.app_base.apis.DeptsViewSet.service")
@patch("commons.core.permission.DependPermisson")
def test_update_dept(mock_permission, mock_service, mock_queryset, client: TestClient):
    """测试更新部门"""
    # 模拟部门数据
    mock_dept = MagicMock()
    mock_dept.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_dept.name = "技术部"
    mock_dept.parent_id = 0
    mock_queryset.get_or_none.return_value = mock_dept
    
    # 更新部门请求数据
    update_data = {
        "name": "技术开发部",
        "remark": "技术开发部门"
    }
    
    # 发送请求
    response = client.put("/api/depts/12345678-1234-5678-1234-567812345678/", json=update_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法调用
    mock_queryset.get_or_none.assert_called_once_with(uuid="12345678-1234-5678-1234-567812345678")
    mock_dept.update.assert_called_once_with(**update_data)
    mock_service.update_dept_closure.assert_called_once_with(mock_dept)

@patch("application.app_base.apis.DeptsViewSet.queryset")
@patch("application.app_base.models.DeptClosure")
@patch("commons.core.permission.DependPermisson")
def test_delete_dept(mock_permission, mock_dept_closure, mock_queryset, client: TestClient):
    """测试删除部门"""
    # 模拟部门数据
    mock_dept = MagicMock()
    mock_dept.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_dept.id = 1
    mock_queryset.get_or_none.return_value = mock_dept
    
    # 发送请求
    response = client.delete("/api/depts/12345678-1234-5678-1234-567812345678/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "部门删除成功"
    
    # 验证方法调用
    mock_queryset.get_or_none.assert_called_once_with(uuid="12345678-1234-5678-1234-567812345678")
    mock_dept.update.assert_called_once_with(is_deleted=True)
    mock_dept_closure.filter.assert_called_once_with(descendant=mock_dept.id)
    mock_dept_closure.filter.return_value.update.assert_called_once_with(is_deleted=True)