# Docs/Admin
This docs will show you how to configure and start/stop chronicle. Also common mistakes are described if these are known.

## Requirements
Chronicle runs inside containers.
You can use Docker or Podman


TBD: wie das machen mit UV/Requirements


## Usage (Start / Stop)
The following commands should be run on where you want to host the chronicle container:

**Start:**
```bash
podman-compose up --build
```

**Stopping Services:**
```bash
podman-compose down
```

## Config / Enviroment
Nicht nur localhost

## DB Access
Make sure the compose stack (or at least postgres) is running before opening the DB shell:
```bash
podman-compose exec postgres psql -U admin -d appdb
```

Show all tables:

```sql
\dt
```
## Updates
Alembic versions

## Tests
Braucht das ein Admin? -> Copy from dev

## Common Errorrs / Troubleshooting
**Build isn't succesfull:**
Force recreate the build:
Podman:
```bash
podman-compose up --build --force-recreate -d
```
