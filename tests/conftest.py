# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: conftest.py
# @Email: fzf54122@163.com
# @Description: 描述文件功能

import asyncio
import pytest
from fastapi.testclient import TestClient
from application import create_app
from tortoise import Tortoise

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def app():
    """Create a FastAPI app instance for testing."""
    app = create_app()
    yield app

@pytest.fixture(scope="session")
def client(app):
    """Create a TestClient for testing endpoints."""
    with TestClient(app) as client:
        yield client