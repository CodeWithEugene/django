from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import get_current_weather, get_forecast, get_weather_alerts
from fields.models import Field
from .models import WeatherAlert


@login_required
def forecast(request):
    """View for general weather forecast"""
    # Get user's fields
    fields = Field.objects.filter(owner=request.user)
    
    # Default coordinates (use first field or default)
    lat, lon = 40.7128, -74.0060  # New York as default
    location_name = "Default Location"
    
    if fields.exists() and fields.first().latitude and fields.first().longitude:
        field = fields.first()
        lat = field.latitude
        lon = field.longitude
        location_name = field.name
    
    # Get weather data
    current_weather = get_current_weather(lat, lon)
    forecast_data = get_forecast(lat, lon)
    
    context = {
        'current_weather': current_weather,
        'forecast_data': forecast_data,
        'fields': fields,
        'location_name': location_name,
    }
    
    return render(request, 'weather/forecast.html', context)


@login_required
def field_weather(request, field_id):
    """View for specific field weather"""
    field = get_object_or_404(Field, pk=field_id, owner=request.user)
    
    if not field.latitude or not field.longitude:
        # If coordinates not set, show message
        return render(request, 'weather/field_weather.html', {
            'field': field,
            'error_message': "This field doesn't have geographical coordinates set. Please update the field information."
        })
    
    # Get weather data
    current_weather = get_current_weather(field.latitude, field.longitude)
    forecast_data = get_forecast(field.latitude, field.longitude)
    
    context = {
        'field': field,
        'current_weather': current_weather,
        'forecast_data': forecast_data,
    }
    
    return render(request, 'weather/field_weather.html', context)


@login_required
def alerts(request):
    """View for weather alerts"""
    # Get user's weather alerts
    alerts = WeatherAlert.objects.filter(user=request.user, is_active=True).order_by('-created_at')
    
    # Get fields to potentially add more alerts
    fields = Field.objects.filter(owner=request.user)
    
    # Get active alerts from API for each field
    api_alerts = []
    for field in fields:
        if field.latitude and field.longitude:
            alerts_data = get_weather_alerts(field.latitude, field.longitude)
            for alert in alerts_data:
                alert['field_name'] = field.name
                api_alerts.append(alert)
    
    context = {
        'alerts': alerts,
        'api_alerts': api_alerts,
    }
    
    return render(request, 'weather/alerts.html', context)