from django.urls import path
from . import views

app_name = 'fields'

urlpatterns = [
    path('', views.field_list, name='field_list'),
    path('create/', views.field_create, name='field_create'),
    path('<int:pk>/', views.field_detail, name='field_detail'),
    path('<int:pk>/update/', views.field_update, name='field_update'),
    path('<int:pk>/delete/', views.field_delete, name='field_delete'),
    
    # Crop URLs
    path('<int:field_pk>/crops/add/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('crops/<int:pk>/update/', views.crop_update, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    
    # Soil data URLs
    path('<int:field_pk>/soil/add/', views.soil_data_create, name='soil_data_create'),
    path('<int:field_pk>/soil/', views.soil_data_list, name='soil_data_list'),
]