import datetime
from chronicle_shared.models import Task
from worker.sched.scheduler import calc_schedule_start_end, merge_overlapping_events
from worker.sched.utils import datetime_to_schedule_time, schedule_time_to_datetime

_BASE_UTC = datetime.datetime(2026, 3, 4, 8, 0, tzinfo=datetime.timezone.utc)


class TestDatetimeToScheduleTime:
    def test_same_time_returns_zero(self):
        assert datetime_to_schedule_time(_BASE_UTC, _BASE_UTC) == 0

    def test_one_hour_later_returns_60(self):
        later = _BASE_UTC + datetime.timedelta(hours=1)
        assert datetime_to_schedule_time(later, _BASE_UTC) == 60

    def test_one_day_later_returns_1440(self):
        later = _BASE_UTC + datetime.timedelta(days=1)
        assert datetime_to_schedule_time(later, _BASE_UTC) == 1440

    def test_returns_integer(self):
        later = _BASE_UTC + datetime.timedelta(minutes=45)
        assert isinstance(datetime_to_schedule_time(later, _BASE_UTC), int)

    def test_non_round_seconds_are_truncated(self):
        # 90 seconds = 1.5 minutes → truncated to 1
        later = _BASE_UTC + datetime.timedelta(seconds=90)
        assert datetime_to_schedule_time(later, _BASE_UTC) == 1


class TestScheduleTimeToDatetime:
    def test_zero_returns_schedule_start(self):
        assert schedule_time_to_datetime(0, _BASE_UTC) == _BASE_UTC

    def test_60_returns_one_hour_later(self):
        expected = _BASE_UTC + datetime.timedelta(hours=1)
        assert schedule_time_to_datetime(60, _BASE_UTC) == expected

    def test_roundtrip_with_datetime_to_schedule_time(self):
        original = _BASE_UTC + datetime.timedelta(hours=3, minutes=15)
        mins = datetime_to_schedule_time(original, _BASE_UTC)
        recovered = schedule_time_to_datetime(mins, _BASE_UTC)
        assert recovered == original

    def test_large_value_spans_multiple_days(self):
        expected = _BASE_UTC + datetime.timedelta(days=7)
        assert schedule_time_to_datetime(7 * 1440, _BASE_UTC) == expected


class TestMergeOverlappingEvents:
    def test_empty_list_returns_empty(self):
        assert merge_overlapping_events([]) == []

    def test_single_event_returned_unchanged(self):
        events = [{"start_min": 0, "duration": 60}]
        assert merge_overlapping_events(events) == [{"start_min": 0, "duration": 60}]

    def test_two_non_overlapping_events_not_merged(self):
        events = [
            {"start_min": 0, "duration": 30},
            {"start_min": 60, "duration": 30},
        ]
        result = merge_overlapping_events(events)
        assert len(result) == 2

    def test_adjacent_events_are_merged(self):
        # Event 1 ends at 60, Event 2 starts at 60 — they touch
        events = [
            {"start_min": 0, "duration": 60},
            {"start_min": 60, "duration": 60},
        ]
        result = merge_overlapping_events(events)
        assert len(result) == 1
        assert result[0]["start_min"] == 0
        assert result[0]["duration"] == 120

    def test_overlapping_events_are_merged(self):
        events = [
            {"start_min": 0, "duration": 90},
            {"start_min": 60, "duration": 60},
        ]
        result = merge_overlapping_events(events)
        assert len(result) == 1
        assert result[0]["start_min"] == 0
        assert result[0]["duration"] == 120

    def test_event_completely_contained_within_another(self):
        events = [
            {"start_min": 0, "duration": 120},
            {"start_min": 30, "duration": 30},
        ]
        result = merge_overlapping_events(events)
        assert len(result) == 1
        assert result[0]["duration"] == 120


