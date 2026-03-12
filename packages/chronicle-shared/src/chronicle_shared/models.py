from pydantic import BaseModel
from datetime import datetime


class Condition(BaseModel):
    field: str
    operator: str
    value: str


class Action(BaseModel):
    type: str
    field: dict


class Rule(BaseModel):
    enabled: bool
    name: str
    conditions: list[Condition]
    actions: list[Action]


class Calenadar(BaseModel):
    id: str
    type: str
    url: str
    username: str
    password: str


class Source(BaseModel):
    id: str
    calendar: Calenadar
    rules: list[Rule]


class Task(BaseModel):
    id: str
    title: str
    description: str
    due_date: datetime | int | None = None
    duration: int = 30
    not_before: datetime | int | None = None
    priority: int = 3


class Profile(BaseModel):
    id: str
    name: str
    main_calendar: Calenadar
    sources: list[Source]
    tasks: list[Task]


class TaskEvent(BaseModel):
    id: str
    title: str
    start: datetime
    end: datetime


class SchedulerConfig(BaseModel):
    id: str
    name: str
    calendar_url: str
    calendar_password: str
    calendar_username: str
    tasks: list[Task]
