from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AnalyticsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_analytics_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('analytics:crop_health'))
        self.assertEqual(response.status_code, 200)