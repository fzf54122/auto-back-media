# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: test_task_manages.py
# @Email: fzf54122@163.com
# @Description: 任务管理测试

from tests.base_test import BaseTestViewSet
from application.app_manage.models import TaskManageModel
from tests.mock_data import mock_task_manages


class TestTaskManageViewSet(BaseTestViewSet):
    """任务管理测试类"""
    model = TaskManageModel
    mock_data = mock_task_manages
    api_prefix = "/api/task_manage"
    required_fields = {}
    field_mapping = {}
    primary_update_field = "task_topic"