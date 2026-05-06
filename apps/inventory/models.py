from django.db import models

from apps.core.models import TenantScopedModel


class InventoryItem(TenantScopedModel):
    branch = models.ForeignKey("tenancy.Branch", related_name="inventory_items", on_delete=models.PROTECT)
    name = models.CharField(max_length=160)
    unit = models.CharField(max_length=32)
    par_level = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    on_hand = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "branch", "name"], name="uniq_inventory_item")]
        indexes = [models.Index(fields=["tenant", "branch", "name"])]


class StockMovement(TenantScopedModel):
    class Type(models.TextChoices):
        PURCHASE = "purchase", "Purchase"
        CONSUMPTION = "consumption", "Consumption"
        WASTE = "waste", "Waste"
        ADJUSTMENT = "adjustment", "Adjustment"

    item = models.ForeignKey(InventoryItem, related_name="movements", on_delete=models.PROTECT)
    movement_type = models.CharField(max_length=24, choices=Type.choices)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reference = models.CharField(max_length=128, blank=True)


class Expense(TenantScopedModel):
    branch = models.ForeignKey("tenancy.Branch", related_name="expenses", on_delete=models.PROTECT)
    category = models.CharField(max_length=80)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    incurred_on = models.DateField(db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant", "branch", "incurred_on"])]
