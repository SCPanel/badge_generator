from fastapi import APIRouter
from app.core.database import find_one
from app.core.error import raise_error_event
from app.core.generate_config import generate_config
from app.core.schemas.foundation_schema import FoundationSchema

schema_router = APIRouter(prefix="/schema")

@schema_router.post("/{id}/new")
async def new_schema(foundation_schema: FoundationSchema, id: str):
    _foundation = await find_one("foundations_db", {"_id": id})
    if not _foundation:
        return await raise_error_event(404, "Foundation not found.")

    _foundation_schema = foundation_schema.dict()

    config = generate_config(
        **_foundation_schema,
        foundation=_foundation
    )

    if not config:
        return await raise_error_event(500, "Something went wrong, try again later.")
    
    return config