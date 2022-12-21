from fastapi import APIRouter
from os import getenv
from dotenv import load_dotenv
from app.core.schemas.foundation_application import FoundationApplication
from app.core.database import find_one, insert_one
from app.core.email.mail import send_message
from app.core.error import raise_error_event
from app.core.generate_id import generate_id

load_dotenv()

signup_router = APIRouter(prefix="/signup")


@signup_router.post("/")
async def new_foundation_application_event(application: FoundationApplication):
    if await find_one("applications_db", {"email": application.email}):
        return await raise_error_event(400, "Email already used")
    
    _application = application.dict()
    
    await send_message(
        email=application.email,
        subject="New Foundation Application on SCPanel Badge Generator",
        content=f"""
        Hi, {application.name}! <br>
        You applied to create a foundation on our SCP Platform, we will contact you later for letting you know about the application status! <br>
        Project name: {application.project_name} <br>
        Description: {application.description}
        """)

    _application["_id"] = await generate_id()
    _application["processed"] = False

    await insert_one("applications_db", _application)

    await send_message(
        email=getenv("applications_team_email"),
        subject="New Foundation Application",
        content=f"""
        Id: {_application["_id"]} <br>
        Processed: { _application["processed"]} <br>
        Name: {application.name} <br>
        Email: {application.email} <br>
        Project name: {application.project_name} <br>
        Description: {application.description} <br>
        To manage this application please go to our A.SCP and do what you need.
        """
    )

    return {"message": "ok"}