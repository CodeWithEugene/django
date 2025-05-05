from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_dashboard_login_required(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_dashboard_with_login(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)