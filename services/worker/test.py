import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="worker_queue")

payload = {"type": "print", "payload": {"user_id": "12345"}}

channel.basic_publish(exchange="", routing_key="worker", body=json.dumps(payload))

print(" [x] Sent 'Hello World!'")
connection.close()
