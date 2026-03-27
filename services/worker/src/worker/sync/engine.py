import hashlib
import logging
import re

from worker.sync.sources import IcsSource, BaseSource
from worker.sync.targets import CaldavTarget
from worker.models import NormalizedEvent
from chronicle_shared.models import Condition, Action, Rule, Source, Profile


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
        event.uid,
        event.summary,
        event.description,
        event.dtstart.isoformat(),
        event.dtend.isoformat(),
    )

    logging.debug(f"Canonical representation for hashing: {canonical}")

    return hashlib.sha256(repr(canonical).encode()).hexdigest()


class SyncEngine:
    def __init__(self, config: Profile):
        logging.info(
            f"Initializing SyncEngine for destination: {config.main_calendar.url}"
        )
        self.sources: list[tuple[BaseSource, Source]] = []
        for source in config.sources:
            if source.calendar.type == "ical":
                self.sources.append((IcsSource(source.calendar.url), source))
                logging.info(f"Added ICS source: {source.calendar.url}")
            else:
                logging.error(f"Unsupported source type: {source.calendar.type}")
                raise ValueError(f"Unsupported source type: {source.calendar.type}")
        self.target = CaldavTarget(
            config.main_calendar.url,
            config.main_calendar.username,
            config.main_calendar.password,
        )

    def run(self):
        logging.info("Starting sync run...")
        for source, source_config in self.sources:
            logging.info(f"Processing source: {source_config.calendar.url}")
            source_events = source.fetch()
            dest_index = self.target.build_index()

            source_uids = set()

            for norm_event, source_event in source_events:
                # Generate our own UID based on a hash of the event's canonical data
                our_uid = str(norm_event.uid) + "@" + source_config.id + ".chronicle"
                source_uids.add(our_uid)

                # Apply rules to get the final event data that we want to represent in the destination calendar
                final_event = apply_rules(norm_event, source_config.rules)

                # Set our own UID in both the normalized event and the raw iCal component
                final_event.uid = our_uid
                source_event["UID"] = our_uid

                # Hash the final event data to detect changes later
                final_hash = hash_event(final_event)

                # apply the final event data to the raw iCal component for updating/creating
                source_event["SUMMARY"] = final_event.summary
                source_event["DESCRIPTION"] = final_event.description
                # raw_ical["DTSTART"] = final_event.dtstart
                # raw_ical["DTEND"] = final_event.dtend
                source_event["X-CHRONICLE-SOURCE"] = source_config.id
                source_event["X-CHRONICLE"] = True

                if our_uid in dest_index:
                    dest = dest_index[our_uid]
                    dest_hash = hash_event(dest["event"])

                    logging.debug(f"Source event: {final_event}")
                    logging.debug(f"Destination event: {dest['event']}")

                    logging.debug(
                        f"Comparing event UID={our_uid}: source hash={final_hash} vs dest hash={dest_hash}"
                    )

                    if final_hash != dest_hash:
                        logging.info(
                            f"Updating event UID={our_uid} due to hash mismatch"
                        )
                        self.target.update_raw(dest["href"], source_event)
                        print(f"Updated event {source_event.to_ical().decode()}")
                    else:
                        logging.info(f"Event UID={our_uid} unchanged")
                else:
                    logging.info(f"Creating new event UID={our_uid}")
                    self.target.create(source_event)

            # Deletions (optional, policy-based)
            # Only delete events that were created by this source (check X-CHRONICLE-SOURCE)
            for uid, dest in dest_index.items():
                logging.debug(f"Checking if destination event UID={uid} needs deletion")
                if uid not in source_uids:
                    # Only delete if the event has X-CHRONICLE-SOURCE matching this source
                    raw_event = self.target.calendar.event_by_url(
                        dest["href"]
                    ).component
                    if str(raw_event.get("X-CHRONICLE-SOURCE", "")) == source_config.id:
                        logging.info(
                            f"Deleting event UID={uid} not found in source {source_config.id}"
                        )
                        self.target.delete(dest["href"])
