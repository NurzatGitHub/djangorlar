from django.shortcuts import render
from datetime import datetime
import pytz
# Create your views here.
def city_time(request):
    city = request.GET.get('city', 'UTC')
    cities = {
        'New York': 'America/New_York',
        'London': 'Europe/London',
        'Tokyo': 'Asia/Tokyo',
        'UTC': 'UTC'
    }
    
    tz = pytz.timezone(cities.get(city, 'UTC'))
    current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'citytime/city_time.html', {'city': city, 'time': current_time, 'cities': cities.keys()})