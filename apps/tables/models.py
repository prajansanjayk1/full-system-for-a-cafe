from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import TenantScopedModel


class DiningTable(TenantScopedModel):
    branch = models.ForeignKey("tenancy.Branch", related_name="tables", on_delete=models.PROTECT)
    label = models.CharField(max_length=64)
    qr_token = models.CharField(max_length=128, unique=True)
    capacity = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "branch", "label"], name="uniq_table_label")]
        indexes = [models.Index(fields=["tenant", "branch", "is_active"])]


class TableSession(TenantScopedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"
        EXPIRED = "expired", "Expired"

    table = models.ForeignKey(DiningTable, related_name="sessions", on_delete=models.PROTECT)
    branch = models.ForeignKey("tenancy.Branch", related_name="table_sessions", on_delete=models.PROTECT)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    guest_name = models.CharField(max_length=120, blank=True)
    guest_phone = models.CharField(max_length=32, blank=True)
    locked_by = models.CharField(max_length=128, blank=True)
    expires_at = models.DateTimeField(db_index=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "table"],
                condition=models.Q(status="active"),
                name="uniq_active_session_per_table",
            )
        ]
        indexes = [models.Index(fields=["tenant", "branch", "status", "expires_at"])]

    @classmethod
    def default_expiry(cls):
        return timezone.now() + timedelta(minutes=settings.TABLE_SESSION_TIMEOUT_MINUTES)
