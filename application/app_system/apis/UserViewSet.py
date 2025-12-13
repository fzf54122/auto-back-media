# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: UserViewSet.py
# @Email: fzf54122@163.com
# @Description: 用户管理视图集，处理用户信息的CRUD操作和密码修改等功能

from fastapi import APIRouter, Depends
from fast_generic_api.generics import GenericAPIView,CustomViewSet
from fast_generic_api.core.response import CoreResponse


from commons.core.permission import DependPermisson

from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_system.models import UserModel
from application.app_system.serializers import (UsersSerializers,
                                                UsersCreateSerializers,
                                                UsersUpdateSerializers,
                                                UsersUpdatePasswordSerializers)
from application.app_system.services import UserService
router = APIRouter(tags=['用户管理'])
service = UserService()

class UserViewSet(CustomViewSet,
                  GenericAPIView):
    """用户视图集"""
    router = router
    prefix = "/users"
    queryset = UserModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = UsersSerializers           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'create':
            return UsersCreateSerializers
        elif self.action == 'update':
            return UsersUpdateSerializers
        return super().get_serializer_class()

    @staticmethod
    @router.post('/{uuid}/update_password/', summary='修改用户密码')
    async def update_user_password(uuid: str, password_data: UsersUpdatePasswordSerializers,
                                   current_user:UserModel=DependPermisson):
        """修改用户密码"""
        data = {'uuid':uuid,'current_user':current_user,
                'password_data':password_data}
        await service.handle_update_user_password(data)
        return CoreResponse(message="密码修改成功")