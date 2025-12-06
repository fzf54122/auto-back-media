

from application.app_base.models.Depts import DeptClosure
from application.app_base.schemas import DeptsSchemas


class DeptsService:
    
    async def update_dept_closure(self, instance:DeptsSchemas):
        parent_depts = await DeptClosure.filter(descendant=instance.parent_id)
        
        dept_closure_objs: list[DeptClosure] = []
        for parent_dept in parent_depts:
            dept_closure_objs.append(DeptClosure(ancestor=parent_dept.ancestor, descendant=instance.id,level=parent_dept.level + 1))
        dept_closure_objs.append(
            DeptClosure(ancestor=instance.id, descendant=instance.id, level=0)
        )
        await DeptClosure.bulk_create(dept_closure_objs)
        