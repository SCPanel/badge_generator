from fastapi import APIRouter
from app.v1.private.system.me import me_router

system_router = APIRouter(prefix="/system")
system_router.include_router(me_router)