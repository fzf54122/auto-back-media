# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: mock_data.py
# @Email: fzf54122@163.com
# @Description: Mock数据文件，包含所有主要实体的模拟数据，不包含id字段

from uuid import UUID
from datetime import datetime

# 部门数据
mock_depts = [
    {
        "uuid": UUID("12345678-1234-5678-1234-567812345678"),
        "name": "技术部",
        "remark": "技术开发部门",
        "parent_id": 0,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("87654321-4321-8765-4321-567812345678"),
        "name": "前端组",
        "remark": "前端开发组",
        "parent_id": 1,
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("abcdef12-3456-7890-abcd-ef1234567890"),
        "name": "后端组",
        "remark": "后端开发组",
        "parent_id": 1,
        "created_at": "2023-01-03T00:00:00",
        "updated_at": "2023-01-03T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 用户数据
mock_users = [
    {
        "uuid": UUID("11111111-1111-1111-1111-111111111111"),
        "username": "admin",
        "email": "admin@example.com",
        "phone": "13800138000",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # 密码: admin123
        "real_name": "管理员",
        "avatar": "",
        "gender": "male",
        "birthday": "1990-01-01",
        "dept_id": 1,
        "role_ids": [1, 2],
        "status": "active",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("22222222-2222-2222-2222-222222222222"),
        "username": "user1",
        "email": "user1@example.com",
        "phone": "13800138001",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # 密码: admin123
        "real_name": "用户1",
        "avatar": "",
        "gender": "male",
        "birthday": "1995-01-01",
        "dept_id": 2,
        "role_ids": [2],
        "status": "active",
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 角色数据
mock_roles = [
    {
        "uuid": UUID("33333333-3333-3333-3333-333333333333"),
        "name": "超级管理员",
        "remark": "拥有所有权限",
        "menu_ids": [1, 2, 3, 4, 5],
        "api_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("44444444-4444-4444-4444-444444444444"),
        "name": "普通用户",
        "remark": "拥有基本权限",
        "menu_ids": [1, 2, 3],
        "api_ids": [1, 2, 3, 4],
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 菜单数据
mock_menus = [
    {
        "uuid": UUID("55555555-5555-5555-5555-555555555555"),
        "name": "系统管理",
        "path": "/system",
        "menu_type": "1",
        "parent_id": 0,
        "order": 1,
        "icon": "system",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("66666666-6666-6666-6666-666666666666"),
        "name": "用户管理",
        "path": "/system/user",
        "menu_type": "2",
        "parent_id": 1,
        "order": 1,
        "icon": "user",
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("77777777-7777-7777-7777-777777777777"),
        "name": "角色管理",
        "path": "/system/role",
        "menu_type": "2",
        "parent_id": 1,
        "order": 2,
        "icon": "role",
        "created_at": "2023-01-03T00:00:00",
        "updated_at": "2023-01-03T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# API数据
mock_apis = [
    {
            "uuid": UUID("88888888-8888-8888-8888-888888888888"),
            "path": "/api/users/",
            "method": "GET",
            "summary": "获取用户列表",
            "tags": ["用户管理"],
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "is_active": True,
            "is_deleted": False
    },
    {
        "uuid": UUID("99999999-9999-9999-9999-999999999999"),
        "path": "/api/users/",
        "method": "POST",
        "summary": "创建用户",
        "tags": ["用户管理"],
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        "path": "/api/depts/",
        "method": "GET",
        "summary": "获取部门列表",
        "tags": ["部门管理"],
        "created_at": "2023-01-03T00:00:00",
        "updated_at": "2023-01-03T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 文件数据
mock_files = [
    {
        "uuid": UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
        "file_id": "file_1234567890",
        "original_filename": "example.txt",
        "file_type": "txt",
        "file_size": 1024,
        "upload_user_id": 1,
        "file_path": "/uploads/example.txt",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"),
        "file_id": "file_0987654321",
        "original_filename": "image.jpg",
        "file_type": "jpg",
        "file_size": 1024000,
        "upload_user_id": 2,
        "file_path": "/uploads/image.jpg",
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 审计日志数据
mock_audit_logs = [
    {
        "uuid": UUID("dddddddd-dddd-dddd-dddd-dddddddddddd"),
        "user_id": 1,
        "username": "admin",
        "module": "用户管理",
        "summary": "登录系统",
        "method": "POST",
        "path": "/api/login/",
        "status": 200,
        "response_time": 100,
        "request_args": {"username": "admin", "password": "******"},
        "response_body": {"code": 0, "message": "登录成功"},
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"),
        "user_id": 1,
        "username": "admin",
        "module": "部门管理",
        "summary": "创建部门",
        "method": "POST",
        "path": "/api/depts/",
        "status": 200,
        "response_time": 200,
        "request_args": {"name": "测试部门", "parent_id": 1},
        "response_body": {"code": 0, "message": "创建成功"},
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 系统设置数据
mock_settings = [
    {
        "uuid": UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"),
        "key": "site_name",
        "value": "自动化后台管理系统",
        "description": "网站名称",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("00000000-0000-0000-0000-000000000000"),
        "key": "site_logo",
        "value": "/static/logo.png",
        "description": "网站Logo",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 媒体用户数据
mock_media_users = [
    {
        "uuid": UUID("1234abcd-5678-ef90-1234-abcd5678ef90"),
        "username": "media_user1",
        "email": "media1@example.com",
        "phone": "13900139000",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # 密码: admin123
        "real_name": "媒体用户1",
        "avatar": "",
        "gender": "male",
        "birthday": "1990-01-01",
        "status": 1,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("abcd1234-ef56-7890-abcd-1234ef567890"),
        "username": "media_user2",
        "email": "media2@example.com",
        "phone": "13900139001",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # 密码: admin123
        "real_name": "媒体用户2",
        "avatar": "",
        "gender": "female",
        "birthday": "1995-01-01",
        "status": 1,
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# 任务管理数据
mock_task_manages = [
    {
        "uuid": UUID("9876abcd-5432-ef10-9876-abcd5432ef10"),
        "project_name": "测试平台",
        "media_type": "微博",
        "media_username": "test_user1",
        "task_topic": "测试任务1",
        "crontab_time": "2023-01-01T00:00:00",
        "last_time": "2023-01-01T00:00:00",
        "status": 0,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("abcd9876-ef54-3210-abcd-9876ef543210"),
        "project_name": "测试平台2",
        "media_type": "微信",
        "media_username": "test_user2",
        "task_topic": "测试任务2",
        "crontab_time": "2023-01-02T00:00:00",
        "last_time": "2023-01-02T00:00:00",
        "status": 1,
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T01:00:00",
        "is_active": True,
        "is_deleted": False
    }
]

# Web数据
mock_webs = [
    {
        "uuid": UUID("11223344-5566-7788-9900-aabbccddeeff"),
        "project_type": "website",
        "project_url": "https://www.example.com",
        "description": "示例网站",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "is_active": True,
        "is_deleted": False
    },
    {
        "uuid": UUID("aabbccdd-eeff-1122-3344-556677889900"),
        "project_type": "api",
        "project_url": "https://api.example.com",
        "description": "示例API",
        "created_at": "2023-01-02T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "is_active": True,
        "is_deleted": False
    }
]