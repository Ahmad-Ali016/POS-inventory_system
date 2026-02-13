from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
