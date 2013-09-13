import pywapi

# Wrapper around pywapi weather.com api


def current(zip):
    weather = pywapi.get_weather_from_weather_com(location_id=zip, units='imperial')


def forcast(zip):
    my_forcast = pywapi.get_weather_from_weather_com(location_id=zip, units='imperial')