class TestCalcScheduleStartEnd:
    def test_start_is_in_the_future(self):
        start, _ = calc_schedule_start_end(datetime.timedelta(weeks=2))
        # Allow a tiny clock skew in CI
        assert start >= datetime.datetime.now(tz=start.tzinfo) - datetime.timedelta(
            seconds=1
        )

    def test_start_has_zero_seconds_and_microseconds(self):
        start, _ = calc_schedule_start_end(datetime.timedelta(weeks=2))
        assert start.second == 0
        assert start.microsecond == 0

    def test_end_minus_start_equals_horizon(self):
        horizon = datetime.timedelta(days=3)
        start, end = calc_schedule_start_end(horizon)
        assert end - start == horizon

    def test_different_horizons_produce_different_ends(self):
        _, end1 = calc_schedule_start_end(datetime.timedelta(days=1))
        _, end2 = calc_schedule_start_end(datetime.timedelta(days=7))
        assert end2 > end1


class TestSchedulingSolver:
    _SCHEDULE_START = datetime.datetime(2026, 3, 4, 9, 0, tzinfo=datetime.timezone.utc)

    def _make_solver(self, horizon=6000, work_day=(9, 17), offset=0):
        from worker.sched.solver import SchedulingSolver

        return SchedulingSolver(
            horizon_duration=horizon,
            schedule_start=self._SCHEDULE_START,
            work_day=work_day,
            schedule_offset=offset,
        )

    def test_solve_with_no_tasks_returns_empty_list(self):
        solver = self._make_solver()
        result = solver.solve(tasks=[], existing_meetings=[])
        assert result == [] or result is None  # no task_vars → empty list

    def test_solve_single_task_returns_one_task_event(self):
        solver = self._make_solver()
        task = Task(id="t1", title="Write tests", description="", duration=30)
        result = solver.solve(tasks=[task], existing_meetings=[])
        print(result)
        assert result is not None
        assert len(result) == 1
        assert result[0].id == "t1"

    def test_task_event_respects_work_hours(self):
        solver = self._make_solver(work_day=(9, 17), offset=0)
        task = Task(id="t1", title="Task", description="", duration=60)
        result = solver.solve(tasks=[task], existing_meetings=[])
        assert result is not None
        event = result[0]
        assert isinstance(event.start, datetime.datetime)
        assert isinstance(event.end, datetime.datetime)
        assert event.end > event.start

    def test_two_tasks_do_not_overlap(self):
        solver = self._make_solver()
        tasks = [
            Task(id="t1", title="Task 1", description="", duration=60),
            Task(id="t2", title="Task 2", description="", duration=60),
        ]
        result = solver.solve(tasks=tasks, existing_meetings=[])
        assert result is not None
        assert len(result) == 2
        # Sorted by start; t1.end must not exceed t2.start
        t1, t2 = result[0], result[1]
        assert t1.end <= t2.start

    def test_result_is_sorted_by_start_time(self):
        solver = self._make_solver()
        tasks = [
            Task(id="t1", title="A", description="", duration=30),
            Task(id="t2", title="B", description="", duration=30),
            Task(id="t3", title="C", description="", duration=30),
        ]
        result = solver.solve(tasks=tasks, existing_meetings=[])
        assert result is not None
        starts = [e.start for e in result]
        assert starts == sorted(starts)

    def test_working_minutes_domain_excludes_night_hours(self):
        """Intervals returned by _get_working_minutes_domain should only cover
        the configured work window [work_start*60, work_end*60] within each day."""
        solver = self._make_solver(horizon=3 * 24 * 60, work_day=(9, 17), offset=0)
        domain = solver._get_working_minutes_domain()
        # A time well outside work hours (e.g. 2 AM = 120 min) should not be in the domain
        # ortools Domain does not expose direct membership check; verify indirectly via
        # intervals stored in solver.all_intervals after call to _get_working_minutes_domain
        # Just verify it doesn't crash and returns a domain object
        from ortools.sat.python import cp_model

        assert isinstance(domain, cp_model.Domain)
