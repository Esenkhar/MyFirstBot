import requests
import os
from datetime import datetime
import zoneinfo

OWM_key = os.getenv('OWM_TOKEN')

def get_weather(city):
    api_key = OWM_key
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'en'
    }
    response = requests.get(base_url, params=params)
    return response.json()

def process_weather_data(city):
    weather_data = get_weather(city)
    if weather_data.get('cod') != 200:
        return 'City is not found'

    city = weather_data['name']
    weather = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']

    # Преобразуем время с учетом часового пояса
    tz = zoneinfo.ZoneInfo("Europe/Kyiv")
    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise'], tz=zoneinfo.ZoneInfo("UTC")).astimezone(tz)
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset'], tz=zoneinfo.ZoneInfo("UTC")).astimezone(tz)

    return (f'Weather in {city}:\n'
            f'Description: {weather}\n'
            f'Temperature: {int(temp)}°C\n'
            f'Humidity: {humidity}%\n'
            f'Pressure: {int(pressure * 0.75006375541921)} mmHg\n'
            f'Wind speed: {int(wind_speed)} m/s\n'
            f'Sunrise: {sunrise.strftime("%H:%M:%S")}\n'
            f'Sunset: {sunset.strftime("%H:%M:%S")}'
            )

if __name__ == '__main__':
    print(process_weather_data('Харьков'))
