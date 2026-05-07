from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    tenant = models.ForeignKey("tenancy.Tenant", on_delete=models.PROTECT, null=True, blank=True)
    branch = models.ForeignKey("tenancy.Branch", on_delete=models.PROTECT, null=True, blank=True)


class StaffRole(models.TextChoices):
    OWNER = "owner", "Owner"
    MANAGER = "manager", "Manager"
    CASHIER = "cashier", "Cashier"
    KITCHEN = "kitchen", "Kitchen"
    WAITER = "waiter", "Waiter"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, related_name="staff_profile", on_delete=models.CASCADE)
    role = models.CharField(max_length=32, choices=StaffRole.choices)
    can_refund = models.BooleanField(default=False)
    can_manage_inventory = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["role"])]
