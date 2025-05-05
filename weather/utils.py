import requests
import os
from django.conf import settings
from datetime import datetime

def get_current_weather(lat, lon):
    """
    Get current weather data from OpenWeatherMap API
    """
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind']['deg'],
            'clouds': data['clouds']['all'],
            'location': data['name'],
            'country': data['sys']['country'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']),
            'timestamp': datetime.fromtimestamp(data['dt']),
        }
        
        if 'rain' in data and '1h' in data['rain']:
            weather_data['rain_1h'] = data['rain']['1h']
        else:
            weather_data['rain_1h'] = 0
            
        return weather_data
    
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None


def get_forecast(lat, lon, days=7):
    """
    Get weather forecast data from OpenWeatherMap API
    """
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Process forecast data
        forecast_data = []
        day_data = {}
        
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            day = dt.date()
            
            if day not in day_data:
                day_data[day] = {
                    'date': day,
                    'temp_min': float('inf'),
                    'temp_max': float('-inf'),
                    'descriptions': [],
                    'icons': [],
                    'precipitation': 0,
                    'humidity': [],
                    'wind_speed': [],
                }
            
            # Update day data
            day_info = day_data[day]
            day_info['temp_min'] = min(day_info['temp_min'], item['main']['temp_min'])
            day_info['temp_max'] = max(day_info['temp_max'], item['main']['temp_max'])
            day_info['descriptions'].append(item['weather'][0]['description'])
            day_info['icons'].append(item['weather'][0]['icon'])
            day_info['humidity'].append(item['main']['humidity'])
            day_info['wind_speed'].append(item['wind']['speed'])
            
            # Add precipitation if available
            if 'rain' in item and '3h' in item['rain']:
                day_info['precipitation'] += item['rain']['3h']
        
        # Calculate daily averages and most common values
        for day, info in day_data.items():
            # Get most common description and icon
            from collections import Counter
            descriptions_counter = Counter(info['descriptions'])
            icons_counter = Counter(info['icons'])
            
            info['main_description'] = descriptions_counter.most_common(1)[0][0]
            info['main_icon'] = icons_counter.most_common(1)[0][0]
            
            # Calculate averages
            info['avg_humidity'] = sum(info['humidity']) / len(info['humidity'])
            info['avg_wind_speed'] = sum(info['wind_speed']) / len(info['wind_speed'])
            
            # Remove temporary lists
            del info['descriptions']
            del info['icons']
            del info['humidity']
            del info['wind_speed']
            
            forecast_data.append(info)
        
        # Sort by date
        forecast_data.sort(key=lambda x: x['date'])
        
        # Limit to requested number of days
        return forecast_data[:days]
    
    except Exception as e:
        print(f"Error fetching forecast data: {e}")
        return None


def get_weather_alerts(lat, lon):
    """
    Get weather alerts from OpenWeatherMap API
    """
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,daily&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'alerts' in data:
            return data['alerts']
        return []
    
    except Exception as e:
        print(f"Error fetching weather alerts: {e}")
        return []