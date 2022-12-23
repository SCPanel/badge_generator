from fastapi import APIRouter, File, UploadFile, Depends
from app.core.database import find_one
from app.core.error import raise_error_event
from app.core.authorisation import get_current_user
import os
from typing import Any, Dict

fs_router = APIRouter(prefix="/fs")

@fs_router.post("/{id}/upload/template")
async def upload_template_event(id: str, file: UploadFile = File(...), current_user: Dict[str, Any] = Depends(get_current_user)):
    if not await find_one("foundations_db", {"_id":id}):
        return await raise_error_event(404, "Foundation not found.")

    user_folder = f"templates/{id}/"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Get the file extension
    file_extension = os.path.splitext(file.filename)[1]

    # Check if the file extension is valid
    if file_extension.lower() not in [".png", ".jpg"]:
        return await raise_error_event(400, "Invalid file format. Only PNG and JPG are allowed.")

    # Change the file name to "template" + the file extension
    file_name = "template" + file_extension

    # Save the uploaded file to the user's folder
    file.file.seek(0)
    with open(f"{user_folder}/{file_name}", "wb") as f:
        f.write(file.file.read())

    return {"message": "file uploaded!"}