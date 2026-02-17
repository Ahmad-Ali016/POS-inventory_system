from django.contrib import admin
from .models import Category, Product, Batch

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
    # list_display references fields or methods
    list_display = ('id', 'name', 'category', 'price', 'get_total_stock')
    list_filter = ('category',)
    search_fields = ('name',)

    # Note the comma after 'price' - this is crucial!
    list_editable = ('price',)

    # Example of how to define get_total_stock if it's not in models.py
    def get_total_stock(self, obj):
        # Logic to sum up batches or return a stock field
        return obj.stock
    get_total_stock.short_description = 'Stock Level'

# Also register Batch so you can see them in the admin
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'selling_price', 'created_at')