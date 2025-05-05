from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Field, Crop
from datetime import date, timedelta

User = get_user_model()

class FieldsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.field = Field.objects.create(
            owner=self.user,
            name='Test Field',
            size_acres=10.5,
            address='123 Farm Road',
            soil_type='loam',
            latitude=40.7128,
            longitude=-74.0060
        )
        self.crop = Crop.objects.create(
            field=self.field,
            name='Corn',
            variety='Sweet Corn',
            planting_date=date.today() - timedelta(days=30),
            expected_harvest_date=date.today() + timedelta(days=60)
        )
        
    def test_field_creation(self):
        self.assertEqual(Field.objects.count(), 1)
        self.assertEqual(self.field.name, 'Test Field')
        self.assertEqual(self.field.owner, self.user)
        
    def test_crop_creation(self):
        self.assertEqual(Crop.objects.count(), 1)
        self.assertEqual(self.crop.name, 'Corn')
        self.assertEqual(self.crop.field, self.field)
        
    def test_field_list_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('fields:field_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Field')