# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: File.py
# @Email: fzf54122@163.com
# @Description: File数据模型定义

from tortoise import fields

from application.models import CoreModel,table_prefix

class FileModel(CoreModel):


    file_id = fields.CharField(max_length=255, unique=True, description="文件ID", index=True)
    original_filename = fields.CharField(max_length=255, description="原始文件名")
    file_type = fields.CharField(max_length=50, description="文件类型")
    file_size = fields.BigIntField(null=True, description="文件大小(字节)")
    upload_user_id = fields.IntField(description="上传用户ID", index=True)
    file_path = fields.CharField(max_length=500, null=True, description="本地文件路径")
    
    class Meta:
            table = f"{table_prefix}file"