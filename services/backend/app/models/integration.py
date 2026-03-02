from sqlalchemy import ForeignKey, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

from app.core.db import Base


class Condition(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id", ondelete="CASCADE"), nullable=False
    )
    field: Mapped[str] = mapped_column(String(255), nullable=False)
    operator: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[str] = mapped_column(String(2048), nullable=False)

    rule = relationship("Rule", back_populates="conditions")


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    field: Mapped[dict] = mapped_column(JSON, nullable=False)

    rule = relationship("Rule", back_populates="actions")


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[str] = mapped_column(
        ForeignKey("sources.id", ondelete="CASCADE"), nullable=False
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

    source = relationship("Source", back_populates="rules")


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    sync_config_id: Mapped[str] = mapped_column(
        ForeignKey("sync_configs.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)

    rules = relationship(
        "Rule", back_populates="source", cascade="all, delete-orphan", lazy="joined"
    )

    sync_config = relationship("SyncConfig", back_populates="sources")


class SyncConfig(Base):
    __tablename__ = "sync_configs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    sources = relationship(
        "Source",
        back_populates="sync_config",
        cascade="all, delete-orphan",
        lazy="joined",
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scheduler_config_id: Mapped[str] = mapped_column(
        ForeignKey("scheduler_configs.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(4096), nullable=False)
    due_date: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    duration: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    not_before: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)

    scheduler_config = relationship("SchedulerConfig", back_populates="tasks")


class SchedulerConfig(Base):
    __tablename__ = "scheduler_configs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    calendar_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    calendar_password: Mapped[str] = mapped_column(String(255), nullable=False)
    calendar_username: Mapped[str] = mapped_column(String(255), nullable=False)

    tasks = relationship(
        "Task",
        back_populates="scheduler_config",
        cascade="all, delete-orphan",
        lazy="joined",
    )
