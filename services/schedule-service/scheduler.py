import datetime
import logging
import os
from solver import SchedulingSolver
import caldav

from models import Task, SchedulerConfig
from utils import datetime_to_schedule_time, schedule_time_to_datetime

HORIZON = datetime.timedelta(weeks=2)

TZ_INFO = datetime.datetime.now().astimezone().tzinfo


def get_events_between(
    start: datetime.datetime,
    end: datetime.datetime,
    caldav_url: str,
    username: str,
    password: str,
):
    with caldav.DAVClient(
        url=caldav_url,
        username=username,
        password=password,
    ) as client:
        calendar = client.calendar(url=caldav_url)
        events = calendar.date_search(start, end)
        print(events)
        return events


def calc_schedule_start_end(horizon: datetime.timedelta):
    now = datetime.datetime.now(tz=TZ_INFO).replace(second=0, microsecond=0)
    minute = (now.minute // 15 + 1) * 15
    if minute == 60:
        schedule_start = (now + datetime.timedelta(hours=1)).replace(minute=0)
    else:
        schedule_start = now.replace(minute=minute)
    schedule_end = schedule_start + horizon
    return schedule_start, schedule_end


def merge_overlapping_events(events):
    if not events:
        return []

    # Sort events by start time
    events.sort(key=lambda x: x["start_min"])
    merged_events = [events[0]]

    for current in events[1:]:
        last_merged = merged_events[-1]
        if current["start_min"] <= last_merged["start_min"] + last_merged["duration"]:
            # Overlapping events, merge them
            last_merged["duration"] = max(
                last_merged["duration"],
                current["start_min"] + current["duration"] - last_merged["start_min"],
            )
        else:
            # No overlap, add to merged list
            merged_events.append(current)

    return merged_events


def update_schedule(scheduler_config: SchedulerConfig):

    schedule_start, schedule_end = calc_schedule_start_end(HORIZON)
    logging.info(
        f"Calculated schedule start: {schedule_start}, schedule end: {schedule_end}"
    )

    # get all the events from the database that are between schedule start and schedule end
    events = get_events_between(
        schedule_start,
        schedule_end,
        scheduler_config.calendar_url,
        scheduler_config.calendar_username,
        scheduler_config.calendar_password,
    )

    for event in events:
        logging.info(
            f"Event: {event.component.get('summary')}, start: {event.component.get('dtstart').dt}, end: {event.component.get('dtend').dt}"
        )
        logging.info(
            datetime_to_schedule_time(event.component["dtstart"].dt, schedule_start)
        )

    # strip the events down to start and duration for the solver
    # TODO figure out what happens when we have an event that starts before the schedule start but ends after the schedule start, or an event that starts before the schedule end but ends after the schedule end
    solver_events = [
        {
            "start_min": datetime_to_schedule_time(
                event.component["dtstart"].dt, schedule_start
            ),
            "duration": datetime_to_schedule_time(
                event.component["dtend"].dt, schedule_start
            )
            - datetime_to_schedule_time(event.component["dtstart"].dt, schedule_start),
        }
        for event in events
    ]

    solver_events = merge_overlapping_events(solver_events)

    print(solver_events)

    solver_tasks = scheduler_config.tasks.copy()

    for task in scheduler_config.tasks:
        logging.info(
            f"Task: {task.title}, duration: {task.duration}, due_date: {task.due_date}"
        )
        if task.due_date:
            task.due_date = datetime_to_schedule_time(task.due_date, schedule_start)
        if task.not_before:
            task.not_before = datetime_to_schedule_time(task.not_before, schedule_start)

    horizon_duration_in_minutes = 14 * 24 * 60

    print(horizon_duration_in_minutes)
    print(schedule_start.hour * 60 + schedule_start.minute)

    solver = SchedulingSolver(
        horizon_duration=horizon_duration_in_minutes,
        schedule_start=schedule_start,
        work_day=(9, 17),
        schedule_offset=schedule_start.hour * 60 + schedule_start.minute,
    )

    print("Starting solver")
    schedule = solver.solve(solver_tasks, solver_events)
    print("Solver finished")
    # print(schedule)

    if not schedule:
        logging.warning("No valid schedule found")
        return

    for item in schedule:
        print(item)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s"
    )

    logging.info("Starting scheduler")
    logging.info(f"Timezone: {TZ_INFO}")

    config = SchedulerConfig(
        id="sched1",
        name="Test Scheduler",
        calendar_url=os.environ["CALDAV_DESTINATION"],
        calendar_username=os.environ["CALDAV_USERNAME"],
        calendar_password=os.environ["CALDAV_PASSWORD"],
        tasks=[
            Task(
                id="task1",
                title="Task 1",
                description="First task",
                due_date=datetime.datetime(
                    2026, 2, 13, 9, 0, tzinfo=datetime.timezone.utc
                ),
                duration=60,
            ),
            Task(
                id="task2",
                title="Task 2",
                description="Second task",
                due_date=datetime.datetime(
                    2026, 2, 18, 17, 0, tzinfo=datetime.timezone.utc
                ),
                duration=120,
            ),
        ],
    )

    update_schedule(config)

    # get the current date and time
