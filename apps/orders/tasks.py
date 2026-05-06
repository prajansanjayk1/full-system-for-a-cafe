from celery import shared_task
from django.utils import timezone

from apps.orders.models import Order
from apps.orders.services import transition_order


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, max_retries=5)
def activate_due_preorders(self):
    due = Order.objects.filter(order_type=Order.Type.SCHEDULED, status=Order.Status.PAYMENT_PENDING, scheduled_for__lte=timezone.now())[:500]
    for order in due:
        transition_order(tenant=order.tenant, order_id=order.id, to_status=Order.Status.ACCEPTED, reason="scheduled_activation")
