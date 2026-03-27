# Admin Guide

This document will show you how to install, configure and administrate chronicle.
Common mistakes are described if these are known.

## Containers

- `backend`: The backend (FastAPI) is the main component of chronicle. It provides the REST API for the frontend and other clients. It is built with FastAPI and runs on Uvicorn.
- `worker`: The worker is responsible for the synchronization of the data with the external sources. It is built with Python.
- `frontend`: The frontend is the user interface of chronicle. It is built with React and runs on a Node.js server.
- `postgres`: The database component of chronicle. It stores all the data of the application. It is a PostgreSQL database.
- `rabbitmq`: The message broker used for asynchronous tasks and communication between services. It is a RabbitMQ server.

For administration purposes:

- `pgadmin`: A web-based administration tool for managing the PostgreSQL database.

## Installation

To install chronicle, you need to have Docker or Podman installed on your system. You can then clone the repository and use the provided `compose.yml` file to set up the services.

```bash
docker compose -f compose.yaml up --build
```

The services should work out of the box with the provided configuration. You can access the frontend at `http://localhost:3000` and the pgAdmin interface at `http://localhost:8080`.

The worker, the database and the rabbitmq server should not be exposed to the outside world, as they are only needed for internal communication between the services.
For this purpose, the network `chronicle-internal` is used, which is only accessible by the services defined in the `compose.yml` file.

### Proxy

If you want to run the services on a server, you can use a reverse proxy like Nginx or Traefik to expose the frontend and the pgAdmin interface to the outside world. This way, you can access the services via a domain name instead of an IP address and port.

#### Production example with Treafik

```yaml
services:
    postgres:
        image: postgres:15
        environment:
            POSTGRES_USER: admin
            POSTGRES_PASSWORD: password
            POSTGRES_DB: appdb
        volumes:
            - postgres_data:/var/lib/postgresql/data
        healthcheck:
            test: ["CMD-SHELL", "pg_isready -U admin -d appdb"]
            interval: 5s
            timeout: 3s
            retries: 20
        networks:
            - chronicle-internal

    backend:
        build:
            context: .
            dockerfile: services/backend/Dockerfile
        environment:
            DATABASE_URL: postgresql://admin:password@postgres:5432/appdb
            ASYNC_DATABASE_URL: postgresql+asyncpg://admin:password@postgres:5432/appdb
            RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
        command: >
            sh -c "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"
        depends_on:
            postgres:
                condition: service_healthy
        networks:
            - chronicle-internal
            - traefik-services
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.backend.rule=Host(`api.chronicle.example.com`)"
            - "traefik.http.services.backend.loadbalancer.server.port=8000"

    rabbitmq:
        image: rabbitmq:3-management
        environment:
            RABBITMQ_DEFAULT_USER: guest
            RABBITMQ_DEFAULT_PASS: guest
        networks:
            - chronicle-internal

    frontend:
        build:
            context: .
            dockerfile: services/frontend/Dockerfile
        depends_on:
            - backend
        environment:
            API_URL: https://api.chronicle.example.com
        volumes:
            - ./services/frontend:/app
            - frontend_node_modules:/app/node_modules
        command: ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
        networks:
            - chronicle-internal
            - traefik-services
        labels:
            - "traefik.enable=true"
            - "traefik.http.routers.chronicle.rule=Host(`chronicle.example.com`)"
            - "traefik.http.services.chronicle.loadbalancer.server.port=3000"
    worker:
        build:
            context: .
            dockerfile: services/worker/Dockerfile
        depends_on:
            - rabbitmq
            - backend
        networks:
            - chronicle-internal
        environment:
            RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
volumes:
    postgres_data: {}
    frontend_node_modules: {}

networks:
    chronicle-internal:
        driver: bridge
    traefik-services:
        external: true
```

## Updates

To update chronicle, you can pull the latest changes from the repository and rebuild the services. This will ensure that you have the latest features and bug fixes.

```bashbash
git pull origin main
docker compose -f compose.yml up --build
```

### Database migrations

Alembic is used internally for database migrations.
When updating chronicle, the migrations are run automatically when you start the backend service, as the command includes `alembic upgrade head`. This ensures that the database schema is up to date with the latest version of the application.

## Troubleshooting
