from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

# We inherit from UserAdmin so we get the nice password hashing and layout
class CustomUserAdmin(UserAdmin):
    # This ensures the 'role' field shows up when you click on a user
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    # This adds 'role' to the main list view column
    list_display = ['id', 'username', 'email', 'role', 'is_staff']

# Register the model
admin.site.register(User, CustomUserAdmin)