from decimal import Decimal

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.catalog.models import MenuItem
from apps.kitchen.models import KitchenTicket
from apps.orders.models import Order, OrderItem, OrderStateTransition
from apps.tables.models import TableSession

VALID_TRANSITIONS = {
    Order.Status.DRAFT: {Order.Status.PAYMENT_PENDING, Order.Status.ACCEPTED, Order.Status.CANCELLED},
    Order.Status.PAYMENT_PENDING: {Order.Status.ACCEPTED, Order.Status.FAILED, Order.Status.CANCELLED},
    Order.Status.ACCEPTED: {Order.Status.IN_KITCHEN, Order.Status.CANCELLED},
    Order.Status.IN_KITCHEN: {Order.Status.READY, Order.Status.CANCELLED},
    Order.Status.READY: {Order.Status.COMPLETED},
}


class InvalidOrderTransition(Exception):
    pass


@transaction.atomic
def create_order(*, tenant, branch, order_type, idempotency_key, items, table_session_id=None, customer=None, scheduled_for=None):
    existing = Order.objects.filter(tenant=tenant, idempotency_key=idempotency_key).prefetch_related("items").first()
    if existing:
        return existing, False
    session = None
    if order_type == Order.Type.DINE_IN:
        session = TableSession.objects.select_for_update().get(
            id=table_session_id,
            tenant=tenant,
            branch=branch,
            status=TableSession.Status.ACTIVE,
            expires_at__gt=timezone.now(),
        )
    try:
        order = Order.objects.create(
            tenant=tenant,
            branch=branch,
            table_session=session,
            order_type=order_type,
            idempotency_key=idempotency_key,
            customer_name=(customer or {}).get("name", ""),
            customer_phone=(customer or {}).get("phone", ""),
            scheduled_for=scheduled_for,
        )
    except IntegrityError:
        return Order.objects.get(tenant=tenant, idempotency_key=idempotency_key), False

    subtotal = Decimal("0.00")
    tax_total = Decimal("0.00")
    menu_items = MenuItem.objects.select_for_update().filter(
        tenant=tenant, branch=branch, id__in=[line["menu_item_id"] for line in items], is_available=True
    )
    menu_by_id = {str(item.id): item for item in menu_items}
    for line in items:
        item = menu_by_id[str(line["menu_item_id"])]
        qty = int(line["quantity"])
        line_total = item.price * qty
        line_tax = (line_total * item.tax_rate / Decimal("100.00")).quantize(Decimal("0.01"))
        OrderItem.objects.create(
            tenant=tenant,
            order=order,
            menu_item=item,
            name_snapshot=item.name,
            quantity=qty,
            unit_price=item.price,
            tax_rate=item.tax_rate,
            line_total=line_total,
            notes=line.get("notes", ""),
        )
        subtotal += line_total
        tax_total += line_tax
    order.subtotal = subtotal
    order.tax_total = tax_total
    order.grand_total = subtotal + tax_total
    order.status = Order.Status.PAYMENT_PENDING
    order.save(update_fields=["subtotal", "tax_total", "grand_total", "status", "updated_at"])
    record_transition(order=order, to_status=Order.Status.PAYMENT_PENDING, reason="order_created")
    return order, True


@transaction.atomic
def transition_order(*, tenant, order_id, to_status, actor=None, reason="") -> Order:
    order = Order.objects.select_for_update().get(id=order_id, tenant=tenant)
    allowed = VALID_TRANSITIONS.get(order.status, set())
    if to_status not in allowed and order.status != to_status:
        raise InvalidOrderTransition(f"Cannot transition {order.status} to {to_status}")
    if order.status == to_status:
        return order
    previous = order.status
    order.status = to_status
    now = timezone.now()
    if to_status == Order.Status.ACCEPTED:
        order.accepted_at = now
    elif to_status == Order.Status.READY:
        order.ready_at = now
    elif to_status == Order.Status.COMPLETED:
        order.completed_at = now
    order.save()
    record_transition(order=order, from_status=previous, to_status=to_status, actor=actor, reason=reason)
    if to_status == Order.Status.ACCEPTED:
        max_minutes = max([item.menu_item.preparation_minutes for item in order.items.select_related("menu_item")] or [10])
        KitchenTicket.objects.get_or_create(
            tenant=tenant,
            order=order,
            defaults={"branch": order.branch, "sla_due_at": now + timezone.timedelta(minutes=max_minutes)},
        )
    return order


def record_transition(*, order, to_status, from_status="", actor=None, reason=""):
    OrderStateTransition.objects.create(
        tenant=order.tenant,
        order=order,
        from_status=from_status,
        to_status=to_status,
        actor=actor,
        reason=reason,
    )
