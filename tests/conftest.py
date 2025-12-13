"""测试配置和固件"""

import asyncio
import os
import subprocess
import sys
import tempfile
import warnings
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from commons.core.password import pwd_context  # 你的 Passlib CryptContext


os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("SWAGGER_UI_PASSWORD", "test_password")
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("APP_TITLE", "FastAPI Backend Template")
os.environ.setdefault("PROJECT_NAME", "FastAPI Backend Template")

try:  # pragma: no cover - fallback for environments without pytest-asyncio
    import pytest_asyncio  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pytest-asyncio>=0.23,<0.24"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        warnings.warn(
            "Installed pytest-asyncio dynamically to enable async fixtures."
        )
        import pytest_asyncio  # type: ignore  # noqa: F401
    except Exception as exc:  # pragma: no cover
        warnings.warn(
            f"pytest-asyncio is required for async tests but could not be installed: {exc}"
        )

if "pytest_asyncio" in sys.modules:  # pragma: no cover - plugin auto-registration helper
    pytest_plugins = ("pytest_asyncio",)

from application import app
from tortoise import Tortoise


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    # 设置测试环境变量
    import os

    os.environ["TESTING"] = "true"

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """设置测试数据库"""
    # 使用临时SQLite数据库
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()

    db_url = f"sqlite://{temp_db.name}"

    # 初始化Tortoise ORM
    test_config = {
        "connections": {"default": db_url},
        "apps": {
            "models": {
                "models": ["application.app_base.models",
                           "application.app_system.models",
                           "application.app_manage.models",  # 如果有模型
                           "aerich.models",  # Aerich 必须
                           ],
                "default_connection": "default",
            },
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai",
    }

    await Tortoise.init(config=test_config)

    # 生成数据库架构
    await Tortoise.generate_schemas()

    yield

    # 清理
    await Tortoise.close_connections()
    os.unlink(temp_db.name)


@pytest.fixture
def client():
    """同步测试客户端"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def clean_database():
    """清理数据库：自动遍历所有已注册模型"""
    try:
        for app_name, models in Tortoise.apps.items():
            for model_name, model_cls in models.items():
                try:
                    await model_cls.all().delete()
                except Exception:
                    # 忽略删除失败的情况，比如外键约束
                    pass
    except Exception:
        # 数据库未初始化时直接跳过
        pass


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """异步测试客户端"""
    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac



@pytest.fixture
async def admin_token(async_client: AsyncClient, clean_database) -> str:
    """获取管理员Token"""
    import os
    import uuid
    from application.app_system.serializers import UsersCreateSerializers
    from application.app_system.models import UserModel

    os.environ["TESTING"] = "true"

    # 使用随机用户名避免冲突
    unique_id = str(uuid.uuid4())[:8]
    raw_password = "Test123456"

    # 创建用户，密码先 hash
    admin_user = UsersCreateSerializers(
        username=f"admin_{unique_id}",
        email=f"admin_{unique_id}@test.com",
        password=pwd_context.hash(raw_password),  # ✅ hash
        is_superuser=True,
        is_active=True,
    )

    try:
        await UserModel.create(**admin_user.model_dump())
    except Exception as e:
        print(f"创建用户失败: {e}")
        raise

    # 登录获取 token
    import time
    for attempt in range(5):
        try:
            response = await async_client.post(
                "/api/auth/access_token/",
                json={"username": f"admin_{unique_id}", "password": raw_password},  # 发送明文密码
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("data", {}).get("access_token")
                if token:
                    return token
                else:
                    raise Exception(f"响应数据中没有 token: {data}")
            elif response.status_code == 429:  # 限流
                time.sleep(2)
                continue
            else:
                if attempt < 4:
                    time.sleep(1)
                    continue
                raise Exception(f"登录失败: {response.status_code} - {response.text}")
        except Exception as e:
            if attempt == 4:
                raise e
            time.sleep(1)

    raise Exception("所有登录尝试都失败了")


@pytest.fixture
async def normal_user_token(async_client: AsyncClient,clean_database) -> str:
    """获取普通用户Token"""
    import os
    import uuid

    from application.app_system.serializers import UsersCreateSerializers
    from application.app_system.models import UserModel

    # 确保测试环境变量设置
    os.environ["TESTING"] = "true"

    # 使用随机用户名避免冲突
    unique_id = str(uuid.uuid4())[:8]
    normal_user = UsersCreateSerializers(
        username=f"user_{unique_id}",
        email=f"user_{unique_id}@test.com",
        password="Test123456",
        is_superuser=False,
        is_active=True,
    )

    try:
        await UserModel.create(**normal_user.model_dump())
    except Exception as e:
        print(f"创建普通用户失败: {e}")
        raise

    # 登录获取token，加重试机制
    import time

    for attempt in range(5):
        try:
            response = await async_client.post(
                "/api/auth/access_token/",
                json={"username": f"user_{unique_id}", "password": "Test123456"},
            )

            if response.status_code == 200:
                data = response.json()
                token = data.get("data", {}).get("access_token")
                if token:
                    return token
                else:
                    print(f"普通用户响应数据中没有token: {data}")
                    raise Exception("Token not found in response")
            elif response.status_code == 429:  # 限流
                print(f"普通用户遇到限流，等待后重试 (尝试 {attempt + 1}/5)")
                time.sleep(2)
                continue
            else:
                print(f"普通用户登录失败: {response.status_code} - {response.text}")
                if attempt < 4:  # 不是最后一次尝试
                    time.sleep(1)
                    continue
                raise Exception(
                    f"普通用户登录失败: {response.status_code} - {response.text}"
                )
        except Exception as e:
            print(f"普通用户登录尝试 {attempt + 1} 失败: {e}")
            if attempt == 4:  # 最后一次尝试
                raise e
            time.sleep(1)

    raise Exception("所有普通用户登录尝试都失败了")


@pytest.fixture
def auth_headers(admin_token: str) -> dict:
    """认证头"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def normal_auth_headers(normal_user_token: str) -> dict:
    """普通用户认证头"""
    return {"Authorization": f"Bearer {normal_user_token}"}