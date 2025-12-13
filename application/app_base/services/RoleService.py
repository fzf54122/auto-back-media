# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: RoleService.py
# @Email: fzf54122@163.com
# @Description: RoleService业务逻辑服务实现


class RoleService:

    async def role_to_dict(self, obj):
            return {
                "uuid": obj.uuid,
                "name": obj.name,
                "desc": obj.desc,
                "is_active": obj.is_active,
                "menus": [menu.id for menu in await obj.menus.all()],
                "apis": [api.id for api in await obj.apis.all()],
                "created_at": obj.created_at,
                "updated_at": obj.updated_at,
            }

    async def handle_get_list(self, qs):
        # qs 是 QuerySet，需要先 await 执行
        objs = await qs  # ⚠️ 一定要 await
        result = []
        for obj in objs:
            result.append(await self.role_to_dict(obj))
        return result