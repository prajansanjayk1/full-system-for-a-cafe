from django.db import models

from apps.core.models import TenantScopedModel


class KitchenTicket(TenantScopedModel):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        PREPARING = "preparing", "Preparing"
        READY = "ready", "Ready"
        SERVED = "served", "Served"

    order = models.OneToOneField("orders.Order", related_name="kitchen_ticket", on_delete=models.CASCADE)
    branch = models.ForeignKey("tenancy.Branch", related_name="kitchen_tickets", on_delete=models.PROTECT)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.QUEUED)
    sla_due_at = models.DateTimeField(db_index=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ready_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "branch", "status", "sla_due_at"])]
