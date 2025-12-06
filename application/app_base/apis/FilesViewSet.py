from fastapi import APIRouter, File, UploadFile


from commons.core.response import AutoResponse
from commons.core.permission import DependPermisson
from commons.drf import CreateModelMixin,GenericViewSet
from application.app_base.services import FileService

router = APIRouter(tags=['上传文件'])
service = FileService()
class AuditLogViewSet(CreateModelMixin,
                      GenericViewSet):
    router = router
    prefix = "/upload"
    permissions = [DependPermisson]

    async def post(self, file: UploadFile = File(..., description="要上传的文件")):
        """上传文件"""
        
        result = await service.upload_file(file)
        return AutoResponse(result.body)