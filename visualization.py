import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

def plot_temperature_trends(daily_summary):
    if not daily_summary:
        print("No data available for temperature trends visualization.")
        return

    try:
        cities = list(daily_summary[list(daily_summary.keys())[0]].keys())
        dates = list(daily_summary.keys())
    
        plt.figure(figsize=(12, 6))
        for city in cities:
            avg_temps = [daily_summary[date][city]["avg_temp"] for date in dates]
            plt.plot(dates, avg_temps, label=city)
    
        plt.title("Average Daily Temperature Trends")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("temperature_trends.png")
        plt.close()
        print("Temperature trends visualization saved as 'temperature_trends.png'")
    except Exception as e:
        print(f"Error in plot_temperature_trends: {str(e)}")

def plot_weather_distribution(daily_summary):
    if not daily_summary:
        print("No data available for weather distribution visualization.")
        return

    try:
        weather_counts = {}
        for date, city_data in daily_summary.items():
            for city, data in city_data.items():
                if city not in weather_counts:
                    weather_counts[city] = {}
                weather = data["dominant_weather"]
                weather_counts[city][weather] = weather_counts[city].get(weather, 0) + 1
        
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Dominant Weather Condition Distribution")
        
        for i, (city, weather_data) in enumerate(weather_counts.items()):
            ax = axs[i // 3, i % 3]
            ax.pie(weather_data.values(), labels=weather_data.keys(), autopct='%1.1f%%')
            ax.set_title(city)
        
        plt.tight_layout()
        plt.savefig("weather_distribution.png")
        plt.close()
        print("Weather distribution visualization saved as 'weather_distribution.png'")
    except Exception as e:
        print(f"Error in plot_weather_distribution: {str(e)}")