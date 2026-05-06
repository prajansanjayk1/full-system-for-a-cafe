from django.db import models

from apps.core.models import TimeStampedModel


class Tenant(TimeStampedModel):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    billing_email = models.EmailField(blank=True)

    def __str__(self) -> str:
        return self.name


class Domain(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, related_name="domains", on_delete=models.CASCADE)
    domain = models.CharField(max_length=253, unique=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["domain", "tenant"])]


class Branch(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, related_name="branches", on_delete=models.PROTECT)
    name = models.CharField(max_length=180)
    code = models.CharField(max_length=32)
    timezone = models.CharField(max_length=64, default="UTC")
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "code"], name="uniq_branch_code_per_tenant")]
        indexes = [models.Index(fields=["tenant", "is_active"])]
