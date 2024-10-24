import requests
from config import API_KEY, CITIES
from datetime import datetime

FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_weather_forecast(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching forecast for {city}: {response.status_code}")

def process_forecast_data(raw_forecast):
    processed_forecast = {}
    for item in raw_forecast['list']:
        dt = datetime.fromtimestamp(item['dt'])
        date = dt.date()
        if date not in processed_forecast:
            processed_forecast[date] = {
                'temp': [],
                'main': []
            }
        processed_forecast[date]['temp'].append(item['main']['temp'])
        processed_forecast[date]['main'].append(item['weather'][0]['main'])
    
    summary = {}
    for date, data in processed_forecast.items():
        summary[date] = {
            'avg_temp': sum(data['temp']) / len(data['temp']),
            'max_temp': max(data['temp']),
            'min_temp': min(data['temp']),
            'dominant_weather': max(set(data['main']), key=data['main'].count)
        }
    
    return summary

def get_all_cities_forecast():
    forecasts = {}
    for city in CITIES:
        raw_forecast = get_weather_forecast(city)
        forecasts[city] = process_forecast_data(raw_forecast)
    return forecasts