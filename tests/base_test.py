# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: base_test.py
# @Email: fzf54122@163.com
# @Description: 通用测试基类模板

import pytest
from httpx import AsyncClient
from typing import List, Dict, Any, Type
from tortoise.models import Model


class BaseTestViewSet:
    """视图集测试基类模板"""
    
    # 子类必须重写以下属性
    model: Type[Model] = None  # 模型类
    mock_data: List[Dict[str, Any]] = None  # 测试数据
    api_prefix: str = ""  # API前缀，如"/api/menus"
    required_fields: Dict[str, Any] = {}  # 必填字段默认值
    
    # 可选配置
    field_mapping: Dict[str, Dict[str, Any]] = {}  # 字段映射，用于转换特殊值

    primary_update_field: str | None = "name"
    
    @pytest.fixture(autouse=True)
    async def setup(self, clean_database):
        """测试前置条件：清理数据库并初始化测试数据"""
        if not self.model or not self.mock_data:
            raise NotImplementedError("请在子类中设置model和mock_data属性")
        
        for item_data in self.mock_data:
            # 准备创建数据，过滤掉不需要的字段
            create_data = {}
            for key, value in item_data.items():
                # 跳过自动生成的字段
                if key in ["id", "uuid", "created_at", "updated_at"]:
                    continue
                
                # 应用字段映射转换
                if key in self.field_mapping:
                    mapped_value = self.field_mapping[key].get(value, value)
                    create_data[key] = mapped_value
                else:
                    create_data[key] = value
            
            # 添加必填字段默认值
            for field, default_value in self.required_fields.items():
                if field not in create_data:
                    create_data[field] = default_value
            
            # 处理None值，确保字符串字段不为None
            for field, value in create_data.items():
                if value is None:
                    # 检查模型字段是否存在且是字符串类型
                    if hasattr(self.model, field):
                        model_field = getattr(self.model, field)
                        if hasattr(model_field, 'field_type'):
                            if model_field.field_type in ['CHAR', 'TEXT']:
                                create_data[field] = ""
                    # 对于序列化器中需要字符串的字段，即使模型允许None，也设置为空字符串
                    elif field in ['desc']:
                        create_data[field] = ""
            
            await self.model.create(**create_data)
    
    @pytest.mark.asyncio
    async def test_get_list(self, async_client: AsyncClient, auth_headers):
        """测试获取列表"""
        if not self.api_prefix:
            raise NotImplementedError("请在子类中设置api_prefix属性")
        
        response = await async_client.get(
            f"{self.api_prefix}/list/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]) >= 1
    
    @pytest.mark.asyncio
    async def test_create(self, async_client: AsyncClient, auth_headers):
        """测试创建"""
        if not self.api_prefix:
            raise NotImplementedError("请在子类中设置api_prefix属性")
        
        # 使用第一个数据项作为模板创建新数据
        if not self.mock_data:
            raise NotImplementedError("请在子类中设置mock_data属性")
        
        template_data = self.mock_data[0]
        new_item = {}
        
        # 复制必要字段并修改主要字段以避免重复
        for key, value in template_data.items():
            if key == self.primary_update_field and value:
                new_item[key] = f"{value}_test"
            elif key not in ["id", "uuid", "created_at", "updated_at"]:
                # 应用字段映射转换
                if key in self.field_mapping:
                    mapped_value = self.field_mapping[key].get(value, value)
                    new_item[key] = mapped_value
                else:
                    new_item[key] = value
        
        # 添加必填字段默认值
        for field, default_value in self.required_fields.items():
            if field not in new_item:
                new_item[field] = default_value
        
        response = await async_client.post(
            f"{self.api_prefix}/create/",
            json=new_item,
            headers=auth_headers
        )
        
        print(f"Create API URL: {self.api_prefix}/create/")
        print(f"Create request data: {new_item}")
        print(f"Create response status: {response.status_code}")
        print(f"Create response content: {response.content}")
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            print(f"Create response JSON: {data}")
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            data = {}
        
        # 更详细的断言信息
        try:
            assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        except AssertionError as e:
            print(f"AssertionError on status code: {e}")
            raise
        
        try:
            assert data.get("code") == 200, f"Expected code 200, got {data.get('code')}"
        except AssertionError as e:
            print(f"AssertionError on code: {e}")
            raise
        
        # 验证创建的数据中包含至少一个我们设置的字段值
        found_match = False
        for key, value in new_item.items():
            if key in data.get("data", {}) and data["data"][key] == value:
                found_match = True
                break
        
        try:
            assert found_match, f"创建的数据未返回预期字段值。响应数据: {data.get('data')}, 请求数据: {new_item}"
        except AssertionError as e:
            print(f"AssertionError on field match: {e}")
            raise
    
    @pytest.mark.asyncio
    async def test_get_detail(self, async_client: AsyncClient, auth_headers):
        """测试获取详情"""
        if not self.api_prefix or not self.model:
            raise NotImplementedError("请在子类中设置api_prefix和model属性")
        
        # 获取第一个数据项的ID
        item = await self.model.all().first()
        if not item:
            pytest.fail("数据库中没有测试数据")
        
        response = await async_client.get(
            f"{self.api_prefix}/{item.uuid}/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["uuid"] == str(item.uuid)
    
    @pytest.mark.asyncio
    async def test_update(self, async_client: AsyncClient, auth_headers):
        """测试更新"""
        if not self.api_prefix or not self.model:
            raise NotImplementedError("请在子类中设置api_prefix和model属性")
        
        # 获取第一个数据项的ID
        item = await self.model.all().first()
        if not item:
            pytest.fail("数据库中没有测试数据")
        # 确保primary_update_field存在
        if not self.primary_update_field:
            pytest.skip("当前模型不支持 update 测试")
        update_data = {
            self.primary_update_field: f"{getattr(item, self.primary_update_field)}_updated"
        }
        
        response = await async_client.put(
            f"{self.api_prefix}/{item.uuid}/",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"][self.primary_update_field] == update_data[self.primary_update_field]
    
    @pytest.mark.asyncio
    async def test_delete(self, async_client: AsyncClient, auth_headers):
        """测试删除"""
        if not self.api_prefix or not self.model:
            raise NotImplementedError("请在子类中设置api_prefix和model属性")
        
        # 获取第一个数据项的ID
        item = await self.model.all().first()
        if not item:
            pytest.fail("数据库中没有测试数据")
        
        response = await async_client.delete(
            f"{self.api_prefix}/{item.uuid}/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        
        # 验证数据已被删除
        deleted_item = await self.model.all().filter(uuid=item.uuid).first()
        assert deleted_item is None