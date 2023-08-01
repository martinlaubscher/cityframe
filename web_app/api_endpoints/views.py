import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

sys.path.append(cityframe_path)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response as RestResponse
from credentials import openweather_key, timezone_db_key
from api_endpoints.get_results import generate_response, current_busyness
from .models import WeatherCurrent, Query, Response
import requests
import datetime
import pytz
from django.core.cache import cache
from django.utils import timezone


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
            RestResponse(weather_data): JSON data of current Manhattan weather
        """
        # Try to get the data from the cache
        weather_data = cache.get('current_weather')

        if weather_data is not None:
            # If there is data in the cache, return it
            # for debugging
            print("\nWeather data fetched from Cache")

            return RestResponse(weather_data)
        else:
            # Try to get the data from the database
            weather_data = WeatherCurrent.get_current()

            if weather_data is not None:
                # If there is data in the database, return it
                # for debugging
                print("\nWeather data fetched from Database")

                # Add the data to the cache, with a timeout of 5 minutes
                cache.set('current_weather', weather_data, 300)

                return RestResponse(weather_data)
            else:
                # If no data in the database, fetch from the OpenWeather API
                url = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid={openweather_key}'
                response = requests.get(url)
                weather_data = response.json()

                # for debugging
                print("\nWeather data fetched from openweather API call")

                # Store the new data in the cache for next time
                cache.set('current_weather', weather_data, 300)

                return RestResponse(weather_data)


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

        return RestResponse(closest_match)


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

        return RestResponse(processed_data)


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

        return RestResponse(processed_data)


class GoldenHourAPIView(APIView):
    def get(self, request, chosen_date):
        """Get request for predicted weather data

        Args:
            chosen_date (String): format "yyyy-mm-dd"

        Returns:
            filtered_data (JSON): JSON data containing golden hour and sunset in format "H:MM:SS PM"
        """
        url = f'https://api.sunrisesunset.io/json?lat=40.7831&lng=-73.9712&timezone=%22America/New_York%22' \
              f'&date={chosen_date}'
        response = requests.get(url)
        data = response.json()

        # Extract relevant keys/values from the response
        golden_hour = data['results']['golden_hour']
        sunset = data['results']['sunset']

        filtered_data = {
            'golden_hour': golden_hour,
            'sunset': sunset
        }

        return RestResponse(filtered_data)


# The below provider had an incorrect offset, meaning local time was one hour off. Potential backup if issue fixed.
# url = 'http://worldtimeapi.org/api/timezone/America/New_York'

class CurrentManhattanTimeAPIView(APIView):
    def get(self, request, formatting=None):
        """Get request for the current time in Manhattan

        One optional argument ('formatting')

        Returns a JSON of the current Unix timestamp (with offset applied)
        If formatting == 'datetime', returns a JSON with datetime string
        """
        url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={timezone_db_key}&format=json&by=position&' \
              f'lat=40.7831&lng=-73.9712'
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

        return RestResponse(processed_data)


class CurrentManhattanBusyness(APIView):
    def get(self, request):
        busyness_data = cache.get('current_busyness')

        if busyness_data is not None:
            # If there is data in the cache, return it
            # for debugging
            print("\nBusyness data fetched from Cache")
            return RestResponse(busyness_data)
        else:
            busyness_data = current_busyness()
            # adds data to cache, timeout of 5 minutes
            cache.set('current_busyness', busyness_data, 300)
            print("\nBusyness data fetched from DB")
            return RestResponse(busyness_data)


class ResponseSerializer(serializers.Serializer):
    # Add fields for all properties in your response
    time = serializers.DateTimeField()
    busyness = serializers.IntegerField()
    trees = serializers.IntegerField()
    style = serializers.CharField()
    submission_id = serializers.IntegerField()


class MainFormSubmissionView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'busyness': openapi.Schema(type=openapi.TYPE_INTEGER, description='Busyness'),
                'trees': openapi.Schema(type=openapi.TYPE_INTEGER, description='Trees'),
                'time': openapi.Schema(type=openapi.TYPE_STRING, description='Time string'),
                'style': openapi.Schema(type=openapi.TYPE_STRING, description='Style'),
            }
        ),
        responses={200: ResponseSerializer(many=True)}
    )
    def post(self, request):
        time = request.data.get('time')
        busyness = int(request.data.get('busyness'))
        trees = int(request.data.get('trees'))
        style = request.data.get('style')
        print(f"busyness: {busyness}")
        print(f"trees: {trees}")
        print(f"style: {style}")
        print(f"time: {time}")

        ny_tz = pytz.timezone('America/New_York')
        query_time = timezone.now().astimezone(ny_tz)

        query = Query.objects.create(
            time=time,
            busyness=busyness,
            trees=trees,
            style=style,
            query_time=query_time,
        )
        results = generate_response(busyness, trees, style, time)

        responses = []

        for zone_id, zone_data in results.items():
            zone_data['zone_id'] = zone_id
            zone_data['submission_id'] = query.id
            responses.append(Response(**zone_data))

        Response.objects.bulk_create(responses)

        print(results)  # for debugging, remove later
        return RestResponse(results)
