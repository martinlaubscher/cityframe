import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

from apiupdate import WeatherHourlyUpdate, WeatherDailyUpdate

def main():
    weather_update_hourly = WeatherHourlyUpdate()
    weather_update_hourly.update(overwrite=True)
    weather_update_daily = WeatherDailyUpdate()
    weather_update_daily.update()


if __name__ == '__main__':
    main()
