from django.db import models

from apps.core.models import TenantScopedModel


class Payment(TenantScopedModel):
    class Status(models.TextChoices):
        CREATED = "created", "Created"
        AUTHORIZED = "authorized", "Authorized"
        CAPTURED = "captured", "Captured"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    order = models.OneToOneField("orders.Order", related_name="payment", on_delete=models.PROTECT)
    provider = models.CharField(max_length=32, default="razorpay")
    provider_order_id = models.CharField(max_length=128, unique=True)
    provider_payment_id = models.CharField(max_length=128, blank=True, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.CREATED)
    failure_code = models.CharField(max_length=64, blank=True)
    failure_reason = models.CharField(max_length=255, blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "status", "created_at"])]


class PaymentWebhookEvent(TenantScopedModel):
    provider = models.CharField(max_length=32, default="razorpay")
    event_id = models.CharField(max_length=128)
    event_type = models.CharField(max_length=128)
    signature = models.CharField(max_length=255)
    payload = models.JSONField(default=dict)
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_error = models.TextField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "provider", "event_id"], name="uniq_payment_webhook_event")]
        indexes = [models.Index(fields=["tenant", "event_type", "processed_at"])]
