from worker.models import Source, Rule, SyncConfig, Condition, Action
import os


def fetch_sync_config_by_user(user_id: str):
    # Placeholder: Fetch sync config from DB based on user_id
    return SyncConfig(
        id="sync1",
        destination=os.environ["CALDAV_DESTINATION"],
        username=os.environ["CALDAV_USERNAME"],
        password=os.environ["CALDAV_PASSWORD"],
        sources=[
            Source(
                id="source1",
                type="ics",
                url="https://vorlesungsplan.stuvma.de/profiles/TINF23CS2",
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
            ),
        ],
    )
