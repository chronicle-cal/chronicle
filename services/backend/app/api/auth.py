from fastapi import APIRouter, Depends, Header, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.user import User as UserModel
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    email = payload.email.lower()
    existing = await db.execute(select(UserModel).where(UserModel.email == email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    user = UserModel(email=email, password_hash=pwd_context.hash(payload.password))
    db.add(user)
    await db.commit()
    return {"message": "registered"}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    email = payload.email.lower()
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if user is None or not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return TokenResponse(access_token="dev-token")


@router.post("/logout")
def logout():
    return {"message": "logged out"}


@router.get("/me")
def me(authorization: str | None = Header(default=None)):
    # Minimal check: expects "Bearer dev-token"
    if authorization != "Bearer dev-token":
        return {"authenticated": False}
    return {"authenticated": True}
