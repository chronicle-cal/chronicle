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
    source_id: str
    enabled: bool
    name: str


class RuleCreate(BaseModel):
    enabled: bool = Field(True)
    name: str = Field(...)


class Source(BaseModel):
    id: str
    sync_config_id: str
    type: str
    url: str


class SourceCreate(BaseModel):
    id: str = Field(...)
    type: str = Field(...)
    url: str = Field(...)


class SyncConfig(BaseModel):
    id: str
    destination: str
    username: str
    password: str


class SyncConfigCreate(BaseModel):
    id: str = Field(...)
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
    id: str = Field(...)
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
    calendar_password: str
    calendar_username: str


class SchedulerConfigCreate(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    calendar_url: str = Field(...)
    calendar_password: str = Field(...)
    calendar_username: str = Field(...)
