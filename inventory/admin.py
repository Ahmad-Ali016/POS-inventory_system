from django.contrib import admin
from .models import Category, Product

from django.db import models
from sales.models import Customer
from accounts.models import User


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # This allows you to see the Category and Stock levels at a glance
    # Using  actual field names: name, category, price, stock
    list_display = ('id', 'name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('price', 'stock')  # Allows quick updates from the list


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.item.name} to {self.customer.username}"