from dataclasses import dataclass
from datetime import datetime
import hashlib
import logging
import requests
from icalendar import Calendar
import caldav
import re
import icalendar
import os


@dataclass
class NormalizedEvent:
    uid: str
    summary: str
    description: str
    dtstart: datetime
    dtend: datetime
    # Only used for hashing/rules, not for updating/creating events


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


def evaluate_condition(event: NormalizedEvent, condition: Condition) -> bool:
    field_value = getattr(event, condition.field, "")
    match condition.operator:
        case "contains":
            return condition.value in field_value
        case "equals":
            return condition.value == field_value
        case "starts_with":
            return field_value.startswith(condition.value)
        case "ends_with":
            return field_value.endswith(condition.value)
        case "regex":
            return re.search(condition.value, field_value) is not None
    return False


def apply_actions(event: NormalizedEvent, actions: list[Action]) -> NormalizedEvent:
    for action in actions:
        match action.type:
            case "set_field":
                setattr(event, action.field["name"], action.field["value"])
    return event


def apply_rules(event: NormalizedEvent, rules: list[Rule]) -> NormalizedEvent:
    for rule in rules:
        if not rule.enabled:
            continue

        if all(evaluate_condition(event, cond) for cond in rule.conditions):
            event = apply_actions(event, rule.actions)
    return event


def hash_event(event: NormalizedEvent) -> str:
    canonical = (
        event.summary,
        event.description,
        event.dtstart.isoformat(),
        event.dtend.isoformat(),
    )

    logging.debug(f"Canonical representation for hashing: {canonical}")

    return hashlib.sha256(repr(canonical).encode()).hexdigest()


class IcsSource:
    def __init__(self, url: str):
        self.url = url
        logging.info(f"Initialized IcsSource with URL: {self.url}")

    def fetch(self) -> list[tuple[NormalizedEvent, icalendar.Event]]:
        logging.info(f"Fetching ICS events from {self.url}")
        resp = requests.get(self.url)
        resp.raise_for_status()

        cal = Calendar.from_ical(resp.text)
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
        with caldav.DAVClient(
            url=self.url,
            username=self.username,
            password=self.password,
        ) as client:
            calendar = client.calendar(url=self.url)
            ev = calendar.event_by_url(href)
            ev.data = self._update_event_component(ev.component, event)
            ev.save()

    def update_raw(self, href: str, raw_ical: icalendar.Event):
        with caldav.DAVClient(
            url=self.url,
            username=self.username,
            password=self.password,
        ) as client:
            calendar = client.calendar(url=self.url)
            logging.info(f"Updating event UID={raw_ical.get('UID')} at href={href}")
            ev = calendar.event_by_url(href)
            ev.component = raw_ical
            ev.save()

    def delete(self, href: str):
        logging.info(f"Deleting event at href={href}")
        with caldav.DAVClient(
            url=self.url,
            username=self.username,
            password=self.password,
        ) as client:
            calendar = client.calendar(url=self.url)
            ev = calendar.event_by_url(href)
            ev.delete()

    def _update_event_component(
        self, component: icalendar.Event, event: NormalizedEvent
    ):
        component["SUMMARY"] = event.summary
        component["DESCRIPTION"] = event.description
        component["DTSTART"] = event.dtstart
        component["DTEND"] = event.dtend
        return component


class SyncEngine:
    def __init__(self, config: SyncConfig):
        logging.info(f"Initializing SyncEngine for destination: {config.destination}")
        self.sources: list[tuple[IcsSource, Source]] = []
        for source in config.sources:
            if source.type == "ics":
                self.sources.append((IcsSource(source.url), source))
                logging.info(f"Added ICS source: {source.url}")
            else:
                logging.error(f"Unsupported source type: {source.type}")
                raise ValueError(f"Unsupported source type: {source.type}")
        self.target = CaldavTarget(config.destination, config.username, config.password)

    def run(self):
        logging.info("Starting sync run...")
        for source, config in self.sources:
            logging.info(f"Processing source: {config.url}")
            source_events = source.fetch()
            dest_index = self.target.build_index()

            source_uids = set()

            for norm_event, raw_ical in source_events:
                source_uids.add(norm_event.uid)

                final_event = apply_rules(norm_event, config.rules)
                final_hash = hash_event(final_event)

                # apply the final event data to the raw iCal component for updating/creating
                raw_ical["SUMMARY"] = final_event.summary
                raw_ical["DESCRIPTION"] = final_event.description

                if norm_event.uid in dest_index:
                    dest = dest_index[norm_event.uid]
                    dest_hash = hash_event(dest["event"])

                    logging.debug(f"Source event: {final_event}")
                    logging.debug(f"Destination event: {dest['event']}")

                    logging.debug(
                        f"Comparing event UID={norm_event.uid}: source hash={final_hash} vs dest hash={dest_hash}"
                    )

                    if final_hash != dest_hash:
                        logging.info(
                            f"Updating event UID={norm_event.uid} due to hash mismatch"
                        )
                        self.target.update_raw(dest["href"], raw_ical)
                        print(f"Updated event {raw_ical.to_ical().decode()}")
                    else:
                        logging.info(f"Event UID={norm_event.uid} unchanged")
                else:
                    logging.info(f"Creating new event UID={norm_event.uid}")
                    self.target.create(raw_ical)

            # Deletions (optional, policy-based)
            for uid, dest in dest_index.items():
                if uid not in source_uids:
                    logging.info(f"Deleting event UID={uid} not found in source")
                    self.target.delete(dest["href"])


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    config = SyncConfig(
        id=os.environ.get("SYNC_ID", "sync1"),
        destination=os.environ["CALDAV_DESTINATION"],
        username=os.environ["CALDAV_USERNAME"],
        password=os.environ["CALDAV_PASSWORD"],
        sources=[
            Source(
                type="ics",
                url=os.environ.get(
                    "ICS_SOURCE_URL",
                    "https://vorlesungsplan.stuvma.de/profiles/TINF23CS2",
                ),
                rules=[
                    Rule(
                        enabled=True,
                        name="Redact",
                        conditions=[
                            Condition(field="summary", operator="regex", value=".*")
                        ],
                        actions=[
                            Action(
                                type="set_field",
                                field={
                                    "name": "description",
                                    "value": "Viel Spaß in der Vorlesung!",
                                },
                            )
                        ],
                    )
                ],
            )
        ],
    )

    engine = SyncEngine(config)
    engine.run()
