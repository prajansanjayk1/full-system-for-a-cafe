import uuid

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TenantScopedModel(TimeStampedModel):
    tenant = models.ForeignKey("tenancy.Tenant", on_delete=models.PROTECT, db_index=True)

    class Meta:
        abstract = True


class AuditLog(TimeStampedModel):
    tenant = models.ForeignKey("tenancy.Tenant", on_delete=models.PROTECT, null=True, blank=True)
    actor = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=128)
    entity_type = models.CharField(max_length=128)
    entity_id = models.CharField(max_length=64, blank=True)
    idempotency_key = models.CharField(max_length=128, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "action", "created_at"])]
