from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.models import MenuCategory, MenuItem
from apps.tables.models import DiningTable
from apps.tenancy.models import Branch, Domain, Tenant


class Command(BaseCommand):
    help = "Seed a tenant, branch, QR tables, and a minimal menu for local testing."

    @transaction.atomic
    def handle(self, *args, **options):
        tenant, _ = Tenant.objects.get_or_create(slug="demo", defaults={"name": "Demo Restaurant"})
        Domain.objects.get_or_create(tenant=tenant, domain="localhost", defaults={"is_primary": True})
        branch, _ = Branch.objects.get_or_create(tenant=tenant, code="main", defaults={"name": "Main Branch"})
        category, _ = MenuCategory.objects.get_or_create(tenant=tenant, branch=branch, name="Popular")
        MenuItem.objects.get_or_create(tenant=tenant, branch=branch, category=category, name="Masala Dosa", defaults={"price": "180.00", "tax_rate": "5.00", "preparation_minutes": 10})
        MenuItem.objects.get_or_create(tenant=tenant, branch=branch, category=category, name="Paneer Tikka", defaults={"price": "260.00", "tax_rate": "5.00", "preparation_minutes": 15})
        for number in range(1, 11):
            DiningTable.objects.get_or_create(tenant=tenant, branch=branch, label=f"T{number}", defaults={"qr_token": f"demo-table-{number}"})
        self.stdout.write(self.style.SUCCESS("Demo tenant seeded for localhost"))
