# OpenWeatherMap API configuration
API_KEY = "d78dd9a1240df12779f98505e08e6ed9"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Cities to monitor
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Update interval in seconds (15 minutes)
UPDATE_INTERVAL = 900

# Temperature unit (celsius or fahrenheit)
TEMP_UNIT = "celsius"

# Alerting thresholds
TEMP_THRESHOLD = 35
CONSECUTIVE_ALERTS = 2

# Database configuration
DB_NAME = "weather_data.db"

EMAIL_CONFIG = {
    'sender': 'vasanthiik12@gmail.com',
    'recipient': 'vasanthiik12@gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'vasanthiik12@gmail.com',
    'password': 'Vasanthi@123'
}