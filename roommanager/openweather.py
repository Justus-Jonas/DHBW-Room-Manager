import pyowm
from roommanager.models import Forecast
import datetime
from time import gmtime, strftime, ctime

def getCurrentWeather():
    """Open Weather Map API Request. Current weather for Mannheim is requested"""
    owm = pyowm.OWM('d12bf70afc7467861163ebdc67a1642d')
    fore = owm.three_hours_forecast('Mannheim')
    forecast = fore.get_forecast()
    weather_list = forecast.get_weathers()
    weather = weather_list[0]
    temp_date_ob = datetime.datetime.strptime(weather.get_reference_time('iso'), '%Y-%m-%d %H:%M:%S+%f')
    forecastdate = temp_date_ob.date()
    forecasttime = temp_date_ob.time()

    temp = float(weather.get_temperature(unit='celsius')["temp"])
    Forecast.objects.all().delete()
    fc = Forecast()
    fc.temp = temp
    print(temp)
    fc.save()




