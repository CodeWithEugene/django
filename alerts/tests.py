from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Alert

User = get_user_model()

class AlertsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.alert = Alert.objects.create(
            user=self.user,
            title='Test Alert',
            message='This is a test alert message',
            level='warning',
            category='system'
        )
    
    def test_alert_creation(self):
        self.assertEqual(Alert.objects.count(), 1)
        self.assertEqual(self.alert.title, 'Test Alert')
        self.assertEqual(self.alert.user, self.user)
        
    def test_alert_list_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('alerts:alert_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Alert')
        
    def test_alert_mark_as_read(self):
        self.assertFalse(self.alert.is_read)
        self.alert.mark_as_read()
        self.assertTrue(self.alert.is_read)