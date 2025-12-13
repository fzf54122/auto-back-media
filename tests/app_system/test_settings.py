# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_settings.py
# @Email: fzf54122@163.com
# @Description: 系统设置测试

from tests.base_test import BaseTestViewSet
from application.app_system.models import SettingsModel
from tests.mock_data import mock_settings


class TestSettingsViewSet(BaseTestViewSet):
    """系统设置测试类"""
    model = SettingsModel
    mock_data = mock_settings
    api_prefix = "/api/settings"
    required_fields = {}
    field_mapping = {}
    primary_update_field = "key"