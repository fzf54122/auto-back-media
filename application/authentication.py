# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: authentication.py
# @Email: fzf54122@163.com
# @Description: 认证相关功能实现
import re

from fastapi import Depends,Request,HTTPException,status

from application.app_system.models import UserModel
from commons.core.permission import AuthControl


async def check_permission(request: Request, current_user: UserModel = Depends(AuthControl.is_authed)):
    if current_user.is_superuser:
        return

    method = request.method
    path = request.url.path
    roles = await current_user.roles.all()

    if not roles:
        raise HTTPException(status_code=403, detail="The user is not bound to a role")

    apis = [await role.apis.all() for role in roles]
    permission_apis = [(api.method, api.path) for api in sum(apis, [])]

    for perm_method, perm_path in permission_apis:
        if method == perm_method:
            pattern = re.sub(r"\{[^}]+\}", r"[^/]+", perm_path)
            pattern = f"^{pattern}$"
            if re.match(pattern, path):
                return

    raise HTTPException(status_code=403, detail=f"Permission denied method:{method} path:{path}")
