from dataclasses import dataclass
import datetime
from pydantic import BaseModel


@dataclass
class NormalizedEvent:
    uid: str
    summary: str
    description: str
    dtstart: datetime.datetime
    dtend: datetime.datetime


class Message(BaseModel):
    type: str
    payload: dict
