from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    # Defining role choices as a class for cleaner reference
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        CASHIER = "CASHIER", "Cashier"

    # Add the role field with a default of CASHIER
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CASHIER
    )