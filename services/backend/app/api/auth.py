import os
import time

from fastapi import APIRouter, Depends, Header, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.db.session import get_async_db
from app.models.user import User as UserModel
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

router = APIRouter()

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


def get_bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    return authorization.split(" ", 1)[1].strip()


async def get_current_user(
    token: str = Depends(get_bearer_token), db: AsyncSession = Depends(get_async_db)
) -> UserModel:
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.unique().scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_async_db)):
    email = payload.email.lower()
    existing = await db.execute(select(UserModel).where(UserModel.email == email))
    if existing.unique().scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    user = UserModel(email=email, password_hash=pwd_context.hash(payload.password))
    db.add(user)
    await db.commit()
    return TokenResponse(access_token=create_token(email))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    email = payload.email.lower()
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.unique().scalar_one_or_none()
    if user is None or not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return TokenResponse(access_token=create_token(email))


@router.post("/logout")
def logout():
    return {"message": "logged out"}


@router.get("/me")
async def me(
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    return {"authenticated": True, "email": user.email, "name": user.fullname}
