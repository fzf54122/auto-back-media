# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_depts.py
# @Email: fzf54122@163.com
# @Description: 部门管理测试

from tests.base_test import BaseTestViewSet
from application.app_base.models import DeptsModel
from tests.mock_data import mock_depts


class TestDeptViewSet(BaseTestViewSet):
    """部门管理测试类"""
    model = DeptsModel
    mock_data = mock_depts
    api_prefix = "/api/depts"
    required_fields = {}
    field_mapping = {}