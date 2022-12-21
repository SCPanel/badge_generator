from fastapi import APIRouter
from app.core.database import (
    find_one,
    insert_one,
    delete_one
)
from app.core.secret import (
    generate_password,
    password_hash
)
from app.core.error import raise_error_event
from app.core.generate_id import generate_id


application_admin_router = APIRouter(prefix="/application")


@application_admin_router.get("/{id}/approve")
async def approve_application_event(id: str):
    application = await find_one("applications_db", {"_id": id})

    if not application:
        return await raise_error_event(404, "Application not found.")
    
    foundation = application
    _temp_password = await generate_password() # dont forget send that shit via email
    _hashed_temp_password = await password_hash(_temp_password)

    foundation["_id"] = await generate_id("foundations_db")
    foundation["metadata"] = {
        "approved_by": {
            "_id": "root",
            "name": "root",
            "date": "secret"
        },
        "is_default_password": True
    }
    foundation["password"] = _hashed_temp_password
    foundation["project_details"]
