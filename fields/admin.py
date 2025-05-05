from django.contrib import admin
from .models import Field, Crop, SoilData

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'size_acres', 'created_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name', 'owner__username')

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'field', 'planting_date', 'expected_harvest_date')
    list_filter = ('field__owner', 'planting_date')
    search_fields = ('name', 'field__name')

@admin.register(SoilData)
class SoilDataAdmin(admin.ModelAdmin):
    list_display = ('field', 'reading_date', 'moisture_percentage', 'temperature')
    list_filter = ('field', 'reading_date')