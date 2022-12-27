from fastapi import APIRouter
from app.core.generate_config import generate_config
from app.core.schemas.foundation_schema import FoundationSchema

schema_router = APIRouter(prefix="/schema")

@schema_router.post("/new")
async def new_schema(foundation_schema: FoundationSchema):
    _foundation_schema = foundation_schema.dict()

    generate_config(
        **_foundation_schema,
        foundation=0
    )