from fastapi import APIRouter
from app.v1.private.foundation.fs import fs_router
from app.v1.private.foundation.management import management_router
from app.v1.private.foundation.schema import schema_router
from app.v1.private.foundation.check import check_router

foundation_router = APIRouter(prefix="/foundation")
foundation_router.include_router(fs_router)
foundation_router.include_router(management_router)
foundation_router.include_router(schema_router)
foundation_router.include_router(check_router)