# Backend Tests

## Create test database (once)
```bash
podman exec -it chronicle_org_postgres_1 psql -U admin -d appdb -c "CREATE DATABASE testdb;"
```

## Run all tests
```bash
cd services/backend
pytest tests/ -v
```

## Run specific test
```bash
pytest tests/test_integration.py::test_create_sync_config -v
```

## Coverage report
```bash
pytest tests/ --cov --cov-report=term-missing
```
