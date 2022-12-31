from shutil import rmtree
from fastapi import APIRouter
from app.core.database import find_one, delete_one, delete
from app.core.error import raise_error_event

management_router = APIRouter(prefix="/management")

@management_router.delete("/{id}/delete")
async def delete_foundation_event(id: str):
    if not await find_one("foundations_db", {"_id": id}):
        return await raise_error_event(404, "Foundation not found.")
    
    await delete_one("foundations_db", {"_id": id})
    await delete("users_db", {"alias": id})

    rmtree(f"templates/{id}")	

    return {"message": "ok."}