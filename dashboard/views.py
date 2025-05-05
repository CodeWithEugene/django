from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fields.models import Field, Crop
from weather.utils import get_current_weather
from alerts.models import Alert


@login_required
def home(request):
    # Get user's fields
    fields = Field.objects.filter(owner=request.user).order_by('-created_at')[:5]
    
    # Get recent alerts
    alerts = Alert.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get weather data for user's location (using first field or default)
    weather_data = None
    if fields.exists():
        first_field = fields.first()
        weather_data = get_current_weather(first_field.latitude, first_field.longitude)
    
    context = {
        'fields': fields,
        'alerts': alerts,
        'weather_data': weather_data,
        'crop_count': Crop.objects.filter(field__owner=request.user).count(),
        'field_count': Field.objects.filter(owner=request.user).count(),
        'alert_count': Alert.objects.filter(user=request.user, is_read=False).count(),
    }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def overview(request):
    # Get all user's fields
    fields = Field.objects.filter(owner=request.user)
    
    # Get recent alerts
    alerts = Alert.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    context = {
        'fields': fields,
        'alerts': alerts,
        'total_acres': sum(field.size_acres for field in fields),
    }
    
    return render(request, 'dashboard/overview.html', context)