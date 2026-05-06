from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from apps.analytics.models import DailyMetric, ItemPerformanceMetric
from apps.core.http import tenant_required


@login_required
@require_GET
@tenant_required
def dashboard_view(request):
    branch_id = request.GET.get("branch_id")
    metrics = DailyMetric.objects.filter(tenant=request.tenant, branch_id=branch_id).order_by("-business_date")[:30]
    top_items = ItemPerformanceMetric.objects.select_related("menu_item").filter(tenant=request.tenant, branch_id=branch_id).order_by("-quantity_sold")[:10]
    return JsonResponse(
        {
            "daily": list(metrics.values("business_date", "revenue", "orders_count", "dine_in_count", "takeaway_count", "scheduled_count")),
            "top_items": [{"name": item.menu_item.name, "quantity": item.quantity_sold, "revenue": str(item.revenue)} for item in top_items],
        }
    )
