from django.db import models

from apps.core.models import TenantScopedModel


class MenuCategory(TenantScopedModel):
    branch = models.ForeignKey("tenancy.Branch", related_name="menu_categories", on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        indexes = [models.Index(fields=["tenant", "branch", "is_active"])]


class MenuItem(TenantScopedModel):
    category = models.ForeignKey(MenuCategory, related_name="items", on_delete=models.PROTECT)
    branch = models.ForeignKey("tenancy.Branch", related_name="menu_items", on_delete=models.PROTECT)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sku = models.CharField(max_length=64, blank=True)
    is_available = models.BooleanField(default=True)
    preparation_minutes = models.PositiveIntegerField(default=12)

    class Meta:
        indexes = [
            models.Index(fields=["tenant", "branch", "is_available"]),
            models.Index(fields=["tenant", "sku"]),
        ]
