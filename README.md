# Restaurant Operating System

Production-oriented Django modular monolith for multi-tenant restaurant operations: QR dine-in ordering, takeaway, scheduled preorders, Razorpay payments, KDS, analytics, inventory, expenses, and RBAC-ready staff management.

## Architecture

- **Modular monolith:** apps are isolated by bounded context (`tenancy`, `orders`, `payments`, `kitchen`, `analytics`, `inventory`) to support future service extraction.
- **Tenant isolation:** `TenantResolutionMiddleware` resolves each request by host and tenant-scoped models carry a mandatory tenant foreign key.
- **Consistency:** order creation is idempotent, table sessions use row locks and a partial unique constraint, and payment webhooks are stored before processing.
- **Async workloads:** Celery + Redis handles webhook processing, scheduled preorder activation, notifications, and analytics aggregation.
- **Performance:** strategic compound indexes, precomputed analytics tables, `select_related`/`prefetch_related`, stateless web containers, and Redis caching.

## Recommended local setup without Docker

Use this path if Docker Desktop/Compose is not working on your machine. It uses SQLite and Django's in-memory cache so PostgreSQL and Redis are not required for basic development.

```bash
cp .env.local.example .env
./scripts/bootstrap_local.sh
./scripts/run_local.sh
```

Then open:

```text
http://localhost:8000/healthz/
```

## Optional Docker setup

Docker is still supported for a production-like stack, but it is no longer required for local development.

```bash
docker compose up --build
```

The Compose stack now provides default environment values, PostgreSQL/Redis health checks, automatic migrations, static collection, and a `/healthz/` health check. To seed demo data after the web container is healthy:

```bash
docker compose exec web python manage.py seed_demo
```

## Production checklist

1. Set strong environment secrets and live Razorpay credentials.
2. Point each restaurant domain to the Nginx ingress and create `Domain` records.
3. Run migrations during deployment before rolling web/worker containers.
4. Run Celery workers and beat separately from web containers.
5. Enable database backups, Redis persistence, structured logs, metrics, and alerting.

See `docs/architecture.md` and `docs/deployment.md` for operating details.
