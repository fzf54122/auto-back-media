# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_media_users.py
# @Email: fzf54122@163.com
# @Description: 媒体用户管理测试

from tests.base_test import BaseTestViewSet
from application.app_manage.models import MediaUserModel
from tests.mock_data import mock_media_users


class TestMediaUserViewSet(BaseTestViewSet):
    """媒体用户管理测试类"""
    model = MediaUserModel
    mock_data = mock_media_users
    api_prefix = "/api/media-users"
    required_fields = {}
    field_mapping = {}
    primary_update_field = "media_username"