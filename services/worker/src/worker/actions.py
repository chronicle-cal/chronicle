import logging

from chronicle_shared.models import Profile

from worker.sync.engine import SyncEngine
from worker.sched.scheduler import update_schedule


def sync(payload):
    logging.info(f"Starting sync with payload: {payload}")
    try:
        config = Profile.model_validate(payload)
        engine = SyncEngine(config)
        engine.run()

        logging.info("Sync completed successfully, starting schedule update")
        # Schedule the tasks
        update_schedule(engine.target, config.tasks)
    except Exception as e:
        logging.error(f"Sync failed: {e}")
