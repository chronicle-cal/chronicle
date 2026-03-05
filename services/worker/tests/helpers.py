import datetime
import sys
import os
from worker.models import Action, Condition, NormalizedEvent, Rule

_WORKER_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_WORKER_DIR, "../.."))

for _p in (_WORKER_DIR, _PROJECT_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)


_T0 = datetime.datetime(2026, 3, 4, 9, 0, tzinfo=datetime.timezone.utc)
_T1 = datetime.datetime(2026, 3, 4, 10, 0, tzinfo=datetime.timezone.utc)


def make_event(**kwargs) -> NormalizedEvent:
    defaults = dict(
        uid="uid-1",
        summary="Test Event",
        description="Test Description",
        dtstart=_T0,
        dtend=_T1,
    )
    defaults.update(kwargs)
    return NormalizedEvent(**defaults)  # type: ignore


def make_rule(
    enabled=True,
    conditions=None,
    actions=None,
    name="test-rule",
) -> Rule:
    return Rule(
        enabled=enabled,
        name=name,
        conditions=conditions
        or [Condition(field="summary", operator="equals", value="Match")],
        actions=actions
        or [
            Action(
                type="set_field",
                field={"name": "description", "value": "Applied"},
            )
        ],
    )
