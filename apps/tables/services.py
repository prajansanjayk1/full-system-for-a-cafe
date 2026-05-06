from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.tables.models import DiningTable, TableSession


class ActiveSessionExists(Exception):
    pass


@transaction.atomic
def open_table_session(*, tenant, table_id, guest_name="", guest_phone="", locked_by="") -> TableSession:
    table = DiningTable.objects.select_for_update().get(id=table_id, tenant=tenant, is_active=True)
    TableSession.objects.select_for_update().filter(
        tenant=tenant, table=table, status=TableSession.Status.ACTIVE, expires_at__lt=timezone.now()
    ).update(status=TableSession.Status.EXPIRED)
    if TableSession.objects.filter(tenant=tenant, table=table, status=TableSession.Status.ACTIVE).exists():
        raise ActiveSessionExists("Table already has an active session")
    try:
        return TableSession.objects.create(
            tenant=tenant,
            branch=table.branch,
            table=table,
            guest_name=guest_name,
            guest_phone=guest_phone,
            locked_by=locked_by,
            expires_at=TableSession.default_expiry(),
        )
    except IntegrityError as exc:
        raise ActiveSessionExists("Table already has an active session") from exc


@transaction.atomic
def close_table_session(*, tenant, session_id) -> TableSession:
    session = TableSession.objects.select_for_update().get(id=session_id, tenant=tenant)
    session.status = TableSession.Status.CLOSED
    session.closed_at = timezone.now()
    session.save(update_fields=["status", "closed_at", "updated_at"])
    return session
