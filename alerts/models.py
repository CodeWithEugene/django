from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Alert(models.Model):
    LEVEL_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
        ('success', 'Success'),
    ]
    
    CATEGORY_CHOICES = [
        ('weather', 'Weather'),
        ('crop', 'Crop'),
        ('soil', 'Soil'),
        ('system', 'System'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    title = models.CharField(max_length=100)
    message = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='info')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='other')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    field = models.ForeignKey('fields.Field', on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('alerts:alert_detail', args=[str(self.id)])
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()