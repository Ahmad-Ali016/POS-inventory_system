from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

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
