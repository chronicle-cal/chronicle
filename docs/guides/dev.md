# Docs/Dev

## Requirements
Copy from admin.md

## Local Startup / Usage
Copy Usage from Admin.md

## Config / Enviroment
To dev a venv is needet:
```bash
uv sync
```

The .env variables are stored inside `services/backend/.env.example`

## Consistency Checks
All tests, lintings and formating checks do run with the pre commit hook. After `git push`there are also checked in the CI/CD Pipeline in GitHub.

**Pre-Commit-Hook**:
`./.pre-commit-config.yaml`

**CI/CD Workflows are saved in `.github/workflows/`

### Testing
**Run all tests:**
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


## Updates
### Database - Alembic
To keep the DB stable and healthy Alembic is used.

If models of the db are changed the following steps are needet before commit/push:

0. A initial migration already exists. If not or you start fresh use
```bash
alembic init migrations
```
to generate this.


1. Create a revision file
```bash
alembic revision -m "write what you have changed"
```

2. Inside `migrations/versions`should be created that looks as follows:
```python
"""DB Upgrade to add feat/XXXX

Revision ID: REVISION_ID
Revises:
Create Date: XXXX-XX-XX XX:XX:XX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'REVISION_ID'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
```

3. Apply the migration
To run the migration and create the table in your database, use the upgrade command. Head tells Alembic to upgrade to the very latest revision.
```bash
alembic upgrade head
```


4. Check
```bash
# See the full history of migrations
alembic history
# See which revision is currently applied
alembic current
```


5. Roll Back Your Changes
```bash
# Go back one revision
alembic downgrade -1
```

More Informations about Alembic: https://cbarkinozer.medium.com/database-migrations-with-alembic-3c0e2158ac9a

## API

### Endpoints
The available endpoints can be accessed via the **Swagger UI**: http://localhost:8000/docs#/

### Example Requests
Export von Postman wenn möglich, sonst Swagger Docu example Requests erstellen


## File Structure
<!-- tree -L 2-->
```bash
├── compose.yaml
├── docs
│   ├── architecture
│   ├── guides
│   └── overview.md
├── migrations
│   └── versions
├── packages
│   └── chronicle-shared
├── README.md
├── scripts
│   ├── precommit
│   ├── smoke
│   └── worker
└── services
    ├── backend
    ├── frontend
    └── worker
```

**docs:**
Docs for User, Dev and Admin.

**migrations:**
Alembic revision files. These will be changed automaticly (see chapter 'Database - Alembic' above).

**scripts:**
Various scripts required for this project.

**services:**
Includes the main parts of this repo.
Split into:
- backend
- frontend
- worker
