# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_files.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from io import BytesIO

@patch("application.app_base.apis.FilesViewSet.service")
@patch("commons.core.permission.DependPermisson")
def test_upload_file(mock_permission, mock_service, client: TestClient):
    """测试文件上传接口"""
    # 模拟文件上传服务返回
    mock_response = MagicMock()
    mock_response.body = {
        "file_url": "http://example.com/uploads/test.txt",
        "file_name": "test.txt",
        "file_size": 1024,
        "file_type": "text/plain"
    }
    mock_service.upload_file.return_value = mock_response
    
    # 创建测试文件
    test_file = BytesIO(b"Test file content")
    test_file.name = "test.txt"
    
    # 发送请求
    response = client.post("/api/upload/", files={"file": test_file})
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "file_url" in data["data"]
    
    # 验证方法调用
    mock_service.upload_file.assert_called_once()