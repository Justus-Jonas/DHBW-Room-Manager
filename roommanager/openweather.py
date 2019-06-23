from roommanager.models import Forecast
from datetime import datetime
import requests

def get_weather(api_key, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    r = requests.get(url)
    return r.json()

def getCurrentWeather():
    try:
        weather = get_weather("d12bf70afc7467861163ebdc67a1642d", "Mannheim")
        temp = weather['main']['temp']
        now = datetime.now()

        Forecast.objects.all().delete()
        fc = Forecast(temp=temp, forecastdate=now, forecasttime=now.time())
        fc.save()
    except:
        # print("weather api max tries exceeded")
        pass
