__all__ = ["api_router"]

from fastapi import APIRouter
from .RoleViewSet import router as role_router
from .MenuViewSet import router as menu_router
from .DeptsViewSet import router as depts_router
from .AuditLogViewSet import router as audit_log_router
from .FilesViewSet import router as files_router



api_router = APIRouter()
api_router.include_router(role_router)
api_router.include_router(menu_router)
api_router.include_router(depts_router)
api_router.include_router(audit_log_router)
api_router.include_router(files_router)