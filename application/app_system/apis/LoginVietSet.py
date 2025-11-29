
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from application.app_system.exceptions import TokenExpiredException, TokenInvalidException
from commons.core.cache import cache_manager
from commons.core.jwt import create_token_pair, verify_token
from commons.core.response import AutoResponse
from commons.drf import (CreateModelMixin,
                         GenericViewSet)
from application.app_system.schemas.LoginSchemas import CredentialsSchema, JWTOut
from application.app_system.services import UserService
from commons.drf.decorator import api_meta


router = APIRouter(tags=['登录接口'])
service = UserService()
security = HTTPBearer()


class LoginViewSet(CreateModelMixin,
                   GenericViewSet):
    router = router
    prefix = "/login"
    
    @api_meta(summary="用户登录")
    async def post(self, credentials: CredentialsSchema):
        """
        用户登录
        """
        # 验证用户凭据
        user = await service.authenticate(credentials)

        # 更新最后登录时间
        await service.update_last_login(user.id)

        # 生成token对
        access_token, refresh_token = create_token_pair(
            user_id=user.id,
            username=user.username,
            is_superuser=user.is_superuser
        )

        # 将refresh_token存入Redis（可选，用于token黑名单）
        await cache_manager.set(
            f"refresh_token:{user.id}",
            refresh_token,
            ttl=7 * 24 * 3600  # 7天
        )
        return AutoResponse(JWTOut(
            access_token=access_token,
            refresh_token=refresh_token,
            username=user.username,
            expires_in=30 * 60,# 30分钟
            user_uuid=user.uuid
        ))
    
    @router.post('/logout/', summary='用户退出')
    async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
        """用户退出登录"""
        token = credentials.credentials
        if token.lower().startswith("bearer "):
            token = token[7:]

        # 检查是否已在黑名单
        blacklisted = await cache_manager.get(f"blacklist_token:{token}")
        if blacklisted:
            raise TokenExpiredException
        try:
            payload = verify_token(token, token_type="access")

            # token加入黑名单
            await cache_manager.set(
                f"blacklist_token:{token}",
                "logged_out",
                ttl=30*60
            )

            # 删除 refresh_token
            await cache_manager.delete(f"refresh_token:{payload.user_id}")

            return AutoResponse(message="退出登录成功")

        except Exception as e:
            raise TokenInvalidException(detail=str(e))