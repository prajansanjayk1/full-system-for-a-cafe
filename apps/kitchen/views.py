from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST

from apps.core.http import json_body, tenant_required
from apps.kitchen.models import KitchenTicket
from apps.kitchen.services import update_ticket_status


@login_required
@require_GET
@tenant_required
def ticket_feed_view(request):
    branch_id = request.GET.get("branch_id")
    tickets = (
        KitchenTicket.objects.select_related("order")
        .filter(tenant=request.tenant, branch_id=branch_id)
        .exclude(status=KitchenTicket.Status.SERVED)
        .order_by("sla_due_at")[:100]
    )
    return JsonResponse(
        {
            "tickets": [
                {
                    "id": str(ticket.id),
                    "order_id": str(ticket.order_id),
                    "status": ticket.status,
                    "sla_due_at": ticket.sla_due_at.isoformat(),
                    "order_status": ticket.order.status,
                }
                for ticket in tickets
            ]
        }
    )


@login_required
@csrf_protect
@require_POST
@tenant_required
def ticket_status_view(request, ticket_id):
    payload = json_body(request)
    ticket = update_ticket_status(tenant=request.tenant, ticket_id=ticket_id, status=payload["status"], actor=request.user)
    return JsonResponse({"id": str(ticket.id), "status": ticket.status})
