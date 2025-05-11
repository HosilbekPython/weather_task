import requests
import threading
import time
from .models import WeatherData, SearchHistory
from datetime import datetime, timezone

def fetch_weather_data():
    cities = [history.city for history in SearchHistory.objects.all()]
    API_KEY = '24c1bd2e851cf62a4e0f1b708fdc5ca3'
    PARAMS = {'units': 'metric'}

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        try:
            response = requests.get(url, params=PARAMS)
            if response.status_code == 200:
                data = response.json()
                WeatherData.objects.create(
                    city=city,
                    temperature=data['main']['temp'],
                    description=data['weather'][0]['description'],
                    icon=data['weather'][0]['icon'],
                    timestamp=datetime.now(timezone.utc)
                )

                max_records_per_city = 200
                total_records = WeatherData.objects.filter(city__iexact=city).count()
                if total_records > max_records_per_city:
                    records_to_delete = total_records - max_records_per_city
                    oldest_records = WeatherData.objects.filter(city__iexact=city).order_by('timestamp')[:records_to_delete]
                    oldest_records.delete()

        except Exception as e:
            print(f"Error fetching data for {city}: {e}")

def run_periodically():
    while True:
        fetch_weather_data()
        time.sleep(600)

def start_scheduler():
    thread = threading.Thread(target=run_periodically)
    thread.daemon = True
    thread.start()