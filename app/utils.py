from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional

from pydantic import BaseModel
from .database import db_instance
from .config import settings

class SignIn(BaseModel):
  email: str
  password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_user(db, email: str) -> Optional[SignIn]:
    user = await db["users"].find_one({"email": email})
    if user:
        return SignIn(email=user['email'], password=user['password'])

async def authenticate_user(db, email: str, password: str) -> Optional[SignIn]:
    user = await get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

async def get_current_user(request: Request) -> Optional[SignIn]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    api_key = request.headers.get("Authorization")
    if not api_key or "Bearer " not in api_key:
        raise credentials_exception

    token = api_key.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(db_instance, email=email)
    if user is None:
        raise credentials_exception
    return user
