import pytest

from apps.tables.models import DiningTable
from apps.tables.services import ActiveSessionExists, open_table_session
from apps.tenancy.models import Branch, Tenant


@pytest.mark.django_db
def test_single_active_session_per_table():
    tenant = Tenant.objects.create(name="Tenant", slug="tenant")
    branch = Branch.objects.create(tenant=tenant, name="Main", code="main")
    table = DiningTable.objects.create(tenant=tenant, branch=branch, label="T1", qr_token="token")

    session = open_table_session(tenant=tenant, table_id=table.id, locked_by="device-a")

    assert session.status == "active"
    with pytest.raises(ActiveSessionExists):
        open_table_session(tenant=tenant, table_id=table.id, locked_by="device-b")
