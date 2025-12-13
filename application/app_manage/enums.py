# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: enums.py
# @Email: fzf54122@163.com
# @Description: 枚举类型定义


class TaskManageStatus(object):
    NOT_STARTED = 10
    IN_PROGRESS = 20
    SUCCESS = 30
    FAILED = 40

    @classmethod
    def choice(cls):
        return (
        (cls.NOT_STARTED,"未开始"),
        (cls.IN_PROGRESS,'运行中'),
        (cls.SUCCESS,'成功'),
        (cls.FAILED,'失败')
        )

class MediaUserStatus(object):
    NOT_ACTIVE = 10  # 未激活
    ACTIVE = 20      # 激活
    SUSPENDED = 30   # 已禁用

    @classmethod
    def choice(cls):
        return (
            (cls.NOT_ACTIVE, "未激活"),
            (cls.ACTIVE, "激活"),
            (cls.SUSPENDED, "已禁用"),
        )