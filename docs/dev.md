# Development Guide

## Requirements

- Docker / Podman
- Python (backend / worker)
- uv 
- Node.js (frontend)

## Local Development

You can either run Chronicle using Docker (recommended) or run services individually for development.

### Using Docker

```bash
docker compose -f compose.yaml up --build -d
```

### Backend
```bash
cd services/backend
uv sync
uv run uvicorn app.main:app --reload
```

The backend will be available at: `http://localhost:8000`

### Frontend
```bash
cd services/frontend
npm install
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## Environment Configuration

Environment variables are defined in: `.env.example`

## API Client Generation (Frontend)

The frontend uses a generated API client based on the backend OpenAPI specification.

If the backend API changes, you must regenerate the client. Run this command from the `services/frontend` directory.

```bash
npx @openapitools/openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g typescript-axios \
  -o src/api-client
```

Make sure the backend is running before executing this command.

The generated client is used by the frontend to interact with the backend API.

After regenerating the client, restart the frontend development server.

## Code Quality

Pre-commit hooks are used for:

- linting
- formatting
- basic checks

Configuration:

`./.pre-commit-config.yaml`

CI/CD workflows are located in: `.github/workflows/`

### Testing

Run all tests:

```bash
cd services/backend
pytest tests/ -v
```

**Run specific test:**

```bash
pytest tests/test_integration.py::test_create_sync_config -v
```

**Coverage report:**

```bash
pytest tests/ --cov --cov-report=term-missing
```

## Database Migration

### Alembic

Alembic is used for database migrations.

If database models are changed, create and apply a new migration before committing:

Create a migration:

```bash
alembic revision -m "describe your change"
```

Apply migrations:
```bash
alembic upgrade head
```

Check current state:
```bash
alembic history
alembic current
```

Rollback (if needed):
```bash
alembic downgrade -1
```

## API

The available endpoints can be accessed via the Swagger UI: `http://localhost:8000/docs`


## File Structure

<!-- tree -L 2-->

```bash
├── CHANGELOG.md
├── compose.yaml
├── docs
│   ├── admin.md
│   ├── architecture
│   ├── dev.md
│   ├── readme.md
│   └── user.md
├── LICENSE
├── package-lock.json
├── packages
│   └── chronicle-shared
├── README.md
├── release-please-config.json
├── scripts
│   ├── smoke
│   ├── update_version.sh
│   └── worker
├── services
│   ├── backend
│   ├── frontend
│   └── worker
└── version.txt
```

**docs:**
Docs for User, Dev and Admin

**scripts:**
Various scripts required for this project

**services:**
Includes the main parts of this repo.
Split into:

- backend
- frontend
- worker
