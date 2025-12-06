
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from application.app_system.exceptions import TokenExpiredException, TokenInvalidException, UserNotFoundException
from application.app_system.schemas import UsersSchemas
from application.app_system.models import UserModel
from commons.core.cache import cache_manager
from commons.core.jwt import create_token_pair, verify_token
from commons.core.response import AutoResponse
from commons.drf import (CreateModelMixin,
                         GenericViewSet)
from application.app_system.schemas.LoginSchemas import CredentialsSchema, JWTOut, RefreshTokenRequest, TokenRefreshOut
from application.app_system.services import UserService
from commons.drf.decorator import api_meta
from commons.core.limit import apply_rate_limit

router = APIRouter(tags=['登录接口'])
service = UserService()
security = HTTPBearer()



class LoginViewSet(CreateModelMixin,
                   GenericViewSet):
    router = router
    prefix = "/login"

    @staticmethod
    @api_meta(summary="用户登录")
    @apply_rate_limit(rate="5/minute")
    async def post( request: Request,credentials: CredentialsSchema):
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
    async def logout(self, request: Request,credentials: HTTPAuthorizationCredentials = Depends(security)):
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
            raise TokenInvalidException
        

    @staticmethod
    @apply_rate_limit(rate="5/minute")
    @router.post('/refresh/', summary='刷新Token')
    async def refresh_token(request: Request, refresh_token_request: RefreshTokenRequest):
        """
        使用refresh_token刷新获取新的access_token和refresh_token
        """
        refresh_token = refresh_token_request.refresh_token
        
        try:
            # 验证refresh_token
            payload = verify_token(refresh_token, token_type="refresh")
            
            # 检查refresh_token是否在Redis中存在且匹配
            stored_refresh_token = await cache_manager.get(f"refresh_token:{payload.user_id}")
            if not stored_refresh_token or stored_refresh_token != refresh_token:
                raise TokenInvalidException
            
            # 获取用户信息
            user = await UserModel.filter(id=payload.user_id).first()
            if not user:
                raise TokenInvalidException
            
            # 生成新的token对
            new_access_token, new_refresh_token = create_token_pair(
                user_id=user.id,
                username=user.username,
                is_superuser=user.is_superuser
            )
            
            # 更新Redis中的refresh_token
            await cache_manager.set(
                f"refresh_token:{user.id}",
                new_refresh_token,
                ttl=7 * 24 * 3600  # 7天
            )
            
            return AutoResponse(TokenRefreshOut(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type="bearer",
                expires_in=30 * 60  # 30分钟
            ))
            
        except Exception as e:
            if "expired" in str(e).lower():
                raise TokenExpiredException
            raise TokenInvalidException

    @staticmethod
    @router.get('/get_user_info/', summary='获取当前用户信息')
    async def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
            """
            根据当前token获取用户详细信息
            """
            token = credentials.credentials
            if token.lower().startswith("bearer "):
                token = token[7:]
                
            # 检查token是否在黑名单
            blacklisted = await cache_manager.get(f"blacklist_token:{token}")
            if blacklisted:
                raise TokenExpiredException
            
            try:
                # 验证access token
                payload = verify_token(token, token_type="access")
                
                # 根据用户ID获取用户信息
                user = await UserModel.filter(id=payload.user_id).first()
                if not user:
                    raise UserNotFoundException
                    
                # 将用户信息转换为schema格式返回
                user_data = UsersSchemas.model_validate(user)
                
                return AutoResponse(data=user_data)
                
            except Exception as e:
                if "expired" in str(e).lower():
                    raise TokenExpiredException
                raise TokenInvalidException