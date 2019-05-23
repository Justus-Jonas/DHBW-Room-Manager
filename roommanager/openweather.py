import pyowm
import datetime
from time import gmtime, strftime, ctime
from roommanager.models import Forecast
def getCurrentWeather():
    owm = pyowm.OWM('d12bf70afc7467861163ebdc67a1642d')
    fore = owm.three_hours_forecast('Mannheim')
    forecast = fore.get_forecast()
    forecast_list = []
    weather_list = forecast.get_weathers()
    for weather in weather_list:
        temp_date_ob = datetime.datetime.strptime(weather.get_reference_time('iso'), '%Y-%m-%d %H:%M:%S+%f')
        weather_date = temp_date_ob.date()
        weather_time = temp_date_ob.time()
        temp = str(weather.get_temperature()["temp"])
        forecast_list.append([ weather_date, weather_time, temp])
        forecast = Forecast(forecastdate=weather_date, forecasttime=weather_time, temp=temp)
        forecast.save()
    return forecast_list


def analyseWeather(forecast_list):
    current_dates = datetime.datetime.strptime(strftime('%Y-%m-%d %H:%M:%S', gmtime()), '%Y-%m-%d %H:%M:%S')
    current_time = current_dates.time()
    current_date = current_dates.date()
    for forecast_date, forecast_time, weather in forecast_list:
        if forecast_date > current_date:
            print(forecast_date)




currentWeatherList = getCurrentWeather()
analyseWeather(currentWeatherList)

