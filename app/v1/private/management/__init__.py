from fastapi import APIRouter

management_router = APIRouter(prefix="/management")


@management_router.post("/new_project")
async def create_new_project_event():

    pass