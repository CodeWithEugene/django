from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from multiselectfield import MultiSelectField

User = get_user_model()

class Field(models.Model):
    SOIL_TYPE_CHOICES = [
        ('clay', 'Clay'),
        ('silt', 'Silt'),
        ('sand', 'Sand'),
        ('loam', 'Loam'),
        ('clay_loam', 'Clay Loam'),
        ('sandy_loam', 'Sandy Loam'),
        ('silty_loam', 'Silty Loam'),
        ('peat', 'Peat'),
        ('chalky', 'Chalky'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    size_acres = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES, default='loam')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to='field_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('fields:field_detail', args=[str(self.id)])


class Crop(models.Model):
    CROP_CATEGORY_CHOICES = [
        ('cereal', 'Cereal'),
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
        ('legume', 'Legume'),
        ('oilseed', 'Oilseed'),
        ('root', 'Root Vegetable'),
        ('fiber', 'Fiber Crop'),
        ('forage', 'Forage Crop'),
        ('other', 'Other'),
    ]
    
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CROP_CATEGORY_CHOICES, default='other')
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    actual_harvest_date = models.DateField(blank=True, null=True)
    yield_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    yield_unit = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} at {self.field.name}"
    
    def get_growth_days(self):
        from datetime import date
        if self.actual_harvest_date:
            return (self.actual_harvest_date - self.planting_date).days
        else:
            return (date.today() - self.planting_date).days
    
    def get_days_to_harvest(self):
        from datetime import date
        if self.actual_harvest_date:
            return 0
        else:
            days = (self.expected_harvest_date - date.today()).days
            return max(0, days)


class SoilData(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='soil_data')
    reading_date = models.DateField()
    moisture_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperature in °C")
    ph_level = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nitrogen = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="N level in ppm")
    phosphorus = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="P level in ppm")
    potassium = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="K level in ppm")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-reading_date']
        verbose_name_plural = 'Soil Data'
    
    def __str__(self):
        return f"Soil data for {self.field.name} on {self.reading_date}"