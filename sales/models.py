from django.db import models
from django.contrib.auth.hashers import make_password

from accounts.models import User
from inventory.models import Product


# Create your models here.

class Customer(models.Model):
    # Credentials
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) # Will store hashed password
    email = models.EmailField(unique=True)

    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.TextField(null=True, blank=True)

    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # This hashes the password before it hits the database
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.first_name})"

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='purchases')
    staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales_handled')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sold_items')
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.product.name} x {self.quantity_sold}"