from dataclasses import dataclass
import datetime


@dataclass
class NormalizedEvent:
    uid: str
    summary: str
    description: str
    dtstart: datetime.datetime
    dtend: datetime.datetime
