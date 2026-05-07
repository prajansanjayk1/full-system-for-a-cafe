import uuid

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0001_initial"),
        ("tables", "0001_initial"),
        ("tenancy", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("order_type", models.CharField(choices=[("dine_in", "Dine-in"), ("takeaway", "Takeaway"), ("scheduled", "Scheduled preorder")], max_length=24)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("payment_pending", "Payment pending"), ("accepted", "Accepted"), ("in_kitchen", "In kitchen"), ("ready", "Ready"), ("completed", "Completed"), ("cancelled", "Cancelled"), ("failed", "Failed")], default="draft", max_length=32)),
                ("customer_name", models.CharField(blank=True, max_length=120)),
                ("customer_phone", models.CharField(blank=True, max_length=32)),
                ("idempotency_key", models.CharField(max_length=128)),
                ("scheduled_for", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("subtotal", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("tax_total", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("grand_total", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("accepted_at", models.DateTimeField(blank=True, null=True)),
                ("ready_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to="tenancy.branch")),
                ("table_session", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="orders", to="tables.tablesession")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "status", "created_at"], name="orders_orde_tenant__8fb4d8_idx"), models.Index(fields=["tenant", "order_type", "scheduled_for"], name="orders_orde_tenant__d8f132_idx")]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name_snapshot", models.CharField(max_length=160)),
                ("quantity", models.PositiveIntegerField()),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("tax_rate", models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ("line_total", models.DecimalField(decimal_places=2, max_digits=12)),
                ("notes", models.CharField(blank=True, max_length=255)),
                ("menu_item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="catalog.menuitem")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "order"], name="orders_orde_tenant__571f9e_idx")]},
        ),
        migrations.CreateModel(
            name="OrderStateTransition",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("from_status", models.CharField(blank=True, max_length=32)),
                ("to_status", models.CharField(max_length=32)),
                ("reason", models.CharField(blank=True, max_length=255)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="transitions", to="orders.order")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "order", "created_at"], name="orders_orde_tenant__d6ca82_idx")]},
        ),
        migrations.AddConstraint(model_name="order", constraint=models.UniqueConstraint(fields=("tenant", "idempotency_key"), name="uniq_order_idempotency")),
    ]
