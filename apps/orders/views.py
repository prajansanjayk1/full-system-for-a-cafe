from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST
from django_ratelimit.decorators import ratelimit

from apps.core.http import json_body, tenant_required
from apps.orders.models import Order
from apps.orders.services import create_order, transition_order
from apps.tenancy.models import Branch


@csrf_protect
@require_POST
@tenant_required
@ratelimit(key="ip", rate="60/m", block=True)
def create_order_view(request):
    payload = json_body(request)
    branch = Branch.objects.get(id=payload["branch_id"], tenant=request.tenant, is_active=True)
    order, created = create_order(
        tenant=request.tenant,
        branch=branch,
        order_type=payload["order_type"],
        idempotency_key=request.headers.get("Idempotency-Key") or payload["idempotency_key"],
        items=payload["items"],
        table_session_id=payload.get("table_session_id"),
        customer=payload.get("customer", {}),
        scheduled_for=payload.get("scheduled_for"),
    )
    return JsonResponse({"id": str(order.id), "status": order.status, "created": created, "grand_total": str(order.grand_total)}, status=201 if created else 200)


@login_required
@csrf_protect
@require_POST
@tenant_required
def transition_order_view(request, order_id):
    payload = json_body(request)
    order = transition_order(tenant=request.tenant, order_id=order_id, to_status=payload["status"], actor=request.user, reason=payload.get("reason", ""))
    return JsonResponse({"id": str(order.id), "status": order.status})


@login_required
@require_GET
@tenant_required
def order_detail_view(request, order_id):
    order = Order.objects.select_related("branch", "table_session").prefetch_related("items").get(id=order_id, tenant=request.tenant)
    return JsonResponse({"id": str(order.id), "status": order.status, "items": list(order.items.values("name_snapshot", "quantity", "line_total"))})
