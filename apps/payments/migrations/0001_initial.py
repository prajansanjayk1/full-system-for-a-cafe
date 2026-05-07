import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("orders", "0001_initial"), ("tenancy", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("provider", models.CharField(default="razorpay", max_length=32)),
                ("provider_order_id", models.CharField(max_length=128, unique=True)),
                ("provider_payment_id", models.CharField(blank=True, db_index=True, max_length=128)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(default="INR", max_length=3)),
                ("status", models.CharField(choices=[("created", "Created"), ("authorized", "Authorized"), ("captured", "Captured"), ("failed", "Failed"), ("refunded", "Refunded")], default="created", max_length=24)),
                ("failure_code", models.CharField(blank=True, max_length=64)),
                ("failure_reason", models.CharField(blank=True, max_length=255)),
                ("raw_payload", models.JSONField(blank=True, default=dict)),
                ("order", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="payment", to="orders.order")),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "status", "created_at"], name="payments_pa_tenant__06fa43_idx")]},
        ),
        migrations.CreateModel(
            name="PaymentWebhookEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("provider", models.CharField(default="razorpay", max_length=32)),
                ("event_id", models.CharField(max_length=128)),
                ("event_type", models.CharField(max_length=128)),
                ("signature", models.CharField(max_length=255)),
                ("payload", models.JSONField(default=dict)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
                ("processing_error", models.TextField(blank=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="tenancy.tenant")),
            ],
            options={"indexes": [models.Index(fields=["tenant", "event_type", "processed_at"], name="payments_pa_tenant__1e81a2_idx")]},
        ),
        migrations.AddConstraint(model_name="paymentwebhookevent", constraint=models.UniqueConstraint(fields=("tenant", "provider", "event_id"), name="uniq_payment_webhook_event")),
    ]
