from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.integration import Calendar
from app.schemas.integration import CalendarRead, CalendarCreate
from app.api.auth import get_current_user
from app.db.session import get_db

calendar_router = APIRouter()


@calendar_router.get("", response_model=list[CalendarRead])
async def list_calendars(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve all calendars for the current user."""

    calendars = db.query(Calendar).filter(Calendar.owner_id == user.id).all()

    return calendars


@calendar_router.post("", response_model=CalendarRead)
async def create_calendar(
    calendar_data: CalendarCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new calendar for the current user."""

    calendar = Calendar(
        type=calendar_data.type,
        url=calendar_data.url,
        username=calendar_data.username,
        password=calendar_data.password,
        owner_id=user.id,
    )

    db.add(calendar)
    db.commit()
    db.refresh(calendar)

    return calendar


@calendar_router.delete("/{calendar_id}", status_code=204)
async def delete_calendar(
    calendar_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a calendar by ID."""

    calendar = (
        db.query(Calendar)
        .filter(Calendar.id == calendar_id, Calendar.owner_id == user.id)
        .first()
    )

    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")

    db.delete(calendar)
    db.commit()


@calendar_router.get("/{calendar_id}", response_model=CalendarRead)
async def get_calendar(
    calendar_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a calendar by ID."""

    calendar = (
        db.query(Calendar)
        .filter(Calendar.id == calendar_id, Calendar.owner_id == user.id)
        .first()
    )

    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")

    return calendar


@calendar_router.put("/{calendar_id}", response_model=CalendarRead)
async def update_calendar(
    calendar_id: str,
    calendar_data: CalendarCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a calendar by ID."""

    calendar = (
        db.query(Calendar)
        .filter(Calendar.id == calendar_id, Calendar.owner_id == user.id)
        .first()
    )

    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")

    calendar.type = calendar_data.type
    calendar.url = calendar_data.url
    calendar.username = calendar_data.username
    calendar.password = calendar_data.password

    db.commit()
    db.refresh(calendar)

    return calendar
