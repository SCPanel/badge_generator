from fastapi import APIRouter
from app.core.database import (
    find_one,
    insert_one,
    delete_one
)
from app.core.secret import Password
from app.core.error import raise_error_event
from app.core.generate_id import generate_id
from app.core.email.mail import send_message


application_admin_router = APIRouter(prefix="/application")


@application_admin_router.get("/{id}/approve")
async def approve_application_event(id: str):
    application = await find_one("applications_db", {"_id": id})

    if not application:
        return await raise_error_event(404, "Application not found.")
    
    foundation = application

    _temp_password = Password() # dont forget send that shit via email
    _temp_password.generate()

    foundation["_id"] = await generate_id("foundations_db")
    foundation["metadata"] = {
        "approved_by": {
            "_id": "root",
            "name": "root",
            "date": "secret"
        },
        "is_default_password": True
    }
    foundation["password"] = _temp_password.hash
    foundation["project_details"] = {}
    foundation["expire"] = 1

    await delete_one("applications_db", {"_id": id})
    await insert_one("foundations_db", foundation)

    await send_message(
        email=foundation["email"],
        subject="Foundation confirmation!",
        content=f"""
        Hi {foundation["name"]}! <br>
        We are glad to let you know that your foundation named "{foundation["project_name"]}" has been confirmed by our admins.<br>
        To continue using our platform, please follow instructions below:<br>
        1. Go to our website and enter signin form<br>
        2. Use your email "{foundation["email"]}" and default password(you have to change he after login) "{_temp_password.hex}"<br>
        3. Enter this SECRET KEY(you will get a list of other keys which will be used while using platform) "SECRET_KEY" <br>
        4. Follow instructions and add your "{foundation["project_name"]}" Foundation details.
        """)

    return {"message": "ok."}