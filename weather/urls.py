from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('forecast/', views.forecast, name='forecast'),
    path('alerts/', views.alerts, name='alerts'),
    path('field/<int:field_id>/', views.field_weather, name='field_weather'),
]