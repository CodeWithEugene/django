from fields.models import Field, Crop, SoilData
from datetime import datetime, timedelta

def get_crop_health_score(crop):
    """
    Calculate a simple crop health score based on available data
    Range: 0-100
    """
    score = 70  # Default baseline score
    
    # Check if crop is within growing season
    today = datetime.now().date()
    if crop.planting_date <= today <= crop.expected_harvest_date:
        # Crop is in growing season
        total_season_days = (crop.expected_harvest_date - crop.planting_date).days
        days_elapsed = (today - crop.planting_date).days
        growth_percentage = (days_elapsed / total_season_days) * 100
        
        # Adjust score based on growth percentage (example algorithm)
        if growth_percentage < 20:
            score += 5  # Early growth stage, typically healthy
        elif growth_percentage > 80:
            score -= 5  # Late stage, more susceptible to issues
    else:
        # Crop is either not planted yet or past harvest date
        score -= 20
    
    # Check for soil data
    field = crop.field
    recent_soil_data = SoilData.objects.filter(
        field=field,
        reading_date__gte=today - timedelta(days=14)
    ).order_by('-reading_date').first()
    
    if recent_soil_data:
        # Adjust score based on soil moisture (example algorithm)
        if recent_soil_data.moisture_percentage < 10:
            score -= 20  # Too dry
        elif recent_soil_data.moisture_percentage > 40:
            score -= 15  # Too wet
        else:
            score += 10  # Optimal moisture
            
        # Adjust for soil temperature
        if recent_soil_data.temperature < 10:
            score -= 10  # Too cold
        elif recent_soil_data.temperature > 35:
            score -= 15  # Too hot
        else:
            score += 5  # Optimal temperature
    
    # Ensure score stays in range 0-100
    return max(0, min(100, score))


def get_soil_health_indicators(field):
    """
    Get soil health indicators for a field
    """
    soil_data = SoilData.objects.filter(field=field).order_by('-reading_date')[:10]
    
    if not soil_data:
        return None
    
    # Calculate averages
    avg_moisture = sum(sd.moisture_percentage for sd in soil_data) / len(soil_data)
    avg_temp = sum(sd.temperature for sd in soil_data) / len(soil_data)
    
    # Get pH levels if available
    ph_readings = [sd.ph_level for sd in soil_data if sd.ph_level is not None]
    avg_ph = sum(ph_readings) / len(ph_readings) if ph_readings else None
    
    # Get nutrient levels if available
    n_readings = [sd.nitrogen for sd in soil_data if sd.nitrogen is not None]
    p_readings = [sd.phosphorus for sd in soil_data if sd.phosphorus is not None]
    k_readings = [sd.potassium for sd in soil_data if sd.potassium is not None]
    
    avg_n = sum(n_readings) / len(n_readings) if n_readings else None
    avg_p = sum(p_readings) / len(p_readings) if p_readings else None
    avg_k = sum(k_readings) / len(k_readings) if k_readings else None
    
    # Determine soil health indicators
    moisture_status = "Optimal"
    if avg_moisture < 15:
        moisture_status = "Dry"
    elif avg_moisture > 35:
        moisture_status = "Wet"
    
    ph_status = "Unknown"
    if avg_ph is not None:
        if avg_ph < 5.5:
            ph_status = "Acidic"
        elif avg_ph > 7.5:
            ph_status = "Alkaline"
        else:
            ph_status = "Neutral"
    
    return {
        'avg_moisture': avg_moisture,
        'avg_temp': avg_temp,
        'avg_ph': avg_ph,
        'avg_n': avg_n,
        'avg_p': avg_p,
        'avg_k': avg_k,
        'moisture_status': moisture_status,
        'ph_status': ph_status,
        'latest_reading': soil_data.first().reading_date if soil_data else None,
    }