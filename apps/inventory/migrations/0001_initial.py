import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("tenancy", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="InventoryItem",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160)),
                ("unit", models.CharField(max_length=32)),
                ("par_level", models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ("on_hand", models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="inventory_items", to="tenancy.branch")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "name"], name="inventory_i_tenant__71a721_idx")]},
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.CharField(max_length=80)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("incurred_on", models.DateField(db_index=True)),
                ("notes", models.TextField(blank=True)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="expenses", to="tenancy.branch")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "incurred_on"], name="inventory_e_tenant__cb17b9_idx")]},
        ),
        migrations.CreateModel(
            name="StockMovement",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("movement_type", models.CharField(choices=[("purchase", "Purchase"), ("consumption", "Consumption"), ("waste", "Waste"), ("adjustment", "Adjustment")], max_length=24)),
                ("quantity", models.DecimalField(decimal_places=3, max_digits=12)),
                ("unit_cost", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("reference", models.CharField(blank=True, max_length=128)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="movements", to="inventory.inventoryitem")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
        ),
        migrations.AddConstraint(model_name="inventoryitem", constraint=models.UniqueConstraint(fields=("tenant", "branch", "name"), name="uniq_inventory_item")),
    ]
