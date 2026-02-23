from dataclasses import dataclass
import datetime


@dataclass
class NormalizedEvent:
    uid: str
    summary: str
    description: str
    dtstart: datetime.datetime
    dtend: datetime.datetime


@dataclass
class Condition:
    field: str
    operator: str
    value: str


@dataclass
class Action:
    type: str
    field: dict


@dataclass
class Rule:
    enabled: bool
    name: str
    conditions: list[Condition]
    actions: list[Action]


@dataclass
class Source:
    id: str
    type: str
    url: str
    rules: list[Rule]


@dataclass
class SyncConfig:
    id: str
    destination: str
    sources: list[Source]
    username: str
    password: str


@dataclass
class Task:
    id: str
    title: str
    description: str
    due_date: datetime.datetime | int | None = None
    duration: int = 30
    not_before: datetime.datetime | int | None = None
    priority: int = 3


@dataclass
class TaskEvent:
    id: str
    title: str
    start: datetime.datetime
    end: datetime.datetime


@dataclass
class SchedulerConfig:
    id: str
    name: str
    calendar_url: str
    calendar_password: str
    calendar_username: str
    tasks: list
