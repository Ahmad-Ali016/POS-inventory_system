from django.contrib import admin
from .models import Customer, Sale

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'created_at')
    search_fields = ('username', 'phone_number')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # What to show in the main table list
    list_display = ('id', 'sale_date', 'customer', 'product', 'quantity_sold', 'total_price', 'staff_member')

    list_filter = ('sale_date', 'staff_member', 'product__category')
    search_fields = ('customer__username', 'product__name')

    # Important: Make transactions read-only so they can't be edited after the sale
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        # We usually want sales to be created via the API/POS View, not manually in admin
        return False