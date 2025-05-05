from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import WeatherAlert

User = get_user_model()

class WeatherTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.weather_alert = WeatherAlert.objects.create(
            user=self.user,
            type='frost',
            severity='moderate',
            description='Frost expected overnight',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            is_active=True
        )
    
    def test_weather_alert_creation(self):
        self.assertEqual(WeatherAlert.objects.count(), 1)
        self.assertEqual(self.weather_alert.type, 'frost')
        self.assertEqual(self.weather_alert.user, self.user)
        
    def test_weather_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('weather:forecast'))
        self.assertEqual(response.status_code, 200)