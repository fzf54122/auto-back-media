__all__ = ["api_router"]

from fastapi import APIRouter
from .LoginVietSet import router as login_router
from .UserViewSet import router as user_router



api_router = APIRouter()
api_router.include_router(login_router)
api_router.include_router(user_router)