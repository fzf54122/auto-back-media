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

@router.post('/upload/', status_code=201, summary='上传文件')
async def create(file: UploadFile = File(..., description="要上传的文件"),current_user=DependPermisson):
        """上传文件"""
        result = await service.upload_file(file, current_user.uuid)
        return CoreResponse(result)