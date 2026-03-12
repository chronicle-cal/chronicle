from app import models
import chronicle_shared.models as shared_models


def _calendar_to_shared_calendar(calendar: models.Calendar) -> shared_models.Calendar:
    return shared_models.Calendar(
        id=calendar.id,
        type=calendar.type,
        url=calendar.url,
        username=calendar.username,
        password=calendar.password,
    )


def _source_to_shared_source(source: models.CalendarSource) -> shared_models.Source:
    return shared_models.Source(
        id=source.id,
        calendar=_calendar_to_shared_calendar(source.calendar),
        rules=[
            shared_models.Rule(
                enabled=rule.enabled,
                name=rule.name,
                conditions=[
                    shared_models.Condition(
                        field=condition.field,
                        operator=condition.operator,
                        value=condition.value,
                    )
                    for condition in rule.conditions
                ],
                actions=[
                    shared_models.Action(
                        type=action.type,
                        field=action.field,
                    )
                    for action in rule.actions
                ],
            )
            for rule in source.rules
        ],
    )


def profile_to_shared_profile(profile: models.CalendarProfile) -> shared_models.Profile:
    return shared_models.Profile(
        id=profile.id,
        name=profile.name,
        main_calendar=_calendar_to_shared_calendar(profile.main_calendar),
        tasks=[],
        sources=[
            _source_to_shared_source(source) for source in profile.calendar_sources
        ],
    )
