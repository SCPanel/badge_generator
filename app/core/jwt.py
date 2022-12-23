import jwt
from app.core.config import settings

def generate_jwt(data: dict) -> str:
    return jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode("utf-8")

def decode_jwt(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None