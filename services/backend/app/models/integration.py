from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, Integer, String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Condition(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id", ondelete="CASCADE"), nullable=False
    )
    field: Mapped[str] = mapped_column(String(255), nullable=False)
    operator: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[str] = mapped_column(String(2048), nullable=False)

    rule = relationship("Rule", back_populates="conditions", lazy="joined")


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    arguments: Mapped[dict] = mapped_column(JSON, nullable=False)

    rule = relationship("Rule", back_populates="actions", lazy="joined")


class CalendarSource(Base):
    __tablename__ = "calendar_sources"

    id: Mapped[str] = mapped_column(
        String(64), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    profile_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_profiles.id", ondelete="CASCADE"), nullable=False
    )
    calendar_id: Mapped[str] = mapped_column(
        ForeignKey("calendars.id", ondelete="CASCADE"), nullable=False
    )

    profile = relationship(
        "CalendarProfile", back_populates="calendar_sources", lazy="joined"
    )
    calendar = relationship("Calendar", lazy="joined")
    rules = relationship(
        "Rule",
        back_populates="calendar_source",
        cascade="all, delete-orphan",
        lazy="joined",
    )


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    calendar_profile_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_profiles.id", ondelete="CASCADE"), nullable=False
    )
    calendar_source_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_sources.id", ondelete="CASCADE"), nullable=False
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    conditions = relationship(
        "Condition",
        back_populates="rule",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    actions = relationship(
        "Action", back_populates="rule", cascade="all, delete-orphan", lazy="joined"
    )

    calendar_source = relationship("CalendarSource", back_populates="rules")


class Calendar(Base):
    __tablename__ = "calendars"

    id: Mapped[str] = mapped_column(
        String(64), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    type: Mapped[str] = mapped_column(String(64), nullable=False)  # "caldav" or "ical"
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    owner_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="calendars", lazy="joined")


class CalendarProfile(Base):
    __tablename__ = "calendar_profiles"

    id: Mapped[str] = mapped_column(
        String(64), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    main_calendar_id: Mapped[str | None] = mapped_column(
        ForeignKey("calendars.id", ondelete="SET NULL"), nullable=True
    )

    calendar_sources = relationship(
        "CalendarSource",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    main_calendar = relationship(
        "Calendar", foreign_keys=[main_calendar_id], lazy="joined"
    )

    tasks = relationship(
        "Task", back_populates="profile", cascade="all, delete-orphan", lazy="joined"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        String(64), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    not_before: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    profile_id: Mapped[str | None] = mapped_column(
        ForeignKey("calendar_profiles.id", ondelete="SET NULL"), nullable=True
    )
    completed = mapped_column(Boolean, default=False, nullable=False)
    profile = relationship("CalendarProfile", lazy="joined")
