import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

sys.path.append(cityframe_path)

from drf_yasg import openapi
from django.db.models import Case, CharField, Value, When, F, Count
from django.db.models.functions import Greatest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response as RestResponse
from credentials import openweather_key, timezone_db_key
from api_endpoints.generate_response import generate_response, current_busyness
from .models import WeatherCurrent, Query, Response, TaxiZones, Zoning, Zones
import requests
import datetime
import pytz
from dateutil import tz
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


def convert_time_format(date_str, golden_hour_str):
    """This function converts the golden hour string provided by sunrisesunset API to a usable format

    Args:
        date_str
        golden_hour_str

    """
    # Create datetime object
    datetime_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    golden_hour = datetime.datetime.strptime(golden_hour_str, "%I:%M:%S %p")
    golden_hour = golden_hour.replace(year=datetime_obj.year, month=datetime_obj.month, day=datetime_obj.day)

    # Return formatted string
    return golden_hour.strftime("%Y-%m-%d %H:%M:%S")


def add_minutes_to_time(time_str, minutes):
    """This function adds (or subtracts) minutes to a time string

    Args:
        time_str (str): time string in the format "YYYY-MM-DD HH:MM:SS".
        minutes (int): number of minutes to add to the time. Can be negative to subtract minutes

    Returns:
        str: The calculated new time as a string in format "YYYY-MM-DD HH:MM:SS"

    """
    time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    new_time_obj = time_obj + datetime.timedelta(minutes=minutes)
    return new_time_obj.strftime("%Y-%m-%d %H:%M:%S")


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


class HiddenGemsDataView(APIView):
    def get(self, request):
        least_recommended_zones_ids = (
            Response.objects.values("zone_id")
            .annotate(count=Count("zone_id"))
            .order_by("count")[:10]
        )
        # get zone_ids from the results
        zone_ids = [zone["zone_id"] for zone in least_recommended_zones_ids]

        # Get the relevant TaxiZone objects
        zones = TaxiZones.objects.filter(id__in=zone_ids)

        response_data = {}
        for zone in zones:
            style_fields = {
                "neo-Georgian": zone.neo_georgian,
                "Greek Revival": zone.greek_revival,
                "Romanesque Revival": zone.romanesque_revival,
                "neo-Grec": zone.neo_grec,
                "Renaissance Revival": zone.renaissance_revival,
                "Beaux-Arts": zone.beaux_arts,
                "Queen Anne": zone.queen_anne,
                "Italianate": zone.italianate,
                "Federal": zone.federal,
                "neo-Renaissance": zone.neo_renaissance,
            }

            # Find the style with the max value
            max_style = max(style_fields, key=style_fields.get)

            response_data[zone.id] = {
                "zone_id": zone.id,
                "name": zone.zone,
                "trees": zone.trees,
                "main_style_amount": style_fields[max_style],
                "main_style": max_style,
            }

        return RestResponse(response_data)


# class CurrentSuntimesAPIView(APIView):
#     def get(self, request, formatting=None):
#
#         """Get request for current day's sunrise and sunset data
#
#         One optional argument ('formatting')
#
#         Returns json listing sunrise and sunset in unix timestamp format (with offset applied)
#         If formatting == 'datetime', returns a datetime string
#         """
#         url = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid={openweather_key}'
#         response = requests.get(url)
#         raw_data = response.json()
#         sunrise_timestamp = raw_data['sys']['sunrise']
#         sunset_timestamp = raw_data['sys']['sunset']
#         timezone_offset = raw_data['timezone']
#         sunrise_local = sunrise_timestamp + timezone_offset
#         sunset_local = sunset_timestamp + timezone_offset
#
#         # Check if the 'format' query parameter is provided
#         if formatting == 'datetime':
#             # Handle datetime format
#             processed_data = {
#                 'sunrise': convert_to_datetime_string(sunrise_local),
#                 'sunset': convert_to_datetime_string(sunset_local),
#             }
#         else:
#             # Handle default format
#             processed_data = {
#                 'sunrise': sunrise_local,
#                 'sunset': sunset_local,
#             }
#
#         return RestResponse(processed_data)


