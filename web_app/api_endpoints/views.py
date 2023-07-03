from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from data_apis.creds import openweather_key
import json


# class FutureWeatherAPIView(APIView):
#     def get(self, request):
#         url = 'https://pro.openweathermap.org/data/2.5/forecast/hourly?' \
#               'lat=40.7831&lon=-73.9712&appid={openweather_key}'
#         response = requests.get(url)
#         data = response.json()
#         return Response(data)
#
#     def get(self, request, datetime):
#         """Get request for predicted weather data
#             Takes one argument, DTG (UTC) in format "YYYY-MM-DD HH:MM:SS"
#             Returns JSON data for requested time (UTC)
#             """
#         url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=40.7831&lon=-73.9712&appid={openweather_key}'
#         response = requests.get(url)
#         data = response.json()
#         """now filter the data for the relevant
#         datetime
#         """
#         return Response(data)


class CurrentWeatherAPIView(APIView):
    def get(self, request):
        """add
        docstring
        here
        """
        url = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid={openweather_key}'
        response = requests.get(url)
        data = response.json()
        return Response(data)


# class FutureWeatherAPIView(APIView):
#     def get(self, request, datetime):
#         """Get request for predicted weather data
#             Takes one argument, datetime (UNIX  UTC)
#             Returns JSON data for the closest match to the provided datetime (UNIX UTC)
#         """
#         url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=40.7831&lon=-73.9712&appid={openweather_key}'
#         response = requests.get(url)
#         data = response.json()
#
#         # Find the closest match to the provided datetime
#         closest_match = min(data['list'], key=lambda x: abs(x['dt_txt'] == datetime))
#
#         return Response(closest_match)

class FutureWeatherAPIView(APIView):
    def get(self, request, timestamp):
        """Get request for predicted weather data
            Takes one argument, Unix timestamp in UTC (e.g. 1688421600)
            Returns JSON data for the closest match to the provided timestamp
        """
        url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?' \
              f'lat=40.7831&lon=-73.9712&appid=\{openweather_key}'
        response = requests.get(url)
        data = response.json()

        # Find the closest match to the provided datetime
        closest_match = min(data['list'], key=lambda x: abs(x['dt'] - int(timestamp)))

        return Response(closest_match)


class CurrentSuntimesAPIView(APIView):
    def get(self, request):
        """Get request for current day's sunrise and sunset data
        No argument
        Returns json listing sunrise and sunset in unix timestamp format (local time)
        """
        url = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid={openweather_key}'
        response = requests.get(url)
        raw_data = response.json()
        sunrise_timestamp = raw_data['sys']['sunrise']
        sunset_timestamp = raw_data['sys']['sunset']
        timezone_offset = raw_data['timezone']
        sunrise_local = sunrise_timestamp + timezone_offset
        sunset_local = sunset_timestamp + timezone_offset

        processed_data = {
            'sunrise': sunrise_local,
            'sunset': sunset_local
        }

        return Response(processed_data)


class FutureSuntimesAPIView(APIView):
    def get(self, request, days_in_future):
        """docstring here
        takes one argument, days_in_future, an int between 1-5 inclusive (representing a number of days into the future)
        returns a json listing sunrise and sunset for that day in unix timestamp format (local time)
        """
        url = f'https://api.openweathermap.org/data/2.5/forecast/daily?' \
              f'lat=40.7831&lon=-73.9712&cnt=5&appid={openweather_key}'
        response = requests.get(url)
        data = response.json()

        # now do something with days_in_future
        return Response(data)
