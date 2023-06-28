from data_apis.apiupdate import WeatherHourlyUpdate

if __name__ == '__main__':
    weather_update = WeatherHourlyUpdate()
    weather_update.update(overwrite=True)
