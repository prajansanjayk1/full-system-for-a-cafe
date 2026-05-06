# Deployment

## Runtime topology

- Nginx terminates HTTP and forwards to Gunicorn.
- Gunicorn runs stateless Django web workers.
- Celery workers process payment, preorder, notification, and analytics jobs.
- PostgreSQL stores transactional data; Redis backs cache, broker, and task results.

## CI/CD pipeline

Recommended stages:

1. Install dependencies.
2. Run `python -m compileall config apps tests`.
3. Run `python manage.py check --deploy` against production-like env variables.
4. Run unit/integration tests.
5. Build and scan Docker image.
6. Apply migrations and roll containers using blue/green or rolling deployment.

## Scaling

Scale `web` horizontally behind the load balancer. Scale Celery by queue (`payments`, `analytics`, `notifications`) as traffic grows. Partition high-volume tables such as `orders_order`, `orders_orderitem`, and `core_auditlog` by tenant and/or month when write volume requires it.
