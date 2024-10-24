import requests
from config import API_KEY, CITIES

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        'name': city,
        'main': data['weather'][0]['main'],
        'temp': kelvin_to_celsius(data['main']['temp']),
        'feels_like': kelvin_to_celsius(data['main']['feels_like']),
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'dt': data['dt']
    }

def get_all_cities_weather():
    return [get_weather_data(city) for city in CITIES]