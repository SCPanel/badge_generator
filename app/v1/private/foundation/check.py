import json
from os import listdir, path
from io import BytesIO

from fastapi.responses import Response
from fastapi import APIRouter
from app.core.database import find_one
from app.core.error import raise_error_event
from app.core.generator import Generator

check_router = APIRouter(prefix="/check")

async def check_fs(id):
    important_files = ["template_schema.json", "template.png", "avatar.png", "font.ttf"]

    root_folder = f"templates/{id}"

    if not path.exists(root_folder):
        return await raise_error_event(404, "Foundation folder not found, please upload material.")

    files = listdir(root_folder)
    _missed_files = []

    for file in important_files:
        if file not in files: 
            _missed_files.append(file.split(".")[0])
    
    if _missed_files:
        return await raise_error_event(404, f"You must upload: {', '.join(_missed_files)}")
        

@check_router.get("/{id}")
async def check_foundation_event(id: str):
    _foundation = await find_one("foundations_db", {"_id": id})
    if not _foundation:
        return await raise_error_event(404, "Foundation not found.")

    await check_fs(id)
    
    # TODO: Improve user exist check

    return {"message": "Foundation ready to generation."}


@check_router.get("/{id}/print")
async def check_foundation_print_event(id: str):
    _foundation = await find_one("foundations_db", {"_id": id})
    if not _foundation:
        return await raise_error_event(404, "Foundation not found.")
    
    await check_fs(id)

    _config = open(f"templates/{id}/template_schema.json")
    _config = json.load(_config)
    generated = await Generator.from_json(_config)

    image_bytes = BytesIO()
    
    # Save the PIL image to the BytesIO object
    generated.save(image_bytes, format='png')

    # Seek to the beginning of the file-like object
    image_bytes.seek(0)

    return Response(content=image_bytes.read(), media_type='image/png')