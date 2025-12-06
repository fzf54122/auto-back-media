from uuid import UUID
from pydantic import Field
from commons.core.schemas import AutoSchemas


class DeptsSchemas(AutoSchemas):
    """部门管理序列化器"""
    uuid:UUID = Field(..., description="部门ID")
    name: str = Field(..., description="部门名称", example="研发中心")
    desc: str = Field("", description="备注", example="研发中心")
    order: int = Field(0, description="排序")
    parent_id: int = Field(0, description="父部门ID")

class DeptsSchemasCreate(DeptsSchemas):
    """部门管理创建序列化器"""
    pass

class DeptsSchemasUpdate(DeptsSchemas):
    """部门管理更新序列化器"""
    uuid: UUID
