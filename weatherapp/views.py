from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
from .models import WeatherData, SearchHistory
import csv
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import WeatherDataSerializer

def home(request):
    description = 'clear sky'
    icon = '01d'
    temp = 25
    day = datetime.date.today()
    timestamp = datetime.datetime.now()
    exception_occurred = True

    if request.method == 'POST':
        city = request.POST.get('city', 'Tashkent')
        if not SearchHistory.objects.filter(city__iexact=city).exists():
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=24c1bd2e851cf62a4e0f1b708fdc5ca3'
            PARAMS = {'units': 'metric'}

            try:
                data = requests.get(url, params=PARAMS).json()
                description = data['weather'][0]['description']
                icon = data['weather'][0]['icon']
                temp = data['main']['temp']
                day = datetime.date.today()
                timestamp = datetime.datetime.now()
                exception_occurred = False

                WeatherData.objects.create(
                    city=city,
                    temperature=temp,
                    description=description,
                    icon=icon,
                    timestamp=timestamp
                )
                SearchHistory.objects.create(city=city)
            except (KeyError, requests.exceptions.RequestException):
                exception_occurred = True
                messages.error(request, 'Entered data is not available to API')
                city = 'Indore'
        else:
            latest_weather = WeatherData.objects.filter(city__iexact=city).order_by('-timestamp').first()
            if latest_weather:
                description = latest_weather.description
                temp = latest_weather.temperature
                icon = latest_weather.icon
                timestamp = latest_weather.timestamp
                exception_occurred = False
            else:
                exception_occurred = True
                messages.error(request, 'No weather data available for this city')
    else:
        city = 'Tashkent'

    weather_data = WeatherData.objects.filter(city__iexact=city).order_by('-timestamp')[:6]

    popular_cities = [history.city for history in SearchHistory.objects.all().order_by('-timestamp')]

    context = {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'timestamp': timestamp,
        'city': city,
        'exception_occurred': exception_occurred,
        'weather_data': weather_data,
        'popular_cities': popular_cities,
    }
    return render(request, 'weatherapp/index.html', context)

def export_weather_csv(request):
    city = request.GET.get('city') or 'Tashkent'
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not city:
        return HttpResponse("No city specified for export.", status=400)

    queryset = WeatherData.objects.filter(city__iexact=city)
    if start_date and end_date:
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        except ValueError:
            return HttpResponse("Invalid date format. Use YYYY-MM-DDTHH:MM format.", status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="weather_{city}.csv"'

    writer = csv.writer(response)
    writer.writerow(['City', 'Temperature (°C)', 'Description', 'Timestamp'])
    for data in queryset:
        writer.writerow([data.city, data.temperature, data.description, data.timestamp])

    return response

class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer