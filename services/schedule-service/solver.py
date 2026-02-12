import datetime

from ortools.sat.python import cp_model

from models import Task, TaskEvent
from utils import datetime_to_schedule_time, schedule_time_to_datetime

DAY_DURATION_IN_MINUTES = 24 * 60


class SchedulingSolver:
    def __init__(
        self,
        horizon_duration,
        schedule_start: datetime.datetime,
        work_day=(9, 17),
        schedule_offset=0,
    ):
        self.model = cp_model.CpModel()
        self.horizon_in_mins = horizon_duration
        self.work_start, self.work_end = work_day
        self.schedule_offset = schedule_offset
        self.schedule_start = schedule_start
        self.all_intervals = []
        self.task_vars = []  # Store references to retrieve values later
        self.penalties = []

    def _get_working_minutes_domain(self):
        intervals = []

        # the solver starts at any time during the day (schedule_offset), so this must be compemsated when calculating the intervals
        if self.work_start < self.schedule_offset // 60 < self.work_end:
            intervals.append([0, self.work_end * 60 - self.schedule_offset])

        # now that the first interval is set correctly, we can focus on the intervals following todays day
        for day in range(
            1,
            (self.horizon_in_mins - (DAY_DURATION_IN_MINUTES - self.schedule_offset))
            // DAY_DURATION_IN_MINUTES,
        ):
            day_start = day * DAY_DURATION_IN_MINUTES - self.schedule_offset
            interval_start = day_start + self.work_start * 60
            interval_end = day_start + self.work_end * 60
            intervals.append([interval_start, interval_end])

        print(intervals)

        return cp_model.Domain.FromIntervals(intervals)

    def solve(self, tasks: list[Task], existing_meetings):
        work_domain = self._get_working_minutes_domain()

        # 1. Fixed Meetings (cannot overlap, threfore should be preprocessed)
        for m in existing_meetings:
            start = m["start_min"]
            duration = m["duration"]
            fixed_interval = self.model.new_fixed_size_interval_var(
                start, duration, f"meet_{start}"
            )
            self.all_intervals.append(fixed_interval)

        # 2. Flexible Tasks (no chunking)
        for task in tasks:
            suffix = f"{task.id}"
            start = self.model.new_int_var_from_domain(work_domain, f"start_{suffix}")
            end = self.model.new_int_var_from_domain(work_domain, f"end_{suffix}")
            interval = self.model.new_interval_var(
                start, task.duration, end, f"inter_{suffix}"
            )
            self.all_intervals.append(interval)
            self.task_vars.append({"id": task.id, "start": start, "end": end})

            if task.due_date:
                assert isinstance(task.due_date, int), (
                    "Due date must be an integer representing minutes from schedule start"
                )

                lateness = self.model.new_int_var(
                    0, self.horizon_in_mins, f"late_{suffix}"
                )
                self.model.add_max_equality(lateness, [0, end - task.due_date])
                self.penalties.append(lateness * task.priority)

                # self.model.add(end <= task.due_date)

        self.model.add_no_overlap(self.all_intervals)
        self.model.minimize(sum(self.penalties))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        status = solver.Solve(self.model)

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self._format_results(solver)
        return None

    def _format_results(self, solver):
        results = []
        for v in self.task_vars:
            start_val = solver.Value(v["start"])
            end_val = solver.Value(v["end"])
            results.append(
                TaskEvent(
                    id=v["id"],
                    title="",  # TODO add title to task_vars
                    start=schedule_time_to_datetime(start_val, self.schedule_start),
                    end=schedule_time_to_datetime(end_val, self.schedule_start),
                )
            )
        return sorted(results, key=lambda x: x.start)
