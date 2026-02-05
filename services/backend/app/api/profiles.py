from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.profile import Profile as ProfileModel
from app.schemas.profiles import Profile as ProfileSchema
from app.schemas.profiles import ProfileCreate

router = APIRouter()


@router.get("")
async def list_profiles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProfileModel))
    items = result.scalars().all()
    return [{"id": p.id, "user_id": p.user_id, "name": p.name} for p in items]


@router.post("", response_model=ProfileSchema, status_code=status.HTTP_201_CREATED)
async def create_profile(payload: ProfileCreate, db: AsyncSession = Depends(get_db)):
    # Placeholder user_id until auth/user linkage is implemented.
    profile = ProfileModel(name=payload.name, user_id=1)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return ProfileSchema(id=profile.id, name=profile.name)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    profile = await db.get(ProfileModel, profile_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    await db.delete(profile)
    await db.commit()
    return None
