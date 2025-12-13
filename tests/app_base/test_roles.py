# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_roles.py
# @Email: fzf54122@163.com
# @Description: 角色管理测试

from tests.base_test import BaseTestViewSet
from application.app_base.models import RoleModel
from tests.mock_data import mock_roles


class TestRoleViewSet(BaseTestViewSet):
    """角色管理测试类"""
    model = RoleModel
    mock_data = mock_roles
    api_prefix = "/api/roles"
    required_fields = {}
    field_mapping = {}