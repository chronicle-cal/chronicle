# Admin Guide

This document will show you how to install, configure and administrate chronicle.
Common mistakes are described if these are known.

## Installation

To install chronicle, you need to have Docker (or Podman) installed on your system. 

1. Clone the repository 

```bash
git clone https://github.com/chronicle-cal/chronicle.git
```
2. Create a `.env` file based on `.env.example`.

3. Launch chronicle using Docker

```bash
docker compose -f compose.yaml up --build -d
```

4. Access the services:
- Frontend: `http://localhost:3000` 
- Backend API docs: `http://localhost:8000/docs` 
- RabbitMQ management: `http://localhost:15672` (credentials defined in `.env`)

## Services

- `backend`: Provides the REST API (FastAPI)
- `worker`: Handles background jobs and synchronization
- `frontend`: React application built with Vite and served via Nginx
- `postgres`: PostgreSQL database storing application data
- `rabbitmq`: Message broker for asynchronous communication

## Logs

View logs for all services:

```bash
docker compose logs -f
# docker compose logs -f <service-name>
```

## Service Management

Stop all containers:
```bash
docker compose -f compose.yaml down
```

Restart services:
```bash
docker compose restart
```

### Proxy

For server deployments, use a reverse proxy such as Nginx or Traefik to expose the required public services via domain names and HTTPS.

## Updates

To update chronicle, you can pull the latest changes from the repository and rebuild the services. This will ensure that you have the latest features and bug fixes.

```bash
git pull origin main
docker compose -f compose.yaml up --build
```

## Production Deployment

For production use, Chronicle should be deployed behind a reverse proxy (e.g. Nginx or Traefik) with HTTPS enabled.

Only the frontend (and optionally the backend API) should be exposed to the outside world. Internal services such as PostgreSQL, RabbitMQ and the worker should not be publicly accessible.

Configuration is managed via the `.env` file and should be adapted for the target environment.

Make sure that persistent storage is configured for the PostgreSQL database to prevent data loss.

## Database migrations

Alembic is used internally for database migrations.
When updating chronicle, the migrations are run automatically when you start the backend service, as the command includes `alembic upgrade head`. This ensures that the database schema is up to date with the latest version of the application.

## Troubleshooting

### Services not starting
- Check logs
```bash
docker compose logs
```

### Backend Errors
- Verify container is running
- Health check: `http://localhost:8000/api/health`

### Worker / Sync not working
- Check worker logs:
```bash
  docker compose logs -f worker
```
- Verify RabbitMQ is running
- Restart services if needed
