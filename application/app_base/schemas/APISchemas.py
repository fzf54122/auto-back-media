from pydantic import BaseModel, Field

from ..enums import MethodType


class APISchemas(BaseModel):
    path: str = Field(..., description="API路径", json_schema_extra={'example': "/api/v1/user/list"})
    summary: str = Field("", description="API简介", json_schema_extra={'example': "查看用户列表"})
    method: MethodType = Field(..., description="API方法", json_schema_extra={'example': "GET"})
    tags: str = Field(..., description="API标签", json_schema_extra={'example': "User"})


class APICreateSchemas(APISchemas): ...


class APIUpdateSchemas(APISchemas):
    id: int
