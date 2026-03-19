# Chronicle Worker

This is the worker service for Chronicle. It is responsible for processing tasks that are added to the queue by the API service.

## Development

To run the worker service locally, you can use the following command:

```bash
uv run --env-file .env worker
```

Make sure to create a `.env` file in the `services/worker` directory with the following content:

```env
RABBITMQ_URL=amqp://localhost
RABBITMQ_QUEUE=task_queue
RABBITMQ_PREFETCH_COUNT=1
```

and of course a RabbitMQ instance running locally. You can use Docker to run RabbitMQ:

```bash
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## Testing

To run the tests for the worker service, you can use the following command:

```bash
uv run pytest .
```