class CurrentSuntimesAPIView(APIView):
    def get(self, request):
        """Get request for current day's sunrise and sunset data, including golden and blue hours

        Returns json listing sunrise, sunset, golden and blue hours in datetime strings (local time)
        """
        # Get New York timezone and current date with PYTZ / datetime
        ny_tz = pytz.timezone('America/New_York')
        ny_datetime = datetime.datetime.now(ny_tz)
        today = ny_datetime.strftime('%Y-%m-%d')

        # data sources for accurate sunrise/sunset and evening golden hour times
        url_suntimes = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid=' \
                       f'{openweather_key}'
        url_golden_hr = f'https://api.sunrisesunset.io/json?lat=40.7831&lng=-73.9712&timezone=%22America/New_York%22' \
                        f'&date={today}'

        # retrieve sunrise / sunset data
        response_suntimes = requests.get(url_suntimes)
        raw_data = response_suntimes.json()
        sunrise_timestamp = raw_data['sys']['sunrise']
        sunset_timestamp = raw_data['sys']['sunset']
        timezone_offset = raw_data['timezone']

        # apply timezone offset for local time conversion, and convert to string
        sunrise_local = sunrise_timestamp + timezone_offset
        sunrise_local_str = convert_to_datetime_string(sunrise_local)
        sunset_local = sunset_timestamp + timezone_offset
        sunset_local_str = convert_to_datetime_string(sunset_local)

        # retrieve evening golden hour data
        response_golden = requests.get(url_golden_hr)
        golden_data = response_golden.json()

        # Extract relevant keys/values from the response
        golden_hour = golden_data['results']['golden_hour']
        golden_hour_formatted = convert_time_format(today, golden_hour)

        # we have a good data source for evening golden hour but not for its morning equivalent or for blue hours
        # These times are calculated below, assuming 30 minutes before/after sunrise/sunset
        blue_hour_morning_str = add_minutes_to_time(sunrise_local_str, -30)
        blue_hour_evening_str = add_minutes_to_time(sunset_local_str, 30)
        golden_hour_morning_str = add_minutes_to_time(sunrise_local_str, 30)

        processed_data = {
            'blue_hour_morning': blue_hour_morning_str,
            'sunrise': sunrise_local_str,
            'golden_hour_morning': golden_hour_morning_str,
            'golden_hour_evening': golden_hour_formatted,
            'sunset': sunset_local_str,
            'blue_hour_evening': blue_hour_evening_str,
        }

        # write to cache for future use w
        cache.set(today, processed_data, 1382400)

        return RestResponse(processed_data)


class SuntimesAPIView(APIView):
    def get(self, request, requested_date):
        """Get request for sunrise/sunset and blue/golden hour data

        Args:
            requested_date (str), a date in format yyyy-mm-dd, acceptable up to today+14 days new york time

        Returns:
            a json listing sunrise/sunset, golden/blue hours for that day in datetime string format (local time)
        """
        # Get New York timezone and current date with PYTZ / datetime
        ny_tz = pytz.timezone('America/New_York')
        ny_datetime = datetime.datetime.now(ny_tz)

        # sanitise input for requested_date
        if requested_date is not None:
            try:
                datetime.datetime.strptime(requested_date, '%Y-%m-%d')
            except ValueError:
                return RestResponse({'error': 'Invalid date format. It should be in the format "YYYY-MM-DD".'},
                                    status=status.HTTP_400_BAD_REQUEST)

        processed_data = cache.get(requested_date)

        if processed_data is not None:
            # If there is data in the cache, return it
            # for debugging
            print(f"\nSuntimes for {requested_date} fetched from Cache")
            return RestResponse(processed_data)
        else:
            # Convert future_date to a datetime.date object, compare to today and calculate difference in days
            requested_date_obj = datetime.datetime.strptime(requested_date, '%Y-%m-%d').date()
            time_difference = requested_date_obj - ny_datetime.date()
            days_in_future = time_difference.days

            if requested_date_obj.day == ny_datetime.day:
                current_suntimes_view = CurrentSuntimesAPIView()
                return current_suntimes_view.get(request)
            else:
                # data sources for accurate sunrise/sunset and evening golden hour times
                url = f'https://api.openweathermap.org/data/2.5/forecast/daily?' \
                      f'lat=40.7831&lon=-73.9712&cnt=16&appid={openweather_key}'
                url_golden_hr = f'https://api.sunrisesunset.io/json?lat=40.7831&lng=-73.9712&timezone=%22America/New_York%22' \
                                f'&date={requested_date}'

                # retrieve sunrise / sunset data
                suntimes_response = requests.get(url)
                suntimes_data = suntimes_response.json()

                # Filter the data based on days_in_future
                filtered_data = suntimes_data['list'][
                    days_in_future]  # Adjusting index since days_in_future starts from 1

                # calculate sunrise and sunset with offset applied
                timezone_offset = suntimes_data['city']['timezone']
                sunrise_timestamp = filtered_data['sunrise']
                sunset_timestamp = filtered_data['sunset']
                sunrise_local = sunrise_timestamp + timezone_offset
                sunrise_local_str = convert_to_datetime_string(sunrise_local)
                sunset_local = sunset_timestamp + timezone_offset
                sunset_local_str = convert_to_datetime_string(sunset_local)

                # retrieve evening golden hour data
                response_golden = requests.get(url_golden_hr)
                golden_data = response_golden.json()

                # Extract relevant keys/values from the response
                golden_hour = golden_data['results']['golden_hour']
                golden_hour_formatted = convert_time_format(requested_date, golden_hour)

                # we have a good data source for evening golden hour but not for its morning equivalent or for blue hours
                # These times are calculated below, assuming 30 minutes before/after sunrise/sunset
                blue_hour_morning_str = add_minutes_to_time(sunrise_local_str, -30)
                blue_hour_evening_str = add_minutes_to_time(sunset_local_str, 30)
                golden_hour_morning_str = add_minutes_to_time(sunrise_local_str, 30)

                # format data correctly for the expected response
                processed_data = {
                    'blue_hour_morning': blue_hour_morning_str,
                    'sunrise': sunrise_local_str,
                    'golden_hour_morning': golden_hour_morning_str,
                    'golden_hour_evening': golden_hour_formatted,
                    'sunset': sunset_local_str,
                    'blue_hour_evening': blue_hour_evening_str,
                }

                # adds data to cache, timeout of 16 days (in seconds)
                cache.set(requested_date, processed_data, 1382400)

                return RestResponse(processed_data)


