from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FarmerProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm_name', 'farm_size_acres', 'created_at')
    search_fields = ('user__username', 'farm_name')