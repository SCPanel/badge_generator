from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.core.database import find_one
from jwt import PyJWTError, decode, encode
from datetime import datetime, timedelta

# Set up the signin_router and security scheme
signin_router = APIRouter(prefix="/signin")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")

# Define the request and response models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    password: str

# Set up the sign-in function
@signin_router.post("/signin", response_model=Token)
async def signin(user: User, secret_key: str):
    # Check if the user exists in the database
    user_record = await find_one("users_db", {"email": user.email})
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if the password is correct
    if not user.password == user_record["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if the secret key is correct
    if user_record["secret_key"] != secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect secret key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create the JWT token
    expires = datetime.utcnow() + timedelta(days=10)
    access_token = encode(
        {"sub": user_record["_id"], "exp": expires},
        secret_key,
        algorithm="HS256",
    )
    return {"access_token": access_token, "token_type": "bearer"}