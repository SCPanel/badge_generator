from fastapi import APIRouter
# from management import management_router
from app.v1.private.admin import admin_router

private_router = APIRouter(prefix="/private")

# private_router.include_router(management_router)
private_router.include_router(admin_router)