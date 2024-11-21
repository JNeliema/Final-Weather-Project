import urllib.request
import json
from django.shortcuts import render # type: ignore
from datetime import datetime

# Create your own views here
def fetch_weather_data(city):
    api_key = '<YOUR_API_KEY>'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    source = urllib.request.urlopen(url).read()
    return json.loads(source)

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        list_of_data = fetch_weather_data(city)

        # Extract weather condition and background customization
        weather_condition = list_of_data['weather'][0]['main'].lower()

        # Extract sunrise and sunset times
        sunrise = datetime.fromtimestamp(list_of_data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(list_of_data['sys']['sunset']).strftime('%H:%M:%S')

        # Set dynamic background based on weather condition
        if 'rain' in weather_condition:
            background = 'rainy.jpg'
        elif 'clear' in weather_condition:
            background = 'clear_sky.jpg'
        elif 'cloud' in weather_condition:
            background = 'cloudy.jpg'
        else:
            background = 'default.jpg'

        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + ' °C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "main": str(list_of_data['weather'][0]['main']),
            "description": str(list_of_data['weather'][0]['description']),
            "icon": list_of_data['weather'][0]['icon'],
            'sunrise': sunrise,
            'sunset': sunset,
            'background': background
        }

    else:
        data = {}

    return render(request, "main/index.html", data)
