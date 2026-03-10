from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.auth import get_current_user
from app.db.session import get_async_db
from app.models.integration import (
    CalendarProfile,
    Calendar,
    CalendarSource,
    Rule,
    Condition,
    Action,
)
from app.models.user import User
from app.schemas.integration import (
    CalendarProfile as CalendarProfileSchema,
    CalendarProfileCreate,
    CalendarProfileUpdate,
    Rule as RuleSchema,
    RuleCreate,
)

profile_router = APIRouter()


def _rule_to_response(rule: Rule) -> dict:
    return {
        "id": rule.id,
        "source_id": rule.calendar_source_id,
        "enabled": rule.enabled,
        "name": rule.name,
        "conditions": rule.conditions,
        "actions": rule.actions,
    }


def _profile_to_response(profile: CalendarProfile, rules: list[Rule]) -> dict:
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "name": profile.name,
        "main_calendar_id": profile.main_calendar_id,
        "rules": [_rule_to_response(rule) for rule in rules],
    }


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
    profile = result.unique().scalar_one_or_none()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


async def _get_rules_for_sources(db: AsyncSession, source_ids: list[str]) -> list[Rule]:
    if not source_ids:
        return []
    result = await db.execute(
        select(Rule)
        .options(selectinload(Rule.conditions), selectinload(Rule.actions))
        .where(Rule.calendar_source_id.in_(source_ids))
    )
    return list(result.unique().scalars().all())


def _get_default_source_id(profile: CalendarProfile) -> str | None:
    if profile.main_calendar_id:
        for source in profile.calendar_sources:
            if source.calendar_id == profile.main_calendar_id:
                return source.id
    if profile.calendar_sources:
        return profile.calendar_sources[0].id
    return None


@profile_router.get("", response_model=list[CalendarProfileSchema])
async def list_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(
        select(CalendarProfile)
        .options(selectinload(CalendarProfile.calendar_sources))
        .where(CalendarProfile.user_id == current_user.id)
    )
    profiles = list(result.unique().scalars().all())
    source_ids = [
        source.id for profile in profiles for source in profile.calendar_sources
    ]
    rules = await _get_rules_for_sources(db, source_ids)
    rules_by_source: dict[str, list[Rule]] = defaultdict(list)
    for rule in rules:
        rules_by_source[rule.calendar_source_id].append(rule)

    response = []
    for profile in profiles:
        profile_rules: list[Rule] = []
        for source in profile.calendar_sources:
            profile_rules.extend(rules_by_source.get(source.id, []))
        response.append(_profile_to_response(profile, profile_rules))
    return response


@profile_router.post(
    "", response_model=CalendarProfileSchema, status_code=status.HTTP_201_CREATED
)
async def create_profile(
    payload: CalendarProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    calendar_data = payload.main_calendar.model_dump()
    calendar = Calendar(**calendar_data)
    db.add(calendar)
    await db.flush()

    profile = CalendarProfile(
        user_id=current_user.id,
        name=payload.name,
        main_calendar_id=calendar.id,
    )
    db.add(profile)
    await db.flush()

    source = CalendarSource(profile_id=profile.id, calendar_id=calendar.id)
    db.add(source)

    await db.commit()
    await db.refresh(profile)
    await db.refresh(profile, ["calendar_sources"])
    return _profile_to_response(profile, [])


@profile_router.get("/{id}", response_model=CalendarProfileSchema)
async def get_profile(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(id, current_user, db)
    source_ids = [source.id for source in profile.calendar_sources]
    rules = await _get_rules_for_sources(db, source_ids)
    return _profile_to_response(profile, rules)


@profile_router.put("/{id}", response_model=CalendarProfileSchema)
async def update_profile(
    id: str,
    payload: CalendarProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(id, current_user, db)
    if payload.name is not None:
        profile.name = payload.name

    await db.commit()
    await db.refresh(profile)
    await db.refresh(profile, ["calendar_sources"])
    source_ids = [source.id for source in profile.calendar_sources]
    rules = await _get_rules_for_sources(db, source_ids)
    return _profile_to_response(profile, rules)


@profile_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(id, current_user, db)
    await db.delete(profile)
    await db.commit()


@profile_router.get("/{id}/rule", response_model=list[RuleSchema])
async def list_rules(
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(id, current_user, db)
    source_ids = [source.id for source in profile.calendar_sources]
    rules = await _get_rules_for_sources(db, source_ids)
    return [_rule_to_response(rule) for rule in rules]


@profile_router.post(
    "/{id}/rule", response_model=RuleSchema, status_code=status.HTTP_201_CREATED
)
async def create_rule(
    id: str,
    payload: RuleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    profile = await _get_profile_or_404(id, current_user, db)

    source_id = payload.source_id
    if source_id:
        if source_id not in {source.id for source in profile.calendar_sources}:
            raise HTTPException(status_code=404, detail="Source not found")
    else:
        source_id = _get_default_source_id(profile)
        if source_id is None and profile.main_calendar_id:
            source = CalendarSource(
                profile_id=profile.id, calendar_id=profile.main_calendar_id
            )
            db.add(source)
            await db.flush()
            source_id = source.id
        if source_id is None:
            raise HTTPException(
                status_code=400, detail="Profile has no calendar source"
            )

    rule = Rule(
        calendar_profile_id=profile.id,
        calendar_source_id=source_id,
        enabled=payload.enabled,
        name=payload.name,
    )

    for cond_data in payload.conditions:
        rule.conditions.append(Condition(**cond_data.model_dump()))
    for action_data in payload.actions:
        rule.actions.append(Action(**action_data.model_dump()))

    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    await db.refresh(rule, ["conditions", "actions"])
    return _rule_to_response(rule)


@profile_router.post("/{profile_id}/rule/{rule_id}", response_model=RuleSchema)
async def update_rule(
    profile_id: str,
    rule_id: int,
    payload: RuleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    await _get_profile_or_404(profile_id, current_user, db)
    rule_result = await db.execute(
        select(Rule)
        .options(selectinload(Rule.conditions), selectinload(Rule.actions))
        .join(CalendarSource, Rule.calendar_source_id == CalendarSource.id)
        .where(Rule.id == rule_id, CalendarSource.profile_id == profile_id)
    )
    rule = rule_result.unique().scalar_one_or_none()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    rule.enabled = payload.enabled
    rule.name = payload.name
    rule.conditions.clear()
    rule.actions.clear()

    for cond_data in payload.conditions:
        rule.conditions.append(Condition(**cond_data.model_dump()))
    for action_data in payload.actions:
        rule.actions.append(Action(**action_data.model_dump()))

    await db.commit()
    await db.refresh(rule)
    await db.refresh(rule, ["conditions", "actions"])
    return _rule_to_response(rule)


@profile_router.delete(
    "/{profile_id}/rule/{rule_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_rule(
    profile_id: str,
    rule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    await _get_profile_or_404(profile_id, current_user, db)
    rule_result = await db.execute(
        select(Rule)
        .join(CalendarSource, Rule.calendar_source_id == CalendarSource.id)
        .where(Rule.id == rule_id, CalendarSource.profile_id == profile_id)
    )
    rule = rule_result.scalar_one_or_none()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    await db.delete(rule)
    await db.commit()
