from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('<int:pk>/', views.alert_detail, name='alert_detail'),
    path('<int:pk>/mark-read/', views.mark_alert_read, name='mark_alert_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]