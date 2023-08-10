import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

sys.path.append(cityframe_path)

from sqlalchemy import create_engine, URL, MetaData, Table, delete, select, func
from sqlalchemy.dialects.postgresql import insert
import requests
import json
from datetime import datetime
from dateutil import tz
from credentials import pg_conn, openweather_key


class ApiUpdate:
    """
    Base class for API updates from various sources.

    This class handles the common tasks involved in updating data from an API,
    including making the API request, preparing the response data, and inserting the data into a table.

    Specific APIs can be handled by subclassing `ApiUpdate` and implementing the `extract_data` and `prep_data` methods
    as required for the specific API.
    """

    def __init__(self, schema_name, table_name, url, params):
        """
        Initialises the ApiUpdate instance.

        Args:
            schema_name (str): Name of the schema where the table to insert data to is located
            table_name (str): Name of the table to insert the data into
            url (str): URL of the API endpoint
            params (dict): Parameters to pass to the API request
        """

        pg_url = URL.create(
            "postgresql+psycopg",
            **pg_conn
        )

        self.engine = create_engine(pg_url)
        self.table = Table(table_name, MetaData(), autoload_with=self.engine, schema=schema_name)
        self.url = url
        self.params = params

    def get_api_response(self):
        """
        Sends a GET request to the API endpoint and returns the response.

        Returns:
            response (requests.Response): Response from the API
        """

        response = requests.get(self.url, params=self.params)

        if response.status_code != 200:
            raise Exception('API request failed with status code: {}'.format(response.status_code))

        return response

    def insert_into_table(self, text, overwrite=False):
        """
        Inserts the prepared data into the specified table.

        Args:
            text (str): JSON data as text
            overwrite (bool): Specifies whether the data in the table should be overwritten (optional, default = False)
        """

        data = self.extract_data(json.loads(text))
        vals = tuple(map(self.prep_data, data))

        with self.engine.begin() as connection:
            if overwrite:
                delete_stmt = delete(self.table)
                connection.execute(delete_stmt)

            insert_stmt = insert(self.table)
            connection.execute(insert_stmt, vals)

    def update(self, overwrite=False):
        """
        Updates the data table with new data from the API.

        Args:
            overwrite (bool): Specifies whether the existing data in the table should be overwritten (optional, default = False)
        """

        response = self.get_api_response()
        self.insert_into_table(response.text, overwrite=overwrite)

    @staticmethod
    def extract_data(data):
        """
        Extracts the relevant data from the API response.

        This method should be overridden in a subclass if specific data extraction is required.

        Args:
            data(dict): Dictionary containing the raw data from the API

        Returns:
            data(dict): Dictionary containing the extracted data from the API response
        """

        return data

    @staticmethod
    def prep_data(data):
        """
        Prepares the data for insertion into the database.

        This method should be overridden in a subclass if specific data preparation is required.

        Args:
            data(dict): Dictionary containing the extracted data

        Returns:
            data(dict): Dictionary containing the prepared data for database insertion
        """

        return data


class WeatherHourlyUpdate(ApiUpdate):
    """
    Subclass of ApiUpdate for updating hourly weather data from the OpenWeather API.

    This subclass overrides the extract_data and prep_data methods to handle the specifics of the OpenWeather API and
    the weather forecast data.
    """

    def __init__(self):
        """
        Initialises the WeatherHourlyUpdate instance.

        The schema name is set to "cityframe", the table name to "weather_fc",
        the URL to the OpenWeather forecast API endpoint, and the parameters to the required latitude, longitude,
        and API key.
        """

        params = {"lat": "40.78306", "lon": "-73.971249", "appid": openweather_key}
        super().__init__("cityframe", "weather_fc", "https://pro.openweathermap.org/data/2.5/forecast/hourly", params)

    @staticmethod
    def extract_data(data):
        """
        Extracts the list of weather forecasts from the OpenWeather API response.

        Args:
            data(dict): the OpenWeather API response

        Returns:
            list: List of dictionaries each containing the weather forecast for a specific hour
        """

        return data["list"]

    @staticmethod
    def prep_data(data):
        """
        Prepares the weather forecast data for database insertion.

        The OpenWeather API response data is restructured to match the database schema, extracting the necessary fields
        and handling any missing data.

        Args:
            data(dict): dictionary containing the raw data for a specific hour of the forecast

        Returns:
            data(dict): dictionary containing the prepared data for a specific hour of the forecast
        """

        data['dt_iso'] = datetime.utcfromtimestamp(data['dt']).replace(tzinfo=tz.UTC)
        data['temp'] = data['main']['temp']
        data['feels_like'] = data['main']['feels_like']
        data['temp_min'] = data['main']['temp_min']
        data['temp_max'] = data['main']['temp_max']
        data['pressure'] = data['main']['pressure']
        data['humidity'] = data['main']['humidity']
        data['wind_speed'] = data['wind']['speed']
        data['wind_deg'] = data['wind']['deg']
        data['wind_gust'] = data['wind']['gust']
        data['wind_speed'] = data['wind']['speed']
        try:
            data['rain_1h'] = data['rain']['1h']
        except KeyError:
            data['rain_1h'] = 0
        try:
            data['snow_1h'] = data['snow']['1h']
        except KeyError:
            data['snow_1h'] = 0
        data['clouds_all'] = data['clouds']['all']
        data['weather_id'] = data['weather'][0]['id']
        data['weather_main'] = str.lower(data['weather'][0]['main'])
        data['weather_description'] = data['weather'][0]['description']
        data['weather_icon'] = data['weather'][0]['icon']
        return data


