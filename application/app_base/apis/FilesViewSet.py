# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: FilesViewSet.py
# @Email: fzf54122@163.com
# @Description: 文件上传视图集，处理文件上传功能

from fastapi import APIRouter, File, UploadFile
from fast_generic_api.generics import CreateViewSet
from fast_generic_api.core.response import CoreResponse

from commons.core.permission import DependPermisson
from application.app_base.services import FileService

router = APIRouter(tags=['上传文件'])
service = FileService()
class FilesViewSet(CreateViewSet):
    router = router
    prefix = "/upload"
    permissions = [DependPermisson]

    async def create(self, file: UploadFile = File(..., description="要上传的文件")):
        """上传文件"""
        
        result = await service.upload_file(file)
        return CoreResponse(result.body)