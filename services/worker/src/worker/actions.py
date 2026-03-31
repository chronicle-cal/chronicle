import logging

from chronicle_shared.models import Profile

from worker.sync.engine import SyncEngine
from worker.sched.scheduler import update_schedule


def sync(payload):
    logging.info(f"Starting sync with payload: {payload}")
    try:
        profile_payload = dict(payload)
        work_day = (
            int(profile_payload.pop("workday_start_hour")),
            int(profile_payload.pop("workday_end_hour")),
        )

        config = Profile.model_validate(profile_payload)
        engine = SyncEngine(config)
        engine.run()

        logging.info("Sync completed successfully, starting schedule update")
        # Schedule the tasks
        update_schedule(engine.target, config.tasks, work_day=work_day)
    except Exception as e:
        logging.error(f"Sync failed: {e}")
