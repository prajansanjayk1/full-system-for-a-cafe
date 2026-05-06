from django.db import models

from apps.core.models import TenantScopedModel


class DailyMetric(TenantScopedModel):
    branch = models.ForeignKey("tenancy.Branch", related_name="daily_metrics", on_delete=models.PROTECT)
    business_date = models.DateField()
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    orders_count = models.PositiveIntegerField(default=0)
    dine_in_count = models.PositiveIntegerField(default=0)
    takeaway_count = models.PositiveIntegerField(default=0)
    scheduled_count = models.PositiveIntegerField(default=0)
    avg_prep_seconds = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "branch", "business_date"], name="uniq_daily_metric")]
        indexes = [models.Index(fields=["tenant", "branch", "business_date"])]


class ItemPerformanceMetric(TenantScopedModel):
    branch = models.ForeignKey("tenancy.Branch", related_name="item_metrics", on_delete=models.PROTECT)
    menu_item = models.ForeignKey("catalog.MenuItem", on_delete=models.PROTECT)
    business_date = models.DateField()
    quantity_sold = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "branch", "menu_item", "business_date"], name="uniq_item_metric")]
