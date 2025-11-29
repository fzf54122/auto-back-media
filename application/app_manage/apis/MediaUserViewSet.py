from fastapi import APIRouter, Depends


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson, get_current_username
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_manage.models import MediaUserModel
from application.app_manage.schemas import (MediaUserSchemas,
                                            MediaUserCreateSchemas,
                                            MediaUserUpdateSchemas,)

router = APIRouter(tags=['媒体账号管理'])

class MediaUserViewSet(CustomViewSet,
                  GenericViewSet):
    """媒体账号管理视图集"""
    router = router
    prefix = "/media_users"
    model = MediaUserModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = MediaUserSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return MediaUserCreateSchemas
        elif self.action == 'update':
            return MediaUserUpdateSchemas
        return super().get_serializer_class()