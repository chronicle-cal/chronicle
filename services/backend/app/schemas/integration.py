from pydantic import BaseModel, Field
from datetime import datetime


class Condition(BaseModel):
    id: int
    rule_id: int
    field: str
    operator: str
    value: str


class ConditionCreate(BaseModel):
    field: str = Field(...)
    operator: str = Field(...)
    value: str = Field(...)


class Action(BaseModel):
    id: int
    rule_id: int
    type: str
    field: dict


class ActionCreate(BaseModel):
    type: str = Field(...)
    field: dict = Field(...)


class Rule(BaseModel):
    id: int
    calendar_profile_id: str
    enabled: bool
    name: str


class RuleCreate(BaseModel):
    enabled: bool = Field(True)
    name: str = Field(...)


class CalendarProfile(BaseModel):
    id: str
    sync_config_id: str
    name: str
    color: str
    type: str
    url: str


class CalendarProfileCreate(BaseModel):
    name: str = Field(...)
    color: str = Field("#3B82F6")
    type: str = Field(...)
    url: str = Field(...)


class SyncConfig(BaseModel):
    id: str
    destination: str


class SyncConfigCreate(BaseModel):
    destination: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)


class Task(BaseModel):
    id: str
    scheduler_config_id: str
    title: str
    description: str
    due_date: datetime | None
    duration: int
    not_before: datetime | None
    priority: int


class TaskCreate(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    due_date: datetime | None = Field(None)
    duration: int = Field(30)
    not_before: datetime | None = Field(None)
    priority: int = Field(3)


class SchedulerConfig(BaseModel):
    id: str
    name: str
    calendar_url: str


class SchedulerConfigCreate(BaseModel):
    name: str = Field(...)
    calendar_url: str = Field(...)
    calendar_username: str = Field(...)
    calendar_password: str = Field(...)
