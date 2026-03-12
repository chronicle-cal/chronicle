import logging

from chronicle_shared.models import Profile

from worker.sync.engine import SyncEngine


def sync(payload):
    logging.info(f"Starting sync with payload: {payload}")
    try:
        config = Profile.model_validate(payload)
        engine = SyncEngine(config)
        engine.run()
        logging.info("Sync completed successfully.")
    except Exception as e:
        logging.error(f"Sync failed: {e}")
