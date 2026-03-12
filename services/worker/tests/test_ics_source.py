from unittest.mock import MagicMock, patch

_MINIMAL_ICS = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Test//Test//EN
BEGIN:VEVENT
UID:event-001@test
SUMMARY:Test Event
DESCRIPTION:A description
DTSTART:20260304T090000Z
DTEND:20260304T100000Z
END:VEVENT
END:VCALENDAR
"""

_TWO_EVENTS_ICS = """\
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:evt-1@test
SUMMARY:First Event
DESCRIPTION:Desc1
DTSTART:20260304T090000Z
DTEND:20260304T100000Z
END:VEVENT
BEGIN:VEVENT
UID:evt-2@test
SUMMARY:Second Event
DESCRIPTION:Desc2
DTSTART:20260304T110000Z
DTEND:20260304T120000Z
END:VEVENT
END:VCALENDAR
"""

_EMPTY_ICS = "BEGIN:VCALENDAR\nVERSION:2.0\nEND:VCALENDAR\n"


class TestIcsSource:
    def _mock_get(self, text: str):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.text = text
        mock_get = MagicMock(return_value=mock_resp)
        return mock_get

    def test_fetch_returns_one_normalized_event(self):
        from worker.sync.sources import IcsSource

        with patch("worker.sync.sources.requests.get", self._mock_get(_MINIMAL_ICS)):
            source = IcsSource("http://example.com/cal.ics")
            results = source.fetch()

        assert len(results) == 1
        norm, component = results[0]
        assert norm.uid == "event-001@test"
        assert norm.summary == "Test Event"
        assert norm.description == "A description"

    def test_fetch_returns_multiple_events(self):
        from worker.sync.sources import IcsSource

        with patch("worker.sync.sources.requests.get", self._mock_get(_TWO_EVENTS_ICS)):
            source = IcsSource("http://example.com/cal.ics")
            results = source.fetch()

        assert len(results) == 2
        uids = {r[0].uid for r in results}
        assert uids == {"evt-1@test", "evt-2@test"}

    def test_fetch_empty_calendar_returns_empty_list(self):
        from worker.sync.sources import IcsSource

        with patch("worker.sync.sources.requests.get", self._mock_get(_EMPTY_ICS)):
            source = IcsSource("http://example.com/empty.ics")
            results = source.fetch()

        assert results == []
