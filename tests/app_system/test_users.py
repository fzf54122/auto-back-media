# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_users.py
# @Email: fzf54122@163.com
# @Description: 用户管理测试

from tests.base_test import BaseTestViewSet
from application.app_system.models import UserModel
from tests.mock_data import mock_users


class TestUserViewSet(BaseTestViewSet):
    """用户管理测试类"""
    model = UserModel
    mock_data = mock_users
    api_prefix = "/api/users"
    required_fields = {}
    field_mapping = {}
    primary_update_field = "username"