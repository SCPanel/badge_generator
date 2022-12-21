from fastapi import APIRouter
from app.v1.public.authorisation.signup import signup_router

authorisation_router = APIRouter(prefix="/authorisation")

authorisation_router.include_router(signup_router)