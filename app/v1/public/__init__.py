from fastapi import APIRouter
from app.v1.public.authorisation import authorisation_router

public_router = APIRouter(prefix="/public")

public_router.include_router(authorisation_router)
