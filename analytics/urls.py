from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('crop-health/', views.crop_health, name='crop_health'),
    path('soil-analysis/', views.soil_analysis, name='soil_analysis'),
]