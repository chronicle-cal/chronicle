from pydantic import BaseModel, Field, ConfigDict, AliasChoices

from datetime import datetime


class Condition(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

    id: int
    rule_id: int
    name: str
    arguments: dict


class ActionCreate(BaseModel):
    name: str = Field(..., validation_alias=AliasChoices("name", "type"))
    arguments: dict = Field(...)


class Rule(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: str
    enabled: bool
    name: str
    conditions: list[Condition] = Field(default_factory=list)
    actions: list[Action] = Field(default_factory=list)


class RuleCreate(BaseModel):
    enabled: bool = Field(True)
    name: str = Field(...)
    source_id: str | None = Field(None)
    conditions: list[ConditionCreate] = Field(default_factory=list)
    actions: list[ActionCreate] = Field(default_factory=list)


class Calendar(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: str
    url: str
    username: str | None
    password: str | None


class CalendarCreate(BaseModel):
    type: str = Field(...)
    url: str = Field(...)
    username: str | None = Field(None)
    password: str | None = Field(None)


class CalendarRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    type: str
    url: str
    username: str | None
    password: str | None


class CalendarProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: int
    name: str
    main_calendar_id: str | None


class CalendarProfileCreate(BaseModel):
    name: str = Field(...)
    main_calendar: CalendarCreate = Field(...)


class CalendarProfileUpdate(BaseModel):
    name: str | None = Field(None)


class ProfileCreate(BaseModel):
    name: str = Field(...)
    main_calendar_id: str = Field(
        ..., validation_alias=AliasChoices("main_calendar_id", "main_calendar")
    )


class ProfileReadShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    main_calendar_id: str | None


class ProfileReadFull(ProfileReadShort):
    main_calendar: CalendarRead | None
    rules: list[Rule] = Field(default_factory=list)


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    calendar_id: str
    calendar: CalendarRead


class SourceCreate(BaseModel):
    calendar_id: str = Field(
        ..., validation_alias=AliasChoices("calendar_id", "calendar")
    )


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    completed: bool
    title: str
    description: str | None = None
    due_date: datetime | None = None
    duration: int = 30
    not_before: datetime | None = None
    priority: int = 3
    profile: ProfileReadShort | None = None
    profile_id: str | None = None


class CreateTask(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    duration: int = 30
    not_before: datetime | None = None
    priority: int = 3
    profile_id: str | None = None


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    duration: int | None = None
    not_before: datetime | None = None
    priority: int | None = None
    profile_id: str | None = None
    completed: bool | None = None