# class FutureSuntimesAPIView(APIView):
#     def get(self, request, days_in_future, formatting=None):
#         """Get request for future sunrise and sunset data
#         Takes one argument, days_in_future, an int between 1-5 inclusive (representing a number of days into the future)
#         Returns a json listing sunrise and sunset for that day in unix timestamp format (with offset applied)
#         """
#         url = f'https://api.openweathermap.org/data/2.5/forecast/daily?' \
#               f'lat=40.7831&lon=-73.9712&cnt=16&appid={openweather_key}'
#         response = requests.get(url)
#         data = response.json()
#         timezone_offset = data['city']['timezone']
#
#         # Filter the data based on days_in_future
#         filtered_data = data['list'][days_in_future]  # Adjusting index since days_in_future starts from 1
#
#         # calculate sunrise and sunset with offset applied
#         sunrise_timestamp = filtered_data['sunrise']
#         sunset_timestamp = filtered_data['sunset']
#         sunrise_local = sunrise_timestamp + timezone_offset
#         sunset_local = sunset_timestamp + timezone_offset
#
#         if formatting == 'datetime':
#             # Handle datetime format
#             processed_data = {
#                 'sunrise': convert_to_datetime_string(sunrise_local),
#                 'sunset': convert_to_datetime_string(sunset_local),
#             }
#         else:
#             # format data correctly for the expected response
#             processed_data = {
#                 'sunrise': sunrise_local,
#                 'sunset': sunset_local
#             }
#
#         return RestResponse(processed_data)


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

        # sanitise input for 'formatting'
        if formatting is not None and formatting != 'datetime':
            return RestResponse({'error': 'Invalid formatting type. "datetime" is the only valid option.'},
                                status=status.HTTP_400_BAD_REQUEST)

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
    """Get request for the current busyness data in Manhattan

    Returns a JSON with each taxi zone and corresponding busyness level
    """

    def get(self, request):
        busyness_data = cache.get('current_busyness')

        if busyness_data is not None and len(busyness_data) > 0:
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


class TaxiZoneDataView(APIView):
    """Get request for general data for each taxi zone

    Returns:
        JSON with each taxi zone as a key, with corresponding name (str), number of trees (int) and
        main architectural style (string) as values
    """

    def get(self, request):

        zone_data = cache.get('zone_data')

        if zone_data is not None:
            print('zone data fetched from cache')
            return RestResponse(zone_data)
        else:
            queryset = Zones.objects.all()
            results = {}

            for obj in queryset:
                result = {
                    'zone': obj.zone,
                    'trees': obj.trees,
                    'zone_type': obj.main_zone_type,
                    'main_style': obj.main_zone_style
                }

                results[str(obj.location_id)] = result

            # Add the data to the cache, with a timeout of 90 days (in seconds)
            cache.set('zone_data', results, 7776000)

            return RestResponse(results)


