#!/usr/bin/env python
import pika
import sys
import os
import json
import logging
import time
import signal
from worker import actions

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# Define your actions here
def action_print(body):
    logging.info(f"[ACTION] Printing: {body}")


def action_long_task(body):
    logging.info(f"[ACTION] Starting long task with: {body}")
    time.sleep(10)
    logging.info(f"[ACTION] Finished long task with: {body}")


# Map message types to actions
ACTIONS = {"print": action_print, "long_task": action_long_task, "sync": actions.sync}


def run_action(action, body):
    try:
        action(body)
    except Exception as e:
        logging.error(f"Action failed: {e}")


def get_connection():
    host = os.getenv("RABBITMQ_HOST", "localhost")
    retries = 5
    for _ in range(retries):
        try:
            return pika.BlockingConnection(pika.ConnectionParameters(host=host))
        except Exception as e:
            logging.error(f"Connection failed: {e}, retrying...")
            time.sleep(2)
    logging.critical("Could not connect to RabbitMQ after retries.")
    sys.exit(1)


def main():
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue="worker", durable=True)

    def callback(ch, method, properties, body):
        try:
            msg = json.loads(body)
            action_type = msg.get("type")
            action = ACTIONS.get(action_type)
            if action:
                run_action(action, msg.get("payload"))
            else:
                logging.warning(f"Unknown action type: {action_type}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Failed to process message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="worker", on_message_callback=callback)

    logging.info(" [*] Waiting for messages. To exit press CTRL+C")

    def shutdown(signum, frame):
        logging.info("Shutting down...")
        channel.stop_consuming()
        connection.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        channel.start_consuming()
    except Exception as e:
        logging.critical(f"Consumer crashed: {e}")
        connection.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
