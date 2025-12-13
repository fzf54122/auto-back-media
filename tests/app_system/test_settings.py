# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_settings.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from uuid import UUID

@pytest.mark.asyncio
@patch("application.app_system.apis.SettingsViewSet.get_queryset")
async def test_get_settings_list(mock_get_queryset, client: TestClient):
    """测试获取系统设置列表"""
    # 模拟设置列表数据
    mock_settings = [
        MagicMock(
            uuid=UUID("12345678-1234-5678-1234-567812345678"),
            key="site_name",
            value="我的网站",
            description="网站名称",
            is_public=True,
            category="site"
        ),
        MagicMock(
            uuid=UUID("87654321-4321-8765-4321-567812345678"),
            key="site_logo",
            value="/logo.png",
            description="网站Logo",
            is_public=True,
            category="site"
        )
    ]
    
    # 设置模拟返回
    mock_queryset = MagicMock()
    mock_queryset.all.return_value = mock_settings
    mock_get_queryset.return_value = mock_queryset
    
    mock_service.get_list.return_value = {
        "items": mock_settings,
        "total": 2,
        "limit": 10,
        "offset": 0
    }
    
    # 发送请求
    response = client.get("/api/settings/?limit=10&offset=0")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]["items"]) == 2
    
    # 验证方法调用
    mock_service.get_list.assert_called_once()

@pytest.mark.asyncio
@patch("application.app_system.apis.SettingsViewSet.service")
async def test_get_setting_detail(mock_service, client: TestClient):
    """测试获取单个系统设置详情"""
    # 模拟设置数据
    mock_setting = MagicMock(
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        key="site_name",
        value="我的网站",
        description="网站名称",
        is_public=True,
        category="site"
    )
    
    # 设置模拟返回
    mock_service.get_detail.return_value = mock_setting
    
    # 发送请求
    response = client.get("/api/settings/12345678-1234-5678-1234-567812345678/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["key"] == "site_name"
    
    # 验证方法调用
    mock_service.get_detail.assert_called_once()

@pytest.mark.asyncio
async def test_create_setting(client: TestClient):
    """测试创建系统设置"""
    # 创建设置请求数据
    create_data = {
        "key": "site_name",
        "value": "我的网站",
        "description": "网站名称",
        "is_public": True,
        "category": "site"
    }
    
    # 发送请求
    response = client.post("/api/settings/", json=create_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0

@pytest.mark.asyncio
async def test_update_setting(client: TestClient):
    """测试更新系统设置"""
    # 更新设置请求数据
    update_data = {
        "value": "更新后的网站名称",
        "description": "更新后的网站名称描述",
        "is_public": False,
        "category": "updated"
    }
    
    # 发送请求
    response = client.put("/api/settings/12345678-1234-5678-1234-567812345678/", json=update_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0

@pytest.mark.asyncio
async def test_delete_setting(client: TestClient):
    """测试删除系统设置"""
    # 发送请求
    response = client.delete("/api/settings/12345678-1234-5678-1234-567812345678/")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0