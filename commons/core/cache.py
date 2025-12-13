# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: cache.py
# @Email: fzf54122@163.com
# @Description: 缓存功能实现
import asyncio
import json
from collections.abc import Callable
from functools import wraps
from typing import Any

import redis.asyncio as redis

from conf import settings
from commons.logger import logger



class CacheManager:
    """Redis缓存管理器（稳定版）"""

    def __init__(self):
        self.redis: redis.Redis | None = None
        self._lock = asyncio.Lock()

    async def connect(self):
        """连接 Redis（带并发保护 + 超时）"""
        if self.redis:
            return self.redis

        async with self._lock:
            if self.redis:
                return self.redis

            try:
                self.redis = redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    max_connections=20,

                    # 🔥 必须
                    socket_timeout=3,
                    socket_connect_timeout=3,

                    # 🚫 async 场景不推荐
                    retry_on_timeout=False,
                )

                # ping 也要保护
                await asyncio.wait_for(self.redis.ping(), timeout=3)
                logger.info("Redis 连接成功")

            except Exception as e:
                logger.warning(f"Redis 连接失败: {e}")
                self.redis = None

        return self.redis

    async def disconnect(self):
        if self.redis:
            await self.redis.aclose()
            self.redis = None
            logger.info("Redis 已断开")

    # ---------- 安全操作封装 ----------

    async def get(self, key: str) -> Any | None:
        if not self.redis:
            return None

        try:
            data = await asyncio.wait_for(self.redis.get(key), timeout=2)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get 失败 key={key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        if not self.redis:
            return False

        try:
            ttl = ttl or settings.CACHE_TTL
            data = json.dumps(value, ensure_ascii=False, default=str)

            await asyncio.wait_for(
                self.redis.setex(key, ttl, data),
                timeout=2
            )
            return True

        except Exception as e:
            logger.error(f"Redis set 失败 key={key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        if not self.redis:
            return False

        try:
            result = await asyncio.wait_for(
                self.redis.delete(key),
                timeout=2
            )
            return bool(result)
        except Exception as e:
            logger.error(f"Redis delete 失败 key={key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        if not self.redis:
            return False

        try:
            result = await asyncio.wait_for(
                self.redis.exists(key),
                timeout=2
            )
            return bool(result)
        except Exception as e:
            logger.error(f"Redis exists 失败 key={key}: {e}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """安全删除（避免 KEYS 阻塞）"""
        if not self.redis:
            return 0

        count = 0
        try:
            async for key in self.redis.scan_iter(match=pattern, count=100):
                count += await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Redis 批量删除失败 pattern={pattern}: {e}")

        return count

    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        parts = [prefix]
        parts.extend(map(str, args))
        for k, v in sorted(kwargs.items()):
            parts.append(f"{k}:{v}")
        return ":".join(parts)

# 全局缓存管理器实例
cache_manager = CacheManager()


def cached(prefix: str, ttl: int | None = None, key_func: Callable | None = None):
    """缓存装饰器

    Args:
        prefix: 缓存键前缀
        ttl: 过期时间（秒）
        key_func: 自定义键生成函数
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = cache_manager.cache_key(prefix, *args, **kwargs)

            # 尝试从缓存获取
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"缓存命中: {cache_key}")
                return cached_result

            # 执行原函数
            result = await func(*args, **kwargs)

            # 设置缓存
            if result is not None:
                await cache_manager.set(cache_key, result, ttl)
                logger.debug(f"缓存设置: {cache_key}")

            return result

        return wrapper

    return decorator


# 缓存清理工具函数
async def clear_user_cache(user_id: int):
    """清除用户相关缓存"""
    patterns = [
        f"user:{user_id}:*",
        f"userinfo:{user_id}",
        f"user_roles:{user_id}",
        f"user_permissions:{user_id}",
    ]

    total_cleared = 0
    for pattern in patterns:
        cleared = await cache_manager.clear_pattern(pattern)
        total_cleared += cleared

    logger.info(f"清除用户{user_id}相关缓存，共{total_cleared}个键")
    return total_cleared


async def clear_role_cache(role_id: int):
    """清除角色相关缓存"""
    patterns = [
        f"role:{role_id}:*",
        f"role_permissions:{role_id}",
        f"role_menus:{role_id}",
    ]

    total_cleared = 0
    for pattern in patterns:
        cleared = await cache_manager.clear_pattern(pattern)
        total_cleared += cleared

    logger.info(f"清除角色{role_id}相关缓存，共{total_cleared}个键")
    return total_cleared
