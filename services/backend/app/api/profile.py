import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from aio_pika.abc import AbstractRobustConnection
import aio_pika
from app.api.auth import get_current_user
from app.db.session import get_async_db, get_message_queue
from app.models.integration import (
    CalendarProfile,
    CalendarSource,
)
from app.models.user import User
from app.schemas.integration import (
    ProfileCreate,
    SourceRead,
    ProfileReadShort,
    ProfileReadFull,
    SourceCreate,
)
from app.core.sync_config_helper import profile_to_shared_profile
from app.core.auth import auth_responses

ROUTING_KEY = "sync_queue"


async def _get_profile_or_404(
    profile_id: str, current_user: User, db: AsyncSession
) -> CalendarProfile:
    result = await db.execute(
        select(CalendarProfile)
        .options(selectinload(CalendarProfile.calendar_sources))
        .where(
            CalendarProfile.id == profile_id,
            CalendarProfile.user_id == current_user.id,
        )
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile


async def _get_source_or_404(
    user: User, profile_id: str, source_id: str, db: AsyncSession
) -> CalendarSource:
    result = await db.execute(
        select(CalendarSource)
        .join(CalendarProfile)
        .where(
            CalendarSource.id == source_id,
            CalendarProfile.id == profile_id,
            CalendarProfile.user_id == user.id,
        )
    )
    source = result.scalar_one_or_none()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )
    return source


profile_router = APIRouter(responses=auth_responses)


@profile_router.get(
    "", response_model=list[ProfileReadShort], operation_id="list_profiles"
)
async def list_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(CalendarProfile)
        .options(selectinload(CalendarProfile.calendar_sources))
        .where(CalendarProfile.user_id == current_user.id)
    )
    profiles = result.scalars().all()

    return profiles


@profile_router.get(
    "/{profile_id}", response_model=ProfileReadFull, operation_id="get_profile"
)
async def get_profile(
    profile_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(CalendarProfile)
        .options(selectinload(CalendarProfile.calendar_sources))
        .where(CalendarProfile.id == profile_id, CalendarProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()
    return profile


@profile_router.post(
    "",
    response_model=ProfileReadShort,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_profile",
)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    new_profile = CalendarProfile(
        user_id=current_user.id,
        name=profile_data.name,
        main_calendar_id=profile_data.main_calendar_id,
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    return new_profile


@profile_router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_profile",
)
async def delete_profile(
    profile_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(CalendarProfile).where(
            CalendarProfile.id == profile_id, CalendarProfile.user_id == current_user.id
        )
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    await db.delete(profile)
    await db.commit()
    return


@profile_router.put(
    "/{profile_id}", response_model=ProfileReadShort, operation_id="update_profile"
)
async def update_profile(
    profile_id: str,
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(CalendarProfile).where(
            CalendarProfile.id == profile_id, CalendarProfile.user_id == current_user.id
        )
    )
    profile = result.unique().scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    profile.name = profile_data.name
    profile.main_calendar_id = profile_data.main_calendar_id
    await db.commit()
    await db.refresh(profile)
    return profile


@profile_router.get(
    "/{profile_id}/source",
    response_model=list[SourceRead],
    operation_id="list_profile_sources",
)
async def list_profile_sync(
    profile_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(profile_id, current_user, db)

    return profile.calendar_sources


@profile_router.post(
    "/{profile_id}/source",
    status_code=status.HTTP_201_CREATED,
    operation_id="add_profile_source",
)
async def add_profile_source(
    profile_id: str,
    source_data: SourceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(profile_id, current_user, db)

    # TODO Validate source_data

    new_source = CalendarSource(
        profile_id=profile.id,
        calendar_id=source_data.calendar_id,
    )
    db.add(new_source)
    await db.commit()
    await db.refresh(new_source)

    return new_source


@profile_router.delete(
    "/{profile_id}/source/{source_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_profile_source",
)
async def delete_profile_source(
    profile_id: str,
    source_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    source = await _get_source_or_404(current_user, profile_id, source_id, db)

    await db.delete(source)
    await db.commit()
    return


@profile_router.post(
    "/{profile_id}/sync",
    status_code=status.HTTP_202_ACCEPTED,
    operation_id="trigger_profile_sync",
)
async def trigger_profile_sync(
    profile_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
    conn: AbstractRobustConnection = Depends(get_message_queue),
):
    profile = await _get_profile_or_404(profile_id, current_user, db)

    sources = profile.calendar_sources

    print(f"Triggering sync for profile {profile.id} with {len(sources)} sources")
    print(sources)

    channel = await conn.channel()

    payload = {
        "type": "sync",
        "payload": profile_to_shared_profile(profile).model_dump(),
    }

    print(f"Publishing message to queue: {payload}")

    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(payload).encode()),
        routing_key="worker",
    )

    return {"message": "Sync triggered"}


"""
@profile_router.get("/{profile_id}/ruleset", response_model=list[RuleCreate])
async def get_rules(
    profile_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(profile_id, current_user, db)
    return profile.rules


@profile_router.post("/{profile_id}/ruleset", status_code=status.HTTP_201_CREATED)
async def set_rules(
    profile_id: str,
    rules_data: list[RuleCreate],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(profile_id, current_user, db)

    # TODO Validate rules_data

    # Clear existing rules
    for source in profile.calendar_sources:
        for rule in source.rules:
            await db.delete(rule)

    # Add new rules
    for rule_data in rules_data:
        source = next(
            (s for s in profile.calendar_sources if s.id == rule_data.source_id), None
        )
        if not source:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid source_id: {rule_data.source_id}",
            )
        new_rule = Rule(
            calendar_source_id=source.id,
            enabled=rule_data.enabled,
            name=rule_data.name,
        )
        db.add(new_rule)
        await db.flush()

        for condition_data in rule_data.conditions:
            condition = Condition(rule_id=new_rule.id, **condition_data.dict())
            db.add(condition)

        for action_data in rule_data.actions:
            action = Action(rule_id=new_rule.id, **action_data.dict())
            db.add(action)
        db.add(new_rule)

    await db.commit()
"""
