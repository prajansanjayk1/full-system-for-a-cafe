from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from apps.core.http import json_body, tenant_required
from apps.payments.services import create_razorpay_order, ingest_webhook, verify_checkout_signature
from apps.payments.tasks import process_payment_webhook


@csrf_protect
@require_POST
@tenant_required
@ratelimit(key="user_or_ip", rate="20/m", block=True)
def create_payment_order_view(request):
    payload = json_body(request)
    payment = create_razorpay_order(tenant=request.tenant, order_id=payload["order_id"])
    return JsonResponse({"provider_order_id": payment.provider_order_id, "amount": str(payment.amount), "currency": payment.currency})


@csrf_protect
@require_POST
@tenant_required
def verify_checkout_view(request):
    payload = json_body(request)
    verify_checkout_signature(
        provider_order_id=payload["razorpay_order_id"],
        provider_payment_id=payload["razorpay_payment_id"],
        signature=payload["razorpay_signature"],
    )
    return JsonResponse({"verified": True})


@csrf_exempt
@require_POST
@tenant_required
def razorpay_webhook_view(request):
    event = ingest_webhook(
        tenant=request.tenant,
        body=request.body,
        signature=request.headers.get("X-Razorpay-Signature", ""),
    )
    process_payment_webhook.delay(str(event.id))
    return JsonResponse({"accepted": True})
