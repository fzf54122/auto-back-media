# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_audit_log.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from uuid import UUID

@patch("application.app_base.apis.AuditLogViewSet.model")
@patch("application.app_base.apis.AuditLogViewSet.get_queryset")
@patch("commons.core.permission.DependPermisson")
def test_get_audit_logs_list(mock_permission, mock_get_queryset, mock_model, client: TestClient):
    """测试获取审计日志列表"""
    # 模拟审计日志数据
    mock_log1 = MagicMock()
    mock_log1.id = 1
    mock_log1.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_log1.user_id = 1
    mock_log1.username = "admin"
    mock_log1.ip_address = "127.0.0.1"
    mock_log1.action = "登录"
    mock_log1.method = "POST"
    mock_log1.path = "/api/login"
    mock_log1.status_code = 200
    mock_log1.created_at = "2023-01-01T00:00:00"
    
    mock_log2 = MagicMock()
    mock_log2.id = 2
    mock_log2.uuid = UUID("87654321-4321-8765-4321-567812345678")
    mock_log2.user_id = 1
    mock_log2.username = "admin"
    mock_log2.ip_address = "127.0.0.1"
    mock_log2.action = "创建用户"
    mock_log2.method = "POST"
    mock_log2.path = "/api/users"
    mock_log2.status_code = 200
    mock_log2.created_at = "2023-01-01T00:01:00"
    
    # 设置模拟返回
    mock_get_queryset.return_value = [mock_log1, mock_log2]
    
    # 发送请求
    response = client.get("/api/audit-log/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法调用
    mock_get_queryset.assert_called_once()

@patch("application.app_base.apis.AuditLogViewSet.get_object")
@patch("commons.core.permission.DependPermisson")
def test_get_audit_log_detail(mock_permission, mock_get_object, client: TestClient):
    """测试获取单个审计日志详情"""
    # 模拟审计日志数据
    mock_log = MagicMock()
    mock_log.uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_log.user_id = 1
    mock_log.username = "admin"
    mock_log.ip_address = "127.0.0.1"
    mock_log.action = "登录"
    mock_log.method = "POST"
    mock_log.path = "/api/login"
    mock_log.status_code = 200
    
    # 设置模拟返回
    mock_get_object.return_value = mock_log
    
    # 发送请求
    response = client.get("/api/audit-log/12345678-1234-5678-1234-567812345678/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法调用
    mock_get_object.assert_called_once()