import uuid

import django.utils.timezone
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Tenant",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=180)),
                ("slug", models.SlugField(unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("billing_email", models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name="Branch",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=180)),
                ("code", models.CharField(max_length=32)),
                ("timezone", models.CharField(default="UTC", max_length=64)),
                ("address", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="branches", to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "is_active"], name="tenancy_bra_tenant__9bd4ef_idx")]},
        ),
        migrations.CreateModel(
            name="Domain",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("domain", models.CharField(max_length=253, unique=True)),
                ("is_primary", models.BooleanField(default=False)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="domains", to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["domain", "tenant"], name="tenancy_dom_domain_017a98_idx")]},
        ),
        migrations.AddConstraint(
            model_name="branch",
            constraint=models.UniqueConstraint(fields=("tenant", "code"), name="uniq_branch_code_per_tenant"),
        ),
    ]
