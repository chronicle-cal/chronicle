from pydantic import BaseModel, Field, ConfigDict, AliasChoices


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
    rules: list[Rule] = Field(default_factory=list)


class CalendarProfileCreate(BaseModel):
    name: str = Field(...)
    main_calendar: CalendarCreate = Field(...)


class CalendarProfileUpdate(BaseModel):
    name: str | None = Field(None)
