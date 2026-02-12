import caldav
import icalendar
from models import NormalizedEvent
import logging


class CaldavTarget:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.client = caldav.DAVClient(
            url=url,
            username=username,
            password=password,
        )
        self.calendar = self.client.calendar(url=url)
        logging.info("Connected to CalDAV server")

    def build_index(self) -> dict[str, dict]:
        """
        UID → {href,  event}
        """
        index = {}

        for event in self.calendar.events():
            uid = str(event.component.get("UID"))
            dtstart = event.component["dtstart"].dt
            dtend = event.component["dtend"].dt
            index[uid] = {
                "href": event.url,
                "event": NormalizedEvent(
                    uid=uid,
                    summary=str(event.component.get("summary", "")),
                    description=str(event.component.get("description", "")),
                    dtstart=dtstart,
                    dtend=dtend,
                ),
            }
        logging.info(f"Built index with {len(index)} events from CalDAV")
        return index

    def create(self, raw_ical: icalendar.Event):
        logging.info(f"Creating event UID={raw_ical.get('UID')}")
        self.calendar.add_event(raw_ical.to_ical())

    def update(self, href: str, event: NormalizedEvent):
        logging.info(f"Updating event UID={event.uid} at href={href}")
        ev = self.calendar.event_by_url(href)
        ev.data = self._update_event_component(ev.component, event)
        ev.save()

    def update_raw(self, href: str, raw_ical: icalendar.Event):
        logging.info(f"Updating event UID={raw_ical.get('UID')} at href={href}")
        ev = self.calendar.event_by_url(href)
        ev.component = raw_ical
        ev.save()

    def delete(self, href: str):
        logging.info(f"Deleting event at href={href}")
        ev = self.calendar.event_by_url(href)
        ev.delete()

    def _update_event_component(
        self, component: icalendar.Event, event: NormalizedEvent
    ):
        component["SUMMARY"] = event.summary
        component["DESCRIPTION"] = event.description
        component["DTSTART"] = event.dtstart
        component["DTEND"] = event.dtend
        return component
