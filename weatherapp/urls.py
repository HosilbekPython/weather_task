from django.urls import path , include
from weatherapp.views import WeatherDataViewSet, home, export_weather_csv
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'weather', WeatherDataViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('export/', export_weather_csv, name='export_weather_csv'),
    path('api/', include(router.urls)),
]