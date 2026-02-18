from django.contrib import admin
from purchases.models import Vendor, Supply


# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'contact_person', 'registered_by', 'date_created')
    search_fields = ('company_name', 'contact_person')

    filter_horizontal = ('categories',)
    list_filter = ('categories', 'date_created')

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('supply_date', 'product', 'vendor', 'quantity_received', 'cost_price', 'order_person')
    list_filter = ('supply_date', 'vendor', 'category')
    date_hierarchy = 'supply_date' # Adds a nice date drill-down at the top