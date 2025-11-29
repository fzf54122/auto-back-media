__all__ = ["api_router"]

from fastapi import APIRouter
from .RoleViewSet import router as role_router



api_router = APIRouter()
api_router.include_router(role_router)