from django.db import transaction
from django.utils import timezone

from apps.kitchen.models import KitchenTicket
from apps.orders.models import Order
from apps.orders.services import transition_order


@transaction.atomic
def update_ticket_status(*, tenant, ticket_id, status, actor=None):
    ticket = KitchenTicket.objects.select_for_update().select_related("order").get(id=ticket_id, tenant=tenant)
    now = timezone.now()
    ticket.status = status
    if status == KitchenTicket.Status.PREPARING and ticket.started_at is None:
        ticket.started_at = now
        transition_order(tenant=tenant, order_id=ticket.order_id, to_status=Order.Status.IN_KITCHEN, actor=actor, reason="kds_started")
    elif status == KitchenTicket.Status.READY:
        ticket.ready_at = now
        transition_order(tenant=tenant, order_id=ticket.order_id, to_status=Order.Status.READY, actor=actor, reason="kds_ready")
    ticket.save()
    return ticket
