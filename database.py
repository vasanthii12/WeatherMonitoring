import sqlite3
from config import DB_NAME
from collections import defaultdict

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data
                 (city TEXT, main TEXT, temp REAL, feels_like REAL, humidity REAL, wind_speed REAL, dt TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_summary
                 (date DATE, city TEXT, avg_temp REAL, max_temp REAL, min_temp REAL, dominant_weather TEXT)''')
    conn.commit()
    conn.close()

def insert_weather_data(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.executemany("INSERT INTO weather_data VALUES (?, ?, ?, ?, ?, ?, ?)",
                  [(city, weather["main"], weather["temp"], weather["feels_like"], 
                    weather["humidity"], weather["wind_speed"], weather["dt"])
                   for city, weather in data.items()])
    conn.commit()
    conn.close()

def insert_daily_summary(summary):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.executemany("INSERT INTO daily_summary VALUES (?, ?, ?, ?, ?, ?)",
                  [(date, city, data["avg_temp"], data["max_temp"], data["min_temp"], data["dominant_weather"])
                   for date, city_data in summary.items()
                   for city, data in city_data.items()])
    conn.commit()
    conn.close()

def get_daily_summary(start_date, end_date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM daily_summary WHERE date BETWEEN ? AND ?", (start_date, end_date))
    results = c.fetchall()
    conn.close()
    
    summary = defaultdict(lambda: defaultdict(dict))
    for row in results:
        date, city, avg_temp, max_temp, min_temp, dominant_weather = row
        summary[date][city] = {
            "avg_temp": avg_temp,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "dominant_weather": dominant_weather
        }
    
    return summary