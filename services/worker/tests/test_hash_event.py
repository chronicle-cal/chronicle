from helpers import make_event, _T0
import datetime
from worker.sync.engine import hash_event


class TestHashEvent:
    def test_same_event_produces_same_hash(self):
        event = make_event()
        assert hash_event(event) == hash_event(event)

    def test_different_summary_produces_different_hash(self):
        e1 = make_event(summary="A")
        e2 = make_event(summary="B")
        assert hash_event(e1) != hash_event(e2)

    def test_different_description_produces_different_hash(self):
        e1 = make_event(description="A")
        e2 = make_event(description="B")
        assert hash_event(e1) != hash_event(e2)

    def test_different_uid_produces_different_hash(self):
        e1 = make_event(uid="uid-1")
        e2 = make_event(uid="uid-2")
        assert hash_event(e1) != hash_event(e2)

    def test_different_dtstart_produces_different_hash(self):
        e1 = make_event(dtstart=_T0)
        e2 = make_event(dtstart=_T0 + datetime.timedelta(hours=1))
        assert hash_event(e1) != hash_event(e2)
