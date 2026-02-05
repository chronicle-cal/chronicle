# Chronicle

Web based calendar tools featuring calendar syncs and smart scheduling.

## Development

### Dev setup

First start the development components (Database, DB Admin, RabbitMQ) with

```bash
podman-compose -f dev-compose.yaml up --build
```

You can then access PgAdmin on http://localhost:5050 .

### API Gateway

Enter the directory `services/api-gateway` and run 
```
source .venv/bin/activate
uv run fastapi --app app
```

### Scheduling Service

Enter the directory `services/scheduling` and run 
```
source .venv/bin/activate
uv run main.py
```

## Services

### API Gateway

-   Recieves HTTP (WS) API queries
-   Validates Data with DTOs (pydantic)
-   Dispatches actions to other services (RabbitMQ)
-   Returns results 

### Integrator Service
-   Reads external Calendars (ical, CalDAV, Google?) and writes events to database
-   Writes events to external Calendars (CalDAV, Google)

### Scheduling Service
-     The Scheduling Service runs on the data in the database ()

### Task Service
-   

### Notification Service
-   Sends user notifications (via E-Mail, SMS, Telegram, etc.)

## Shared 
Shared is a python package that all services depend on. It includes the defintions for the DTOs

## Configuration
Each service gets a the same config file which includes the addresses of all other services as well as installation options