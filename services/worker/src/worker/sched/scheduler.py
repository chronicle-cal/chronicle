import datetime
import logging
from worker.sched.solver import SchedulingSolver
from chronicle_shared.models import Task
from worker.sched.utils import datetime_to_schedule_time
from icalendar import Event
from uuid import uuid4

from worker.sync.targets import CaldavTarget

HORIZON = datetime.timedelta(weeks=2)

TZ_INFO = datetime.datetime.now().astimezone().tzinfo


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


def update_schedule(target: CaldavTarget, tasks: list[Task]):
    schedule_start, schedule_end = calc_schedule_start_end(HORIZON)
    logging.info(
        f"Calculated schedule start: {schedule_start}, schedule end: {schedule_end}"
    )

    # clear the schedule by deleting all previously created events (identified by X-CHRONICLE-TASK)
    target.clear_task_events()

    # get all the events from the database that are between schedule start and schedule end
    events = target.get_events_between(schedule_start, schedule_end)

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

    logging.info(solver_events)

    solver_tasks = tasks.copy()

    for task in tasks:
        logging.info(
            f"Task: {task.title}, duration: {task.duration}, due_date: {task.due_date}"
        )
        if task.due_date:
            task.due_date = datetime_to_schedule_time(task.due_date, schedule_start)
        if task.not_before:
            task.not_before = datetime_to_schedule_time(task.not_before, schedule_start)

    horizon_duration_in_minutes = 14 * 24 * 60

    logging.info(horizon_duration_in_minutes)
    logging.info(schedule_start.hour * 60 + schedule_start.minute)

    solver = SchedulingSolver(
        horizon_duration=horizon_duration_in_minutes,
        schedule_start=schedule_start,
        work_day=(9, 17),
        schedule_offset=schedule_start.hour * 60 + schedule_start.minute,
    )

    logging.info("Starting solver")
    schedule = solver.solve(solver_tasks, solver_events)
    logging.info("Solver finished")
    # print(schedule)

    if not schedule:
        logging.warning("No valid schedule found")
        return

    # for item in schedule:
    #     logging.info(item)

    # delete all events that have X-CHRONICLE-TASK set
    # create new events for each task in the schedule, setting X-CHRONICLE-TASK to the task id
    logging.info("Updating calendar with new schedule")

    # Get existing events with X-CHRONICLE-TASK and delete them
    # existing_events = calendar.search()
    # for event in existing_events:
    #     if event.component.get("X-CHRONICLE-TASK"):
    #         logging.info(
    #             f"Deleting existing scheduled event: {event.component.get('summary')}"
    #         )
    #         event.delete()

    for task_event in schedule:
        event = Event()
        event.add("summary", task_event.title)
        event.add("description", task_event.description or "")
        event.add("dtstart", task_event.start)
        event.add("dtend", task_event.end)
        event.add("uid", str(uuid4()))
        event.add("X-CHRONICLE-TASK", task_event.id)
        event.add("X-CHRONICLE", "True")

        target.create(event)

        logging.info(
            f"Created event for task: {task_event.title}, start: {task_event.start}, end: {task_event.end}"
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s"
    )

    logging.info("Starting scheduler")
    logging.info(f"Timezone: {TZ_INFO}")

    """
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
    """
