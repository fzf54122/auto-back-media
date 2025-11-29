from commons.logger import logger


class RoleService:

    async def role_to_dict(self, obj):
            return {
                "uuid": obj.uuid,
                "name": obj.name,
                "desc": obj.desc,
                "is_active": obj.is_active,
                "menus": [menu.name for menu in await obj.menus.all()],
                "apis": [api.name for api in await obj.apis.all()],
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