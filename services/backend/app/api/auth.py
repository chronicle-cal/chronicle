import base64
import hashlib
import hmac
import os
import time

from fastapi import APIRouter, Depends, Header, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.profile import Profile as ProfileModel
from app.models.user import User as UserModel
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UpdateEmailRequest,
    UpdateNameRequest,
    UpdatePasswordRequest,
    DeleteAccountRequest,
)

router = APIRouter()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
AUTH_SECRET = os.getenv("AUTH_SECRET", "dev-secret")
AUTH_TOKEN_TTL = int(os.getenv("AUTH_TOKEN_TTL", "604800"))


def _b64encode(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")


def _b64decode(value: str) -> str:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding).decode()


def _sign(payload: str) -> str:
    digest = hmac.new(AUTH_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return digest


def create_token(email: str) -> str:
    payload = f"{email}|{int(time.time())}"
    sig = _sign(payload)
    return f"{_b64encode(payload)}.{sig}"


def verify_token(token: str) -> str | None:
    try:
        encoded, sig = token.split(".", 1)
        payload = _b64decode(encoded)
    except Exception:
        return None

    if not hmac.compare_digest(sig, _sign(payload)):
        return None

    try:
        email, ts = payload.rsplit("|", 1)
        issued_at = int(ts)
    except ValueError:
        return None

    if int(time.time()) - issued_at > AUTH_TOKEN_TTL:
        return None

    return email


def get_bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    return authorization.split(" ", 1)[1].strip()


async def get_current_user(
    token: str = Depends(get_bearer_token), db: AsyncSession = Depends(get_db)
) -> UserModel:
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


async def get_profile_name(db: AsyncSession, user_id: int) -> str:
    profile_result = await db.execute(
        select(ProfileModel).where(ProfileModel.user_id == user_id)
    )
    profile_row = profile_result.scalar_one_or_none()
    return profile_row.name if profile_row else ""


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
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
    return TokenResponse(access_token=create_token(email))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    email = payload.email.lower()
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
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
    user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    name = await get_profile_name(db, user.id)
    return {"authenticated": True, "email": user.email, "name": name}


@router.post("/update-email")
async def update_email(
    payload: UpdateEmailRequest,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    new_email = payload.new_email.lower()
    if user.email == new_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New email must be different",
        )

    if not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    conflict = await db.execute(select(UserModel).where(UserModel.email == new_email))
    if conflict.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    user.email = new_email
    await db.commit()
    return {
        "message": "email updated",
        "email": new_email,
        "access_token": create_token(new_email),
    }


@router.post("/update-password")
async def update_password(
    payload: UpdatePasswordRequest,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not pwd_context.verify(payload.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    user.password_hash = pwd_context.hash(payload.new_password)
    await db.commit()
    return {"message": "password updated"}


@router.post("/update-name")
async def update_name(
    payload: UpdateNameRequest,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    profile = await db.execute(
        select(ProfileModel).where(ProfileModel.user_id == user.id)
    )
    profile = profile.scalar_one_or_none()
    if profile is None:
        profile = ProfileModel(user_id=user.id, name=payload.name)
        db.add(profile)
    else:
        profile.name = payload.name

    await db.commit()
    return {"message": "name updated"}


@router.post("/delete-account")
async def delete_account(
    payload: DeleteAccountRequest,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if payload.confirm.strip().lower() != "delete":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Confirmation text must be 'delete'",
        )

    await db.delete(user)
    await db.commit()
    return {"message": "account deleted"}
