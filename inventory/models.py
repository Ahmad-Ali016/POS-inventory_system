from django.db import models
from django.db.models import Sum

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)

    # Link to Category: If a category is deleted, items become "uncategorized" (null)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    # Default price if no batches exist
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        # Database-level summation is significantly faster than a Python loop
        result = self.batches.aggregate(total=Sum('quantity'))['total']
        return result or 0

"""
stock = models.IntegerField(default=0)

def __str__(self):
    # We include ID in the string representation to help us distinguish them
    return f"{self.name} (ID: {self.id})"

# This is a custom method to handle stock changes safely
def update_stock(self, amount):
    # We calculate the new stock
    new_stock = self.stock + amount
    # If the result is negative, we prevent the save
    if new_stock < 0:
        return False

    self.stock = new_stock
    self.save()
    return True
"""

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches')
    quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Tracking
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # Supports FIFO
        verbose_name_plural = "Batches"

    def __str__(self):
        return f"{self.product.name} (Batch #{self.id})"