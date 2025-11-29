class AutoBaseException(Exception):
    code = 0
    detail = '基础错误'

class TokenInvalidException(AutoBaseException):
    code = 1000
    detail = 'Token无效'

class TokenExpiredException(AutoBaseException):
    code = 1010
    detail = 'Token 已注销'

class UpdateOtherUserPasswordException(AutoBaseException):
    code = 1020
    detail = '没有权限修改其他用户的密码'

class UserNotFoundException(AutoBaseException):
    code = 1100
    detail = '用户不存在'

class OldPasswordErrorException(AutoBaseException):
    code = 1104
    detail = '旧密码错误'