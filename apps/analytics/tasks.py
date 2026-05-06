from celery import shared_task
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone

from apps.analytics.models import DailyMetric, ItemPerformanceMetric
from apps.orders.models import Order, OrderItem


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, max_retries=5)
def aggregate_daily_metrics(self, tenant_id, branch_id, business_date=None):
    business_date = business_date or timezone.localdate().isoformat()
    orders = Order.objects.filter(tenant_id=tenant_id, branch_id=branch_id, created_at__date=business_date)
    completed = orders.filter(status=Order.Status.COMPLETED)
    metric_values = completed.aggregate(
        revenue=Sum("grand_total"),
        orders_count=Count("id"),
        dine_in_count=Count("id", filter=Q(order_type=Order.Type.DINE_IN)),
        takeaway_count=Count("id", filter=Q(order_type=Order.Type.TAKEAWAY)),
        scheduled_count=Count("id", filter=Q(order_type=Order.Type.SCHEDULED)),
        avg_prep=Avg("kitchen_ticket__ready_at"),
    )
    DailyMetric.objects.update_or_create(
        tenant_id=tenant_id,
        branch_id=branch_id,
        business_date=business_date,
        defaults={
            "revenue": metric_values["revenue"] or 0,
            "orders_count": metric_values["orders_count"] or 0,
            "dine_in_count": metric_values["dine_in_count"] or 0,
            "takeaway_count": metric_values["takeaway_count"] or 0,
            "scheduled_count": metric_values["scheduled_count"] or 0,
        },
    )
    rows = (
        OrderItem.objects.filter(order__in=completed)
        .values("menu_item_id")
        .annotate(quantity=Sum("quantity"), revenue=Sum("line_total"))
    )
    for row in rows:
        ItemPerformanceMetric.objects.update_or_create(
            tenant_id=tenant_id,
            branch_id=branch_id,
            menu_item_id=row["menu_item_id"],
            business_date=business_date,
            defaults={"quantity_sold": row["quantity"] or 0, "revenue": row["revenue"] or 0},
        )
