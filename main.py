import time
import traceback
from datetime import datetime, timedelta
from api_client import get_all_cities_weather
from data_processor import process_weather_data, calculate_daily_summary, check_alert_thresholds
from database import init_db, insert_weather_data, insert_daily_summary, get_daily_summary
from alerting import AlertSystem
from visualization import plot_temperature_trends, plot_weather_distribution
from config import UPDATE_INTERVAL
from forecast import get_all_cities_forecast

def main():
    init_db()
    alert_system = AlertSystem()
    last_summary_date = None

    while True:
        try:
            print("Fetching weather data...")
            raw_data = get_all_cities_weather()
            print("Raw data received. Processing...")
            processed_data = process_weather_data(raw_data)
            print("Data processed. Inserting into database...")
            insert_weather_data(processed_data)
            print("Data inserted. Checking alert thresholds...")
            check_alert_thresholds(processed_data, alert_system)
            print("Alert check complete.")

            # Calculate and store daily summary at the end of each day
            current_time = datetime.now()
            if current_time.hour == 23 and current_time.minute >= 55:
                print("Calculating daily summary...")
                end_date = current_time.date()
                start_date = end_date - timedelta(days=1)
                daily_data = get_daily_summary(start_date, end_date)
                daily_summary = calculate_daily_summary(daily_data)
                
                if daily_summary:
                    insert_daily_summary(daily_summary)
                    print("Daily summary calculated and stored.")

                    # Generate visualizations
                    print("Generating visualizations...")
                    plot_temperature_trends(daily_summary)
                    plot_weather_distribution(daily_summary)
                    print("Visualizations generated.")
                else:
                    print("No daily summary data available. Skipping visualizations.")
            print(f"Waiting for {UPDATE_INTERVAL} seconds before next update...")
            time.sleep(UPDATE_INTERVAL)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            print("Waiting for 60 seconds before retrying...")
            time.sleep(60)  # Wait for 1 minute before retrying  

if __name__ == "__main__":
    main()