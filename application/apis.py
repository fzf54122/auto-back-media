__all__ = ["api_router"]

from fastapi import APIRouter

from application.app_base.apis import api_router as base_router
from application.app_system.apis import api_router as system_router
api_router = APIRouter()

api_router.include_router(system_router)
api_router.include_router(base_router)
