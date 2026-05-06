# Architecture Notes

## Tenant model

Every commercial restaurant is a `Tenant`; each tenant owns one or more `Branch` records and one or more mapped domains. The request middleware resolves `request.tenant` from the `Host` header and fails closed for unknown domains outside local development.

## Order engine

The platform uses one `Order` aggregate for dine-in, takeaway, and scheduled preorders. `OrderItem` snapshots item name and pricing to preserve historical receipts. The service layer owns creation, idempotency, totals, and state transitions, keeping views thin and replaceable.

## Table sessions

`open_table_session` locks the `DiningTable` row with `select_for_update`, expires stale sessions, checks for an active session, and relies on a partial unique constraint as a final database-level guard. This prevents two guests from holding the same table session under concurrent QR scans.

## Payments

Razorpay order creation happens server-side. Checkout signatures and webhook signatures are verified with HMAC SHA256. Webhooks are stored with a unique provider event key before Celery processing, making retries idempotent and auditable.

## Kitchen and analytics

KDS tickets are created after payment acceptance and ordered by SLA due time. Analytics are precomputed into daily and item metric tables by Celery jobs to keep dashboards off the transactional hot path.
