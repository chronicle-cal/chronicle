# Chronicle Worker

This is the worker service for Chronicle. It is responsible for processing tasks that are added to the queue by the API service.

## Development

To run the worker service locally, you can use the following command:

```bash
uv run worker
```

Make sure to set the `RABBITMQ_URL` variable in the `.env` file in the root directory with the following content, and of course to have a RabbitMQ instance running locally. You can use Docker to run RabbitMQ:

```bash
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

## Testing

To run the tests for the worker service, you can use the following command:

```bash
uv run pytest .
```
