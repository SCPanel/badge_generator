from uuid import uuid4
from app.core.database import find_one

async def generate_id(db:str="applications_db") -> str:
    _id = str(uuid4().hex)
    if await find_one(db, {"_id": _id}):
        return await generate_id(db)
    return _id