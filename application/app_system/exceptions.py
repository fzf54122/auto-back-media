# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: exceptions.py
# @Email: fzf54122@163.com
# @Description: 自定义异常定义、
from fast_generic_api.core.exceptions import CoreException

class TokenInvalidException(CoreException):
    code = 1000
    detail = 'Token无效'

class TokenExpiredException(CoreException):
    code = 1010
    detail = 'Token 已注销'

class UpdateOtherUserPasswordException(CoreException):
    code = 1020
    detail = '没有权限修改其他用户的密码'

class UserNotFoundException(CoreException):
    code = 1100
    detail = '用户不存在'

class OldPasswordErrorException(CoreException):
    code = 1104
    detail = '旧密码错误'