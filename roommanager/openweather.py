import pyowm
from time import gmtime, strftime

def getCurrentWeather():
    owm = pyowm.OWM('d12bf70afc7467861163ebdc67a1642d')
    fore = owm.three_hours_forecast('Mannheim')
    forecast = fore.get_forecast()
    print(forecast.get_reception_time('date'))
    print(len(forecast))
    list = []
    weather_list = forecast.get_weathers()
    for weather in weather_list:
        date = weather.get_reference_time('iso')
        temp = str(weather.get_temperature()["temp"])
        list.append([date, temp])
    return list


def analyseWeather(forecast_list):
    current_time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    print(current_time)
    for date, weather in forecast_list:
        print(date + weather)

currentWeatherList = getCurrentWeather()
analyseWeather(currentWeatherList)

