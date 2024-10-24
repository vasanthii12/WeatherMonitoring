from flask import Flask, render_template, jsonify
from flask_cors import CORS
from api_client import get_all_cities_weather
from data_processor import process_weather_data, calculate_daily_summary
from database import get_daily_summary, init_db
from alerting import AlertSystem
from visualization import plot_temperature_trends, plot_weather_distribution
from forecast import get_all_cities_forecast
from config import CITIES
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

init_db()
alert_system = AlertSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    raw_data = get_all_cities_weather()
    processed_data = process_weather_data(raw_data)
    return jsonify(processed_data)

@app.route('/api/weather/<city>')
def get_city_weather(city):
    raw_data = get_all_cities_weather()
    city_data = next((item for item in raw_data if item["name"] == city), None)
    if city_data:
        return jsonify(process_weather_data([city_data])[0])
    else:
        return jsonify({"error": "City not found"}), 404

@app.route('/api/summary')
def get_summary():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)  # Get last 7 days
    daily_data = get_daily_summary(start_date, end_date)
    summary = calculate_daily_summary(daily_data)
    return jsonify(summary)

@app.route('/api/forecast')
def get_forecast():
    forecast_data = get_all_cities_forecast()
    return jsonify(forecast_data)

@app.route('/api/cities')
def get_cities():
    return jsonify(CITIES)

@app.route('/api/visualization/temperature')
def get_temperature_visualization():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    daily_data = get_daily_summary(start_date, end_date)
    summary = calculate_daily_summary(daily_data)
    plot_temperature_trends(summary)
    return send_file('temperature_trends.png', mimetype='image/png')

@app.route('/api/visualization/weather')
def get_weather_visualization():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    daily_data = get_daily_summary(start_date, end_date)
    summary = calculate_daily_summary(daily_data)
    plot_weather_distribution(summary)
    return send_file('weather_distribution.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)