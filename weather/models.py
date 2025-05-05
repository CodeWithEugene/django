from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WeatherAlert(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('extreme', 'Extreme'),
    ]
    
    TYPE_CHOICES = [
        ('rain', 'Heavy Rain'),
        ('wind', 'Strong Wind'),
        ('frost', 'Frost'),
        ('heat', 'Heat Wave'),
        ('drought', 'Drought'),
        ('storm', 'Storm'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_alerts')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_type_display()} Alert - {self.get_severity_display()}"