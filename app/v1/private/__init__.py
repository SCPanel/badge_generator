from fastapi import APIRouter
from app.v1.private.admin import admin_router
from app.v1.private.foundation import foundation_router
from app.v1.private.system import system_router

private_router = APIRouter(prefix="/private")

private_router.include_router(admin_router)
private_router.include_router(foundation_router)
private_router.include_router(system_router)