from worker.db import fetch_sync_config_by_user
import logging

from worker.sync.engine import SyncEngine


def sync(payload):
    logging.info(f"Starting sync with payload: {payload}")
    try:
        config = fetch_sync_config_by_user(payload["user_id"])
        engine = SyncEngine(config)
        engine.run()
        logging.info("Sync completed successfully.")
    except Exception as e:
        logging.error(f"Sync failed: {e}")
