from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.models.user import User as UserModel
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

from app.core.auth import (
    get_current_user,
    pwd_context,
    create_token,
    get_current_token,
    auth_responses,
)

router = APIRouter()


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


@router.get("/token", responses=auth_responses)
async def get_token(
    token: str = Depends(get_current_token),
):
    return {"access_token": token}
