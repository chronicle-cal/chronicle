import logging
import abc
import icalendar
import requests

from models import NormalizedEvent


class BaseSource(abc.ABC):
    @abc.abstractmethod
    def fetch(self) -> list[tuple[NormalizedEvent, icalendar.Event]]:
        raise NotImplementedError("Must implement fetch method in subclass")


class IcsSource(BaseSource):
    def __init__(self, url: str):
        self.url = url
        logging.info(f"Initialized IcsSource with URL: {self.url}")

    def fetch(self) -> list[tuple[NormalizedEvent, icalendar.Event]]:
        logging.info(f"Fetching ICS events from {self.url}")
        resp = requests.get(self.url)
        resp.raise_for_status()

        cal = icalendar.Calendar.from_ical(resp.text)
        events = []

        for component in cal.walk("VEVENT"):
            norm = NormalizedEvent(
                uid=str(component.get("UID")),
                summary=str(component.get("SUMMARY", "")),
                description=str(component.get("DESCRIPTION", "")),
                dtstart=component.decoded("DTSTART"),
                dtend=component.decoded("DTEND"),
            )
            events.append((norm, component))
        logging.info(f"Fetched {len(events)} events from ICS source")
        return events
