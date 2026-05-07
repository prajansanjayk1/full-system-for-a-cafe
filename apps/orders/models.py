from django.db import models

from apps.core.models import TenantScopedModel


class Order(TenantScopedModel):
    class Type(models.TextChoices):
        DINE_IN = "dine_in", "Dine-in"
        TAKEAWAY = "takeaway", "Takeaway"
        SCHEDULED = "scheduled", "Scheduled preorder"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PAYMENT_PENDING = "payment_pending", "Payment pending"
        ACCEPTED = "accepted", "Accepted"
        IN_KITCHEN = "in_kitchen", "In kitchen"
        READY = "ready", "Ready"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    branch = models.ForeignKey("tenancy.Branch", related_name="orders", on_delete=models.PROTECT)
    table_session = models.ForeignKey("tables.TableSession", related_name="orders", on_delete=models.PROTECT, null=True, blank=True)
    order_type = models.CharField(max_length=24, choices=Type.choices)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT)
    customer_name = models.CharField(max_length=120, blank=True)
    customer_phone = models.CharField(max_length=32, blank=True)
    idempotency_key = models.CharField(max_length=128)
    scheduled_for = models.DateTimeField(null=True, blank=True, db_index=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    accepted_at = models.DateTimeField(null=True, blank=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "idempotency_key"], name="uniq_order_idempotency")]
        indexes = [
            models.Index(fields=["tenant", "branch", "status", "created_at"]),
            models.Index(fields=["tenant", "order_type", "scheduled_for"]),
        ]


class OrderItem(TenantScopedModel):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey("catalog.MenuItem", on_delete=models.PROTECT)
    name_snapshot = models.CharField(max_length=160)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "order"])]


class OrderStateTransition(TenantScopedModel):
    order = models.ForeignKey(Order, related_name="transitions", on_delete=models.CASCADE)
    from_status = models.CharField(max_length=32, blank=True)
    to_status = models.CharField(max_length=32)
    reason = models.CharField(max_length=255, blank=True)
    actor = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "order", "created_at"])]
