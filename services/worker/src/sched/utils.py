import datetime


def datetime_to_schedule_time(
    timestamp: datetime.datetime, schedule_start_time: datetime.datetime
):
    """
    Converts a datetime timestamp to the number of minutes elapsed since a given schedule start time.

    Args:
        timestamp (datetime.datetime): The datetime to convert.
        schedule_start_time (datetime.datetime): The reference start time of the schedule.

    Returns:
        int: The number of minutes between the schedule start time and the given timestamp.
    """
    return int((timestamp - schedule_start_time).total_seconds() // 60)


def schedule_time_to_datetime(
    schedule_time: int, schedule_start_time: datetime.datetime
):
    """
    Converts a schedule time (minutes since schedule start) back to a datetime object.

    Args:
        schedule_time (int): The number of minutes since the schedule start time.
        schedule_start_time (datetime.datetime): The reference start time of the schedule.

    Returns:
        datetime.datetime: The corresponding datetime object.
    """
    return schedule_start_time + datetime.timedelta(minutes=schedule_time)
