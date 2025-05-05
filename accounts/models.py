from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.username


class FarmerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    farm_name = models.CharField(max_length=100)
    farm_size_acres = models.DecimalField(max_digits=10, decimal_places=2)
    farm_location = models.CharField(max_length=255)
    farm_description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Farm Profile"
    
    def get_absolute_url(self):
        return reverse('accounts:profile')