from fastapi import APIRouter
from app.v1.private.admin.application import application_admin_router

admin_router = APIRouter(prefix="/admin")

admin_router.include_router(application_admin_router)