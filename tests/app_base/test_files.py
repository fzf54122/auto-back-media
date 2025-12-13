# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_files.py
# @Email: fzf54122@163.com
# @Description: 文件管理测试

from tests.base_test import BaseTestViewSet
from application.app_base.models import FileModel
from tests.mock_data import mock_files


class TestFileViewSet(BaseTestViewSet):
    """文件管理测试类"""
    model = FileModel
    mock_data = mock_files
    api_prefix = "/api/files"
    required_fields = {}
    field_mapping = {}
    primary_update_field = "original_filename"