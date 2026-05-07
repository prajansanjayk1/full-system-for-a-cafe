# Local Development Without Docker

This project can run without Docker for contributors who have trouble with Docker Desktop, virtualization, or Compose networking.

## Prerequisites

- Python 3.11+
- Network access to install Python packages from PyPI

## Bootstrap

```bash
cp .env.local.example .env
./scripts/bootstrap_local.sh
```

The bootstrap script creates `.venv`, installs dependencies, runs migrations against SQLite, and seeds a demo tenant/domain/menu/tables for `localhost`.

## Run

```bash
./scripts/run_local.sh
```

Health check:

```bash
curl http://localhost:8000/healthz/
```

## Notes

- Local settings use SQLite and an in-memory cache so Redis is not required.
- Celery tasks execute eagerly in local settings for easier debugging.
- Use Docker or a real PostgreSQL database before validating PostgreSQL-specific behavior such as row-level locking under load.
