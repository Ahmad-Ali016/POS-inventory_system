from django.db import models
from accounts.models import User
from inventory.models import Category, Product


# Create your models here.

class Vendor(models.Model):
    # Manually assigned Admin ID from accounts app
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_vendors')

    company_name = models.CharField(max_length=255, unique=True)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    # Selection of multiple categories from Inventory
    categories = models.ManyToManyField(Category, related_name='vendors')

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class Supply(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name='supplies')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order_person = models.ForeignKey(User, on_delete=models.CASCADE)

    quantity_received = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    supply_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Supply: {self.product.name} from {self.vendor.company_name}"