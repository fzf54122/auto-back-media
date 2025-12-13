# -*- coding: utf-8 -*-
# @Time    : 2025-12-13 11:57:20
# @Author  : fzf54122
# @FileName: LoginViewSet.py
# @Email: fzf54122@163.com
# @Description: 用户认证相关视图集，处理登录、退出、刷新Token和获取用户信息等功能

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fast_generic_api.core.response import CoreResponse
from fast_generic_api.decorator import api_meta

from application.app_system.exceptions import TokenExpiredException, TokenInvalidException, UserNotFoundException
from application.app_system.serializers import UsersSerializers
from application.app_system.models import UserModel
from commons.core.cache import cache_manager
from commons.core.jwt import create_token_pair, verify_token
from application.app_system.serializers.LoginSerializers import CredentialsSerializers, JWTOut, RefreshTokenRequest, TokenRefreshOut
from application.app_system.services import UserService

from commons.core.limit import apply_rate_limit

router = APIRouter(tags=['登录接口'])
service = UserService()
security = HTTPBearer()



class LoginViewSet:
    @staticmethod
    @api_meta(summary="用户登录")
    @router.post('/auth/login/', summary='用户登录')
    async def login(request: Request, credentials: CredentialsSerializers):
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
        return CoreResponse(JWTOut(
            access_token=access_token,
            refresh_token=refresh_token,
            username=user.username,
            expires_in=30 * 60,# 30分钟
            user_uuid=user.uuid
        ))

    @staticmethod
    @router.post('/auth/logout/', summary='用户退出')
    async def logout(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
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
                ttl=60 * 60 * 24  # 24小时
            )

            # 删除 refresh_token
            await cache_manager.delete(f"refresh_token:{payload.user_id}")

            return CoreResponse(message="退出登录成功")

        except Exception as e:
            raise TokenInvalidException
        
    @staticmethod
    @apply_rate_limit(rate="5/minute")
    @router.post('/auth/refresh/', summary='刷新Token')
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
            
            return CoreResponse(TokenRefreshOut(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type="Bearer",
                expires_in=60 * 60 * 24  # 24小时
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
                user_data = UsersSerializers.model_validate(user)
                
                return CoreResponse(data=user_data)
                
            except Exception as e:
                if "expired" in str(e).lower():
                    raise TokenExpiredException
                raise TokenInvalidException