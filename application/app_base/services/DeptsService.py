# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: DeptsService.py
# @Email: fzf54122@163.com
# @Description: DeptsService业务逻辑服务实现
from application.app_base.models.Depts import DeptClosure
from application.app_base.serializers import DeptSerializers


class DeptsService:

    async def update_dept_closure(self, instance):
        parent_depts = await DeptClosure.filter(descendant=instance.parent_id)

        dept_closure_objs: list[DeptClosure] = []
        for parent_dept in parent_depts:
            dept_closure_objs.append(DeptClosure(ancestor=parent_dept.ancestor, descendant=instance.id,level=parent_dept.level + 1))
        dept_closure_objs.append(
            DeptClosure(ancestor=instance, descendant=instance, level=0)
        )
        await DeptClosure.bulk_create(dept_closure_objs)
