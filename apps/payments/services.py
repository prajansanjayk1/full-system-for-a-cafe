import hmac
import json
from hashlib import sha256

import razorpay
from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.core.models import AuditLog
from apps.orders.models import Order
from apps.orders.services import transition_order
from apps.payments.models import Payment, PaymentWebhookEvent


class PaymentSignatureError(Exception):
    pass


def _client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@transaction.atomic
def create_razorpay_order(*, tenant, order_id) -> Payment:
    order = Order.objects.select_for_update().get(id=order_id, tenant=tenant)
    if hasattr(order, "payment"):
        return order.payment
    provider_order = _client().order.create(
        {
            "amount": int(order.grand_total * 100),
            "currency": "INR",
            "receipt": str(order.id),
            "payment_capture": 1,
            "notes": {"tenant_id": str(tenant.id), "order_id": str(order.id)},
        }
    )
    payment = Payment.objects.create(
        tenant=tenant,
        order=order,
        provider_order_id=provider_order["id"],
        amount=order.grand_total,
        raw_payload=provider_order,
    )
    AuditLog.objects.create(tenant=tenant, action="payment.order.created", entity_type="Payment", entity_id=str(payment.id), metadata=provider_order)
    return payment


def verify_checkout_signature(*, provider_order_id, provider_payment_id, signature) -> None:
    message = f"{provider_order_id}|{provider_payment_id}".encode()
    expected = hmac.new(settings.RAZORPAY_KEY_SECRET.encode(), message, sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise PaymentSignatureError("Invalid Razorpay checkout signature")


def verify_webhook_signature(*, body: bytes, signature: str) -> None:
    expected = hmac.new(settings.RAZORPAY_WEBHOOK_SECRET.encode(), body, sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise PaymentSignatureError("Invalid Razorpay webhook signature")


@transaction.atomic
def ingest_webhook(*, tenant, body: bytes, signature: str) -> PaymentWebhookEvent:
    verify_webhook_signature(body=body, signature=signature)
    payload = json.loads(body.decode("utf-8"))
    event_id = payload.get("id") or payload.get("created_at", "")
    try:
        event = PaymentWebhookEvent.objects.create(
            tenant=tenant,
            event_id=event_id,
            event_type=payload.get("event", "unknown"),
            signature=signature,
            payload=payload,
        )
    except IntegrityError:
        return PaymentWebhookEvent.objects.get(tenant=tenant, provider="razorpay", event_id=event_id)
    AuditLog.objects.create(tenant=tenant, action="payment.webhook.ingested", entity_type="PaymentWebhookEvent", entity_id=str(event.id), metadata={"event": event.event_type})
    return event


@transaction.atomic
def process_webhook_event(*, event_id) -> None:
    event = PaymentWebhookEvent.objects.select_for_update().select_related("tenant").get(id=event_id)
    if event.processed_at:
        return
    try:
        entity = event.payload.get("payload", {}).get("payment", {}).get("entity", {})
        provider_order_id = entity.get("order_id")
        if provider_order_id:
            payment = Payment.objects.select_for_update().select_related("order").get(
                tenant=event.tenant, provider_order_id=provider_order_id
            )
            payment.provider_payment_id = entity.get("id", "")
            if event.event_type == "payment.captured":
                payment.status = Payment.Status.CAPTURED
                transition_order(tenant=event.tenant, order_id=payment.order_id, to_status=Order.Status.ACCEPTED, reason="payment_captured")
            elif event.event_type == "payment.failed":
                payment.status = Payment.Status.FAILED
                payment.failure_code = entity.get("error_code", "")
                payment.failure_reason = entity.get("error_description", "")
            payment.raw_payload = event.payload
            payment.save()
        event.processed_at = timezone.now()
        event.processing_error = ""
    except Exception as exc:  # Celery will retry; persist the reason for operators.
        event.processing_error = str(exc)
        event.save(update_fields=["processing_error", "updated_at"])
        raise
    event.save(update_fields=["processed_at", "processing_error", "updated_at"])
