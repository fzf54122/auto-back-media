from fastapi import APIRouter


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson
from commons.drf import CustomViewSet,GenericViewSet
from application.pagination import LimitOffsetMaxDefaultPagination
from application.app_base.models import DeptsModel,DeptClosure
from application.app_base.schemas import (DeptsSchemas,
                                          DeptsSchemasCreate,
                                          DeptsSchemasUpdate)
from application.app_base.services import DeptsService

service = DeptsService()

router = APIRouter(tags=['部门管理'])
class DeptsViewSet(CustomViewSet,
                  GenericViewSet):
    """部门管理视图集"""
    router = router
    prefix = "/depts"
    model = DeptsModel
    filter_fields = []
    ordering = ["-created_at"]
    loop_uuid_field = "uuid"
    serializer_class = DeptsSchemas           # ✅ 列表/详情默认序列化器
    pagination_class = LimitOffsetMaxDefaultPagination
    filter_class = None
    permissions = [DependPermisson]

    def get_serializer_class(self):
        if self.action == 'post':
            return DeptsSchemasCreate
        elif self.action == 'update':
            return DeptsSchemasUpdate
        return super().get_serializer_class()
    

    async def list(self,request, data=...):
        pass
    

    async def create(self, request, data=DeptsSchemasCreate):
        if data.parent_id != 0:
            await self.model.get_or_none(id=data.parent_id)
        new_instance = await self.model.create(**data.model_dump())
        # 创建部门关系
        await service.update_dept_closure(new_instance)
        return AutoResponse(data=new_instance)



    async def update(self, request, data=DeptsSchemasUpdate):
        instance = await self.model.get_or_none(uuid=request.path_params["uuid"])
        if not instance:
            return AutoResponse(code=400, status="error", msg="部门不存在")
        await instance.update(**data.model_dump(exclude_unset=True))
        # 更新部门关系
        await service.update_dept_closure(instance)
        return AutoResponse(data=instance)
    

    async def destroy(self, request):
        """逻辑删除部门"""
        instance = await self.model.get_or_none(uuid=request.path_params["uuid"])
        if not instance:
            return AutoResponse(code=400, status="error", msg="部门不存在")
        await instance.update(is_deleted=True)
        await DeptClosure.filter(descendant=instance.id).update(is_deleted=True)
        return AutoResponse("部门删除成功")
