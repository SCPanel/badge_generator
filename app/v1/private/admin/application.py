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

    _secret_key = Password()
    _secret_key.generate(length=50)

    foundation["_id"] = await generate_id("foundations_db")
    foundation["metadata"] = {
        "approved_by": {
            "_id": "root",
            "name": "root",
            "date": "secret"
        },
        "is_default_password": True
    }

    foundation["project_details"] = {
        "secret_key": _secret_key.hash,
        "password": _temp_password.hash
    }
    foundation["expire"] = 1
    del foundation["processed"]

    _user_temp_password = Password() # dont forget send that shit via email
    _user_temp_password.generate()

    _user_secret_key = Password()
    _user_secret_key.generate(length=50)

    user = {
        "_id": await generate_id("users_db"),
        "email": foundation["email"],
        "password": _user_temp_password.hash,
        "secret_key": _user_secret_key.hash,
        "alias": foundation["_id"],
        "interrnal_alias": ""
    }
    foundation["owner"] = user["_id"]

    await delete_one("applications_db", {"_id": id})
    await insert_one("foundations_db", foundation)
    await insert_one("users_db", user)

    await send_message(
        email=foundation["email"],
        subject="Foundation confirmation!",
        content=f"""
        Hi {foundation["name"]}! <br>
        We are glad to let you know that your foundation named "{foundation["project_name"]}" has been confirmed by our admins.<br>
        To continue using our platform, please follow instructions below:<br>
        1. Go to our website and enter signin form<br>
        2. Use your email "{foundation["email"]}" and default password(you have to change he after login) " {_user_temp_password.hex} "<br>
        3. Enter this SECRET KEY(you will get a list of other keys which will be used while using platform) " {_user_secret_key.hex} " <br>
        4. Follow instructions and add your "{foundation["project_name"]}" Foundation details. <br>

        Password of your Foundation: " {_temp_password.hex} " <br>
        Secret key of your Foundation: " {_secret_key.hex} "
        """)

    return {"message": "ok."}