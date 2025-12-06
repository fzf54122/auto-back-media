
import asyncio
from uuid import uuid4
from datetime import datetime
from tortoise import fields, models
from conf import settings
# 数据库表名前缀
table_prefix = getattr(settings, 'TABLE_PREFIX', '')



class CoreModel(models.Model):
    """核心标准抽象模型，可直接继承使用"""

    id = fields.BigIntField(
                            primary_key=True, 
                            db_index=True,
                            auto_increment=True)
    uuid = fields.UUIDField(
                            default=uuid4,
                            unique=True, 
                            db_index=True)
    
    description = fields.CharField(
                            max_length=300,
                            default="",
                            description="描述")

    created_at = fields.DatetimeField(
                            auto_now_add=True, 
                            description="创建时间",
                            db_index=True)
    updated_at = fields.DatetimeField(
                            auto_now=True,
                            description="更新时间",
                            db_index=True)
    
    is_active = fields.BooleanField(
                            default=True, 
                            description="是否启用",
                            db_index=True)
    is_deleted = fields.BooleanField(
                            default=False, 
                            description="是否删除",
                            db_index=True)

    async def to_dict(self, m2m: bool = False, exclude_fields: list[str] | None = None):

        if exclude_fields is None:
            exclude_fields = []

        d = {}
        for field in self._meta.db_fields:
            if field not in exclude_fields:
                value = getattr(self, field)
                if isinstance(value, datetime):
                    value = value.strftime(settings.DATETIME_FORMAT)
                d[field] = value

        if m2m:
            tasks = [
                self.__fetch_m2m_field(field, exclude_fields)
                for field in self._meta.m2m_fields
                if field not in exclude_fields
            ]
            results = await asyncio.gather(*tasks)
            for field, values in results:
                d[field] = values

        return d

    async def __fetch_m2m_field(self, field, exclude_fields):
        values = await getattr(self, field).all().values()
        formatted_values = []

        for value in values:
            formatted_value = {}
            for k, v in value.items():
                if k not in exclude_fields:
                    if isinstance(v, datetime):
                        formatted_value[k] = v.strftime(settings.DATETIME_FORMAT)
                    else:
                        formatted_value[k] = v
            formatted_values.append(formatted_value)

        return field, formatted_values

    async def from_dict(self, data: dict, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []

        update_data = {}
        m2m_data = {}

        # 普通字段和 M2M 区分
        for field, value in data.items():
            if field in exclude_fields:
                continue
            if field in self._meta.db_fields:
                update_data[field] = value
            elif field in self._meta.m2m_fields:
                m2m_data[field] = value

        # 更新普通字段
        if update_data:
            await self.update_from_dict(update_data)
            await self.save()

        # 更新 M2M 字段
        for field in data:
            if field in self._meta.m2m_fields and field not in exclude_fields:
                manager = getattr(self, field)
                await manager.clear()
                m2m_model = self._meta.fields_map[field].related_model
                ids = data[field]
                instances = await m2m_model.filter(id__in=ids)
                await manager.add(*instances)

        return self

    class Meta:
        abstract = True
        verbose_name = '核心模型'

    def delete(self, using=None, soft_delete=True, *args, **kwargs):
        """
        重写删除方法,直接开启软删除
        """
        if soft_delete:
            self.is_deleted = True
            self.save(using=using)
            # 级联软删除关联对象
            for related_object in self._meta.related_objects:
                # 判断是否是级联删除, set_null, protected, do_nothing 在软删除均不需处理
                on_delete = related_object.on_delete
                print(f'soft delete obj {related_object} {on_delete}')
                if not on_delete or on_delete != models.CASCADE:
                    continue
                related_model = getattr(self, related_object.get_accessor_name())

                # 处理一对多和多对多的关联对象
                if related_object.one_to_many or related_object.many_to_many:
                    related_objects = related_model.all()
                elif related_object.one_to_one:
                    related_objects = [related_model]
                else:
                    continue

                for obj in related_objects:
                    obj.delete(soft_delete=True)
        else:
            super().delete(using=using, *args, **kwargs)