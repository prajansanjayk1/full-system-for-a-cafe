import pytest

from apps.catalog.models import MenuCategory, MenuItem
from apps.orders.models import Order
from apps.orders.services import create_order
from apps.tenancy.models import Branch, Tenant


@pytest.mark.django_db
def test_create_order_is_idempotent():
    tenant = Tenant.objects.create(name="Tenant", slug="tenant")
    branch = Branch.objects.create(tenant=tenant, name="Main", code="main")
    category = MenuCategory.objects.create(tenant=tenant, branch=branch, name="Food")
    item = MenuItem.objects.create(tenant=tenant, branch=branch, category=category, name="Burger", price="100.00", tax_rate="5.00")

    first, first_created = create_order(
        tenant=tenant,
        branch=branch,
        order_type=Order.Type.TAKEAWAY,
        idempotency_key="idem-1",
        items=[{"menu_item_id": item.id, "quantity": 2}],
    )
    second, second_created = create_order(
        tenant=tenant,
        branch=branch,
        order_type=Order.Type.TAKEAWAY,
        idempotency_key="idem-1",
        items=[{"menu_item_id": item.id, "quantity": 2}],
    )

    assert first.id == second.id
    assert first_created is True
    assert second_created is False
    assert str(first.grand_total) == "210.00"
