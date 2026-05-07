import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("orders", "0001_initial"), ("tenancy", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="KitchenTicket",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(choices=[("queued", "Queued"), ("preparing", "Preparing"), ("ready", "Ready"), ("served", "Served")], default="queued", max_length=24)),
                ("sla_due_at", models.DateTimeField(db_index=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("ready_at", models.DateTimeField(blank=True, null=True)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="kitchen_tickets", to="tenancy.branch")),
                ("order", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="kitchen_ticket", to="orders.order")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "status", "sla_due_at"], name="kitchen_kit_tenant__20f180_idx")]},
        )
    ]
