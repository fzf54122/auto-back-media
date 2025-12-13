# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: UserService.py
# @Email: fzf54122@163.com
# @Description: UserService业务逻辑服务实现

import secrets
import string
from datetime import datetime
from typing import Optional

from fastapi.exceptions import HTTPException
from application.app_system.exceptions import (OldPasswordErrorException,
                                               UpdateOtherUserPasswordException,
                                               UserNotFoundException)
from commons.core.service import AutoService
from commons.core.password import get_password_hash, verify_password


from application.app_system.models.User import UserModel


class UserService(AutoService):
    def __init__(self):
        super().__init__(model=UserModel)

    async def get_by_email(self, email: str) -> UserModel | None:
        return await self.model.filter(email=email).first()

    async def get_by_username(self, username: str) -> UserModel | None:
        return await self.model.filter(username=username).first()

    async def create_user(self, obj_in) -> UserModel:
        obj_in.password = get_password_hash(password=obj_in.password)
        obj = await self.model.create(**obj_in.model_dump())
        return obj

    async def update_last_login(self, id: int) -> None:
        user = await self.model.get(id=id)
        user.last_login = datetime.now()
        await user.save()

    async def authenticate(self, credentials) -> Optional["UserModel"]:
        user : UserModel = await self.model.filter(username=credentials.username).first()
        if not user:
            raise HTTPException(status_code=400, detail="无效的用户名")
        verified = verify_password(credentials.password, user.password)
        if not verified:
            raise HTTPException(status_code=400, detail="密码错误!")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="用户已被禁用")
        return user


    async def reset_password(self, user_id: int) -> str:
        """重置用户密码，返回新密码"""
        user_obj : UserModel = await self.model.get(id=user_id)
        if user_obj.is_superuser:
            raise HTTPException(status_code=403, detail="不允许重置超级管理员密码")
        # 生成安全的随机密码
        new_password = self._generate_secure_password()
        user_obj.password = get_password_hash(password=new_password)
        await user_obj.save()
        return new_password

    def _generate_secure_password(self, length: int = 12) -> str:
        """生成安全的随机密码"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        return password


    async def handle_update_user_password(self,data):
        """处理修改密码"""
        uuid = data.get('uuid', None)
        password_data = data.get('password_data', None)
        current_user = data.get('current_user', None)
        # 检查权限（用户只能修改自己的密码，超级管理员可以修改任何用户的密码）
        if uuid != current_user.uuid and not current_user.is_superuser:
            raise UpdateOtherUserPasswordException
        # 获取用户
        user = await self.model.get(uuid=uuid)
        if not user:
            raise UserNotFoundException
        # 验证旧密码（非超级管理员需要验证）
        if not current_user.is_superuser or uuid == current_user.uuid:
            if not verify_password(password_data.old_password, user.password):
                raise OldPasswordErrorException
        user.password = get_password_hash(password_data.new_password)
        await user.save()
        return 