class MainFormSubmissionView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'busyness': openapi.Schema(type=openapi.TYPE_INTEGER, description='Busyness'),
                'trees': openapi.Schema(type=openapi.TYPE_INTEGER, description='Trees'),
                'time': openapi.Schema(type=openapi.TYPE_STRING, description='Time string'),
                'style': openapi.Schema(type=openapi.TYPE_STRING, description='Style'),
                'weather': openapi.Schema(type=openapi.TYPE_STRING, description='Weather'),
            }
        ),
        responses={200: ResponseSerializer(many=True)}
    )
    def post(self, request):
        time = request.data.get('time')
        busyness = int(request.data.get('busyness'))
        trees = int(request.data.get('trees'))
        style = str.lower(request.data.get('style'))
        zone_type = str.lower(request.data.get('zone_type'))
        # weather = request.data.get('weather', None)
        weather = request.data.get('weather', None)

        # If user chooses 'All' option, set weather to None
        if weather == 'all':
            weather = None

        # Sanitise busyness and trees inputs
        try:
            busyness = int(busyness)
            trees = int(trees)
        except ValueError:
            return RestResponse({'error': 'Busyness and Trees should be integers.'}, status=status.HTTP_400_BAD_REQUEST)

        if not (1 <= busyness <= 5) or not (1 <= trees <= 5):
            return RestResponse({'error': 'Busyness and Trees should be in the range 1-5 inclusive.'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Sanitise style input
        valid_styles = ['all', 'neo-georgian', 'greek revival', 'romanesque revival', 'neo-grec', 'renaissance revival',
                        'beaux-arts', 'queen anne', 'italianate', 'federal', 'neo-renaissance']
        if style not in valid_styles:
            return RestResponse({'error': 'Invalid style.'}, status=status.HTTP_400_BAD_REQUEST)

        # Sanitise zone type input
        valid_types = ['all', 'commercial', 'manufacturing', 'park', 'residential']
        if zone_type not in valid_types:
            return RestResponse({'error': 'Invalid zone type.'}, status=status.HTTP_400_BAD_REQUEST)

        # Sanitise time input
        try:
            datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        except ValueError:
            return RestResponse({'error': 'Invalid time format. It should be in the format "YYYY-MM-DD HH:MM".'},
                                status=status.HTTP_400_BAD_REQUEST)

        # handles the retrieval of optional parameter 'weather', sanitises input
        try:
            weather_list = ['clear', 'clouds', 'drizzle', 'fog', 'haze', 'mist', 'rain', 'smoke', 'snow', 'squall',
                            'thunderstorm']
            if weather is not None:
                weather = str.lower(weather)
                assert weather in weather_list
        except AssertionError:
            return RestResponse({'error': 'Invalid weather type.'}, status=status.HTTP_400_BAD_REQUEST)

        # prints data for debugging
        print(f"busyness: {busyness}")
        print(f"trees: {trees}")
        print(f"style: {style}")
        print(f"zone type: {zone_type}")
        print(f"time: {time}")
        print(f"weather preference: {weather}")

        ny_tz = pytz.timezone('America/New_York')
        query_time = timezone.now().astimezone(ny_tz)

        # consider adding weather column in the Query model
        query = Query.objects.create(
            time=time,
            busyness=busyness,
            trees=trees,
            style=style,
            zone_type=zone_type,
            query_time=query_time,
        )
        results = generate_response(target_busyness=busyness, target_trees=trees, target_style=style, target_dt=time,
                                    target_type=zone_type, weather=weather)

        # handle empty results (e.g., user searches for 'snow' in summer)
        if not results:
            return RestResponse({'error': 'No results found for the given parameters.'},
                                status=status.HTTP_400_BAD_REQUEST)

        responses = []

        for zone_data in results.values():
            zone_data['zone_id'] = zone_data.pop('id')
            zone_data['submission_id'] = query.id
            responses.append(Response(**zone_data))

        Response.objects.bulk_create(responses)

        for zone_data in results.values():
            zone_data['id'] = zone_data.pop('zone_id')

        print(results)  # for debugging, remove later
        return RestResponse(results)
