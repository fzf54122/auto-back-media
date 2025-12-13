# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_webs.py
# @Email: fzf54122@163.com
# @Description: Web管理测试

from tests.base_test import BaseTestViewSet
from application.app_manage.models import WebModel
from tests.mock_data import mock_webs


class TestWebViewSet(BaseTestViewSet):
    """Web管理测试类"""
    model = WebModel
    mock_data = mock_webs
    api_prefix = "/api/webs"
    required_fields = {}
    field_mapping = {}
    primary_update_field = "project_url"