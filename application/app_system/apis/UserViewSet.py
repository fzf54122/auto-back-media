from fastapi import APIRouter, Depends


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson, get_current_username
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_system.models import UserModel
from application.app_system.schemas import (UsersSchemas,
                                            UsersCreateSchemas,
                                            UsersUpdateSchemas,
                                            UsersUpdatePasswordSchemas)
from application.app_system.services import UserService
router = APIRouter(tags=['用户管理'])
service = UserService()

class UserViewSet(CustomViewSet,
                  GenericViewSet):
    """用户视图集"""
    router = router
    prefix = "/users"
    model = UserModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = UsersSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return UsersCreateSchemas
        elif self.action == 'update':
            return UsersUpdateSchemas
        return super().get_serializer_class()
    
    @router.post('/{uuid}/update_password/', summary='修改用户密码')
    async def update_user_password(self, uuid: str, password_data: UsersUpdatePasswordSchemas,
                                   current_user=Depends(get_current_username)):
        """修改用户密码"""
        data = {'uuid':uuid,'current_user':current_user,
                'password_data':password_data}
        service.handle_update_user_password(data)
        return AutoResponse(message="密码修改成功")