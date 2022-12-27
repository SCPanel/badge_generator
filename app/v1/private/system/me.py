from fastapi import APIRouter

me_router = APIRouter(prefix="/me")

@me_router.get("/me")
async def get_me_event():
    return {}