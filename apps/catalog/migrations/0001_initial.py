import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("tenancy", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="MenuCategory",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=120)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="menu_categories", to="tenancy.branch")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"ordering": ["sort_order", "name"], "indexes": [models.Index(fields=["tenant", "branch", "is_active"], name="catalog_men_tenant__38ca58_idx")]},
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("tax_rate", models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ("sku", models.CharField(blank=True, max_length=64)),
                ("is_available", models.BooleanField(default=True)),
                ("preparation_minutes", models.PositiveIntegerField(default=12)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="menu_items", to="tenancy.branch")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="items", to="catalog.menucategory")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "is_available"], name="catalog_men_tenant__0319b5_idx"), models.Index(fields=["tenant", "sku"], name="catalog_men_tenant__e53728_idx")]},
        ),
    ]
