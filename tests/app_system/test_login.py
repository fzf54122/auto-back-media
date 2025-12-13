# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_login.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from application.app_system.serializers.LoginSerializers import CredentialsSchema, RefreshTokenRequest

@pytest.mark.asyncio
@patch("application.app_system.apis.LoginVietSet.service")
@patch("application.app_system.apis.LoginVietSet.cache_manager")
async def test_login_success(mock_cache_manager, mock_service, client: TestClient):
    """测试用户登录成功"""
    # 模拟用户数据
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.is_superuser = False
    mock_user.uuid = "test-uuid"
    
    # 设置模拟服务返回
    mock_service.authenticate.return_value = mock_user
    mock_service.update_last_login.return_value = None
    mock_cache_manager.set.return_value = None
    
    # 登录请求数据
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    # 发送登录请求
    response = client.post("/api/auth/login/auth/login/", json=login_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["username"] == "testuser"
    
    # 验证服务方法被调用
    mock_service.authenticate.assert_called_once()
    mock_service.update_last_login.assert_called_once_with(1)
    mock_cache_manager.set.assert_called_once()

@pytest.mark.asyncio
@patch("application.app_system.apis.LoginVietSet.service")
async def test_login_failure(mock_service, client: TestClient):
    """测试用户登录失败"""
    # 设置模拟服务抛出异常
    from application.app_system.exceptions import UserNotFoundException
    mock_service.authenticate.side_effect = UserNotFoundException
    
    # 登录请求数据
    login_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }
    
    # 发送登录请求
    response = client.post("/api/auth/login/auth/login/", json=login_data)
    
    # 验证响应
    assert response.status_code == 404
    data = response.json()
    assert data["code"] != 0
    
    # 验证服务方法被调用
    mock_service.authenticate.assert_called_once()

@pytest.mark.asyncio
@patch("application.app_system.apis.LoginVietSet.cache_manager")
@patch("application.app_system.apis.LoginVietSet.verify_token")
async def test_logout_success(mock_verify_token, mock_cache_manager, client: TestClient):
    """测试用户退出成功"""
    # 设置模拟
    mock_verify_token.return_value = MagicMock(user_id=1)
    mock_cache_manager.get.return_value = None
    mock_cache_manager.set.return_value = None
    mock_cache_manager.delete.return_value = None
    
    # 发送退出请求
    response = client.post(
        "/api/auth/login/auth/logout/",
        headers={"Authorization": "Bearer test_access_token"}
    )
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    
    # 验证方法被调用
    mock_verify_token.assert_called_once()
    mock_cache_manager.set.assert_called_once()
    mock_cache_manager.delete.assert_called_once()

@pytest.mark.asyncio
@patch("application.app_system.apis.LoginVietSet.cache_manager")
@patch("application.app_system.apis.LoginVietSet.verify_token")
@patch("application.app_system.apis.LoginVietSet.create_token_pair")
async def test_refresh_token_success(mock_create_token_pair, mock_verify_token, mock_cache_manager, client: TestClient):
    """测试刷新token成功"""
    # 设置模拟
    mock_verify_token.return_value = MagicMock(user_id=1)
    mock_cache_manager.get.return_value = "test_refresh_token"
    mock_cache_manager.set.return_value = None
    
    # 模拟新的token对
    mock_create_token_pair.return_value = ("new_access_token", "new_refresh_token")
    
    # 发送刷新token请求
    refresh_data = {
        "refresh_token": "test_refresh_token"
    }
    
    response = client.post("/api/auth/login/auth/refresh/", json=refresh_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    
    # 验证方法被调用
    mock_verify_token.assert_called_once()
    mock_cache_manager.get.assert_called_once()
    mock_create_token_pair.assert_called_once()
    mock_cache_manager.set.assert_called_once()