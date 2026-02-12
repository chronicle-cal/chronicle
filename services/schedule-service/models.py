from dataclasses import dataclass
import datetime


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
