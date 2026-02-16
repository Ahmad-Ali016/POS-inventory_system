from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'created_at')
    search_fields = ('username', 'phone_number')