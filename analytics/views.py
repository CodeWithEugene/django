from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fields.models import Field, Crop, SoilData
from .utils import get_crop_health_score, get_soil_health_indicators


@login_required
def crop_health(request):
    """View for crop health analytics"""
    # Get user's fields
    fields = Field.objects.filter(owner=request.user)
    
    # Get all crops
    crops = Crop.objects.filter(field__owner=request.user)
    
    # Calculate health scores for each crop
    crop_health_data = []
    for crop in crops:
        health_score = get_crop_health_score(crop)
        crop_health_data.append({
            'crop': crop,
            'health_score': health_score,
            'status': get_health_status(health_score),
            'field': crop.field,
            'days_to_harvest': crop.get_days_to_harvest(),
            'growth_days': crop.get_growth_days(),
        })
    
    # Sort by health score (lowest first)
    crop_health_data.sort(key=lambda x: x['health_score'])
    
    context = {
        'crop_health_data': crop_health_data,
        'fields': fields,
    }
    
    return render(request, 'analytics/crop_health.html', context)


@login_required
def soil_analysis(request):
    """View for soil analysis"""
    # Get user's fields
    fields = Field.objects.filter(owner=request.user)
    
    # Get soil health indicators for each field
    soil_health_data = []
    for field in fields:
        indicators = get_soil_health_indicators(field)
        if indicators:
            soil_health_data.append({
                'field': field,
                'indicators': indicators,
            })
    
    context = {
        'soil_health_data': soil_health_data,
        'fields': fields,
    }
    
    return render(request, 'analytics/soil_analysis.html', context)


def get_health_status(score):
    """Helper function to get health status from score"""
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Fair'
    elif score >= 20:
        return 'Poor'
    else:
        return 'Critical'