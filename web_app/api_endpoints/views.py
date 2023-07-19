from rest_framework.views import APIView
from rest_framework.response import Response
from data_apis.creds import openweather_key, timezone_db_key
from .models import WeatherFc, WeatherCurrent
import requests
import datetime


def convert_to_datetime_string(timestamp):
    """This function converts a timestamp to a datetime string
    It is intended for use with timestamps with timezone offset already applied

    Args:
        timestamp (int): a unix timestamp

    Returns:
        dt_string: the timestamp converted to datetime string
    """
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    dt_string = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt_string


class CurrentWeatherAPIView(APIView):
    def get(self, request):
        """Get request for current weather

        Returns:
            Response(weather_data): JSON data of current Manhattan weather
        """
        # Try to get the data from the database
        weather_data = WeatherCurrent.get_current()

        if weather_data is not None:
            # If there is data in the database, return it
            # for debugging
            print("\nWeather data fetched from Database")

            return Response(weather_data)

        else:
            # If no data in the database, fetch from the OpenWeather API
            url = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid={openweather_key}'
            response = requests.get(url)
            weather_data = response.json()

            # for debugging
            print("\nWeather data fetched from openweather API call")

            return Response(weather_data)
            # return Response({"error": "No weather data found in the database"}, status=500)


class FutureWeatherAPIView(APIView):
    def get(self, request, timestamp):
        """Get request for predicted weather data

        Takes one argument, Unix timestamp in UTC, e.g. 1688810400 (this is to match with openweather data)

        Returns JSON data for the closest match to the provided timestamp
        """
        url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?' \
              f'lat=40.7831&lon=-73.9712&appid={openweather_key}'
        response = requests.get(url)
        data = response.json()

        # Find the closest match to the provided datetime
        closest_match = min(data['list'], key=lambda x: abs(x['dt'] - int(timestamp)))

        return Response(closest_match)


class CurrentSuntimesAPIView(APIView):
    def get(self, request, formatting=None):

        """Get request for current day's sunrise and sunset data

        One optional argument ('formatting')

        Returns json listing sunrise and sunset in unix timestamp format (with offset applied)
        If formatting == 'datetime', returns a datetime string
        """
        url = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid={openweather_key}'
        response = requests.get(url)
        raw_data = response.json()
        sunrise_timestamp = raw_data['sys']['sunrise']
        sunset_timestamp = raw_data['sys']['sunset']
        timezone_offset = raw_data['timezone']
        sunrise_local = sunrise_timestamp + timezone_offset
        sunset_local = sunset_timestamp + timezone_offset

        # Check if the 'format' query parameter is provided
        if formatting == 'datetime':
            # Handle datetime format
            processed_data = {
                'sunrise': convert_to_datetime_string(sunrise_local),
                'sunset': convert_to_datetime_string(sunset_local),
            }
        else:
            # Handle default format
            processed_data = {
                'sunrise': sunrise_local,
                'sunset': sunset_local,
            }

        return Response(processed_data)


class FutureSuntimesAPIView(APIView):
    def get(self, request, days_in_future, formatting=None):
        """Get request for future sunrise and sunset data
        Takes one argument, days_in_future, an int between 1-5 inclusive (representing a number of days into the future)
        Returns a json listing sunrise and sunset for that day in unix timestamp format (with offset applied)
        """
        url = f'https://api.openweathermap.org/data/2.5/forecast/daily?' \
              f'lat=40.7831&lon=-73.9712&cnt=6&appid={openweather_key}'
        response = requests.get(url)
        data = response.json()
        timezone_offset = data['city']['timezone']

        # Filter the data based on days_in_future
        filtered_data = data['list'][days_in_future]  # Adjusting index since days_in_future starts from 1

        # calculate sunrise and sunset with offset applied
        sunrise_timestamp = filtered_data['sunrise']
        sunset_timestamp = filtered_data['sunset']
        sunrise_local = sunrise_timestamp + timezone_offset
        sunset_local = sunset_timestamp + timezone_offset

        if formatting == 'datetime':
            # Handle datetime format
            processed_data = {
                'sunrise': convert_to_datetime_string(sunrise_local),
                'sunset': convert_to_datetime_string(sunset_local),
            }
        else:
            # format data correctly for the expected response
            processed_data = {
                'sunrise': sunrise_local,
                'sunset': sunset_local
            }

        return Response(processed_data)


# The below provider had an incorrect offset, meaning local time was one hour off. Potential backup if issue fixed.
# url = 'http://worldtimeapi.org/api/timezone/America/New_York'

class CurrentManhattanTimeAPIView(APIView):
    def get(self, request, formatting=None):
        """Get request for the current time in Manhattan
        One optional argument ('formatting')
        Returns a JSON of the current Unix timestamp (with offset applied)
        If formatting == 'datetime', returns a JSON with datetime string
        """
        url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={timezone_db_key}&format=json&by=position&lat=40.7831&lng=-73.9712'
        response = requests.get(url)
        data = response.json()

        # the data provided by this API already has the offset applied
        unix_time = data['timestamp']

        if formatting == 'datetime':
            # Handle datetime format
            processed_data = {
                'datetime': convert_to_datetime_string(unix_time),
            }
        else:
            # format data correctly for the expected response
            processed_data = {
                'timestamp': unix_time
            }

        return Response(processed_data)

# now create an endpoint for golden hour
