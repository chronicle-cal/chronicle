import os
import time
from typing import Any, Dict
import jwt

from fastapi import Security, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from app.models.user import User as UserModel
from app.db.session import get_async_db

security = HTTPBearer()

auth_responses: Dict[int | str, Dict[str, Any]] = {
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
}

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
AUTH_SECRET = os.getenv("AUTH_SECRET", "dev-secret")
AUTH_TOKEN_TTL = int(os.getenv("AUTH_TOKEN_TTL", "604800"))


def create_token(email: str) -> str:
    payload = {
        "sub": email,
        "iat": int(time.time()),
        "exp": int(time.time()) + AUTH_TOKEN_TTL,
    }
    return jwt.encode(payload, AUTH_SECRET, algorithm="HS256")


def verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, AUTH_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.PyJWTError:
        return None


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    return credentials.credentials


async def get_current_user(
    token: str = Depends(get_current_token), db: AsyncSession = Depends(get_async_db)
) -> UserModel:
    print("Getting current user with token:", token)
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.unique().scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return user
