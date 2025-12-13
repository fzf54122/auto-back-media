# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_apis.py
# @Email: fzf54122@163.com
# @Description: API管理测试

from tests.base_test import BaseTestViewSet
from application.app_base.models import ApiModel
from tests.mock_data import mock_apis


class TestApiViewSet(BaseTestViewSet):
    """API管理测试类"""
    model = ApiModel
    mock_data = mock_apis
    api_prefix = "/api/apis"
    required_fields = {}
    field_mapping = {}
    primary_update_field = "summary"