class WeatherDailyUpdate(ApiUpdate):
    def __init__(self):
        """
        Initialises the WeatherDailyUpdate instance.

        The schema name is set to "cityframe", the table name to "weather_fc",
        the URL to the OpenWeather forecast API endpoint, and the parameters to the required latitude, longitude,
        number of days, and API key.
        """

        params = {"lat": "40.78306", "lon": "-73.971249", "cnt": "16", "appid": openweather_key}
        super().__init__("cityframe", "weather_fc", "https://pro.openweathermap.org/data/2.5/forecast/daily", params)

    def extract_data(self, data):
        """
        Extracts and transforms the list of weather forecasts from the OpenWeather API response.

        This function expands the daily forecasts into hourly forecasts based on defined time slots.
        It only includes hourly forecasts for times later than the latest time in the existing database.
        The function also adds the minimum and maximum temperatures for each day to each hourly forecast.

        Args:
            data(dict): The OpenWeather API response, which includes a list of daily weather forecasts.

        Returns:
            list: A sorted list of dictionaries. Each dictionary contains the weather forecast for a specific hour,
            expanded from the daily forecast in the input data. The list is sorted in ascending order of forecast time.
        """

        with self.engine.connect() as connection:
            query = select(func.max(self.table.c.dt))
            result = connection.execute(query)
            last_dt = result.scalar()

        # define hourly slots
        time_slots = {
            "morn": range(6, 13),
            "day": range(13, 19),
            "eve": range(19, 24),
            "night": range(0, 6),
        }

        # initialise the list to store exploded data
        exploded_data = []

        # loop over each date
        for weather_info in data["list"]:
            dt = datetime.utcfromtimestamp(weather_info["dt"]).replace(tzinfo=tz.UTC)

            # loop over each hourly slot
            for time_period, hours in time_slots.items():
                for hour in hours:
                    hour_dt = datetime(dt.year, dt.month, dt.day, hour)

                    # skip data point if it is not after the last timestamp in the database
                    if int(hour_dt.timestamp()) <= last_dt:
                        continue

                    # create new data point
                    data_point = weather_info.copy()
                    data_point["dt"] = int(hour_dt.timestamp())

                    # Handle temperature and feels like data
                    for metric in ["temp", "feels_like"]:
                        period_data = data_point[metric].get(time_period)
                        if period_data:
                            data_point[metric] = period_data

                    # Handle min and max temp for the entire day
                    data_point["temp_min"] = weather_info["temp"]["min"]
                    data_point["temp_max"] = weather_info["temp"]["max"]

                    exploded_data.append(data_point)

        exploded_data = sorted(exploded_data, key=lambda d: d["dt"])

        return exploded_data

    @staticmethod
    def prep_data(data):
        """
        Prepares the weather forecast data for database insertion.

        The OpenWeather API response data is restructured to match the database schema, extracting the necessary fields
        and handling any missing data.

        Args:
            data(dict): dictionary containing the raw data for a specific hour of the forecast

        Returns:
            data(dict): dictionary containing the prepared data for a specific hour of the forecast
        """

        data['dt_iso'] = datetime.utcfromtimestamp(data['dt']).replace(tzinfo=tz.UTC)
        data['dt_txt'] = data['dt']
        data['feels_like'] = data['feels_like']
        data['visibility'] = 10000
        data['temp'] = data['temp']
        data['wind_speed'] = data['speed']
        data['wind_deg'] = data['deg']
        data['wind_gust'] = data['gust']
        try:
            data['rain_1h'] = data['rain']
        except KeyError:
            data['rain_1h'] = 0
        try:
            data['snow_1h'] = data['snow']
        except KeyError:
            data['snow_1h'] = 0
        data['clouds_all'] = data['clouds']
        data['weather_id'] = data['weather'][0]['id']
        data['weather_main'] = data['weather'][0]['main']
        data['weather_description'] = data['weather'][0]['description']
        data['weather_icon'] = data['weather'][0]['icon']
        return data
