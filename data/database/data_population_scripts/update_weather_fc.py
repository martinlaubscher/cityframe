from apiupdate import WeatherHourlyUpdate, WeatherDailyUpdate

if __name__ == '__main__':
    weather_update_hourly = WeatherHourlyUpdate()
    weather_update_hourly.update(overwrite=True)
    weather_update_daily = WeatherDailyUpdate()
    weather_update_daily.update()
