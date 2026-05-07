import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("tenancy", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="DiningTable",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("label", models.CharField(max_length=64)),
                ("qr_token", models.CharField(max_length=128, unique=True)),
                ("capacity", models.PositiveIntegerField(default=4)),
                ("is_active", models.BooleanField(default=True)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="tables", to="tenancy.branch")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "is_active"], name="tables_dini_tenant__16d504_idx")]},
        ),
        migrations.CreateModel(
            name="TableSession",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(choices=[("active", "Active"), ("closed", "Closed"), ("expired", "Expired")], default="active", max_length=16)),
                ("guest_name", models.CharField(blank=True, max_length=120)),
                ("guest_phone", models.CharField(blank=True, max_length=32)),
                ("locked_by", models.CharField(blank=True, max_length=128)),
                ("expires_at", models.DateTimeField(db_index=True)),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
                ("branch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="table_sessions", to="tenancy.branch")),
                ("table", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="sessions", to="tables.diningtable")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "branch", "status", "expires_at"], name="tables_tabl_tenant__e84ae2_idx")]},
        ),
        migrations.AddConstraint(model_name="diningtable", constraint=models.UniqueConstraint(fields=("tenant", "branch", "label"), name="uniq_table_label")),
        migrations.AddConstraint(model_name="tablesession", constraint=models.UniqueConstraint(condition=models.Q(("status", "active")), fields=("tenant", "table"), name="uniq_active_session_per_table")),
    ]
