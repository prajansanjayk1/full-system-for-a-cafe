import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("catalog", "0001_initial"), ("tenancy", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="DailyMetric",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("business_date", models.DateField()),
                ("revenue", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("orders_count", models.PositiveIntegerField(default=0)),
                ("dine_in_count", models.PositiveIntegerField(default=0)),
                ("takeaway_count", models.PositiveIntegerField(default=0)),
                ("scheduled_count", models.PositiveIntegerField(default=0)),
                ("avg_prep_seconds", models.PositiveIntegerField(default=0)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="daily_metrics", to="tenancy.branch")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "business_date"], name="analytics_d_tenant__fba3a5_idx")]},
        ),
        migrations.CreateModel(
            name="ItemPerformanceMetric",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("business_date", models.DateField()),
                ("quantity_sold", models.PositiveIntegerField(default=0)),
                ("revenue", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="item_metrics", to="tenancy.branch")),
                ("menu_item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="catalog.menuitem")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
        ),
        migrations.AddConstraint(model_name="dailymetric", constraint=models.UniqueConstraint(fields=("tenant", "branch", "business_date"), name="uniq_daily_metric")),
        migrations.AddConstraint(model_name="itemperformancemetric", constraint=models.UniqueConstraint(fields=("tenant", "branch", "menu_item", "business_date"), name="uniq_item_metric")),
    ]
