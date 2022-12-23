from typing import Any, Dict
import jwt
from datetime import datetime
from fastapi import HTTPException, Depends
from app.core.database import find_one
# from fastapi_security import api_key
from app.core.config import settings

async def verify_api_key(api_key: str):
    try:
        payload = jwt.decode(api_key, settings.SECRET_KEY, algorithms=["HS256"])
        exp = payload.get("exp")
        if exp and exp < datetime.utcnow().timestamp():
            return None
        user_id = payload.get("user_id")
        if not user_id:
            return None
        # Check if the user with the given ID exists in the database
        user = await find_one("users_db", {"_id": user_id})
        if not user:
            return None
        return payload
    except jwt.InvalidTokenError:
        return None

async def get_current_user(payload: Dict[str, Any] = Depends(verify_api_key)):
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return payload