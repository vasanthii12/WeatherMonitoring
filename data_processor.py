def process_weather_data(raw_data):
    processed_data = []
    for data in raw_data:
        processed_data.append({
            'name': data['name'],
            'temp': round(data['temp'], 1),
            'feels_like': round(data['feels_like'], 1),
            'humidity': data['humidity'],
            'wind_speed': data['wind_speed'],
            'main': data['main'],
            'dt': data['dt']
        })
    return processed_data

def calculate_daily_summary(daily_data):
    summary = {}
    for data in daily_data:
        date = data['dt'].date()
        if date not in summary:
            summary[date] = {
                'temps': [],
                'conditions': []
            }
        summary[date]['temps'].append(data['temp'])
        summary[date]['conditions'].append(data['main'])

    for date, data in summary.items():
        summary[date] = {
            'average_temp': round(sum(data['temps']) / len(data['temps']), 1),
            'max_temp': round(max(data['temps']), 1),
            'min_temp': round(min(data['temps']), 1),
            'dominant_condition': max(set(data['conditions']), key=data['conditions'].count)
        }

    return summary