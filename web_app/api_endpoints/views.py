from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from data_apis.creds import openweather_key, timezone_db_key


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
        """Get request for current weather
        No arguments
        Returns JSON data of current Manhattan weather
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
    def get(self, request):
        """Get request for current day's sunrise and sunset data
        No argument
        Returns json listing sunrise and sunset in unix timestamp format (with offset applied)
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
        """Get request for future sunrise and sunset data
        Takes one argument, days_in_future, an int between 1-5 inclusive (representing a number of days into the future)
        Returns a json listing sunrise and sunset for that day in unix timestamp format (with offset applied)
        """
        url = f'https://api.openweathermap.org/data/2.5/forecast/daily?' \
              f'lat=40.7831&lon=-73.9712&cnt=5&appid={openweather_key}'
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

        # format data correctly for the expected response
        processed_data = {
            'sunrise': sunrise_local,
            'sunset': sunset_local
        }

        # now do something with days_in_future
        return Response(processed_data)


# The below provider had an incorrect offset, meaning local time was one hour off
# class CurrentManhattanTimeAPIView(APIView):
#     def get(self, request):
#         """Get request for the current time in Manhattan
#         No argument
#         Returns a JSON of the current Unix timestamp (with offset applied)
#         """
#         url = 'http://worldtimeapi.org/api/timezone/America/New_York'
#         response = requests.get(url)
#         data = response.json()
#         unix_time = data['unixtime']
#         raw_offset = data['raw_offset']
#         current_time = unix_time + raw_offset
#
#         return Response(current_time)

class CurrentManhattanTimeAPIView(APIView):
    def get(self, request):
        """Get request for the current time in Manhattan
        No argument
        Returns a JSON of the current Unix timestamp (with offset applied)
        """
        url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={timezone_db_key}&format=json&by=position&lat=40.7831&lng=-73.9712'
        response = requests.get(url)
        data = response.json()

        # the data provided by this API already has the offset applied
        unix_time = data['timestamp']

        # format data correctly for the expected response
        processed_data = {
            'timestamp': unix_time
        }

        return Response(processed_data)

# now create an endpoint for golden hour