import re
from django.test import TestCase
from django.db import connections
from django.urls import reverse
from rest_framework.test import APIClient


class EndpointTests(TestCase):
    def setUp(self):
        """This method sets up the cityframe schema and weather_fc table on the test database in the same manner as the
        cityframe database. This method also sets up a client used to make HTTP requests to API endpoints
        """
        super().setUp()

        # Get a cursor for your test database
        cursor = connections['default'].cursor()

        # Execute your SQL script to create the necessary tables
        # Replace 'your_sql_script.sql' with the path to your actual SQL script
        with open('api_endpoints/your_sql_script.sql') as f:
            cursor.execute(f.read())

        self.client = APIClient()

    def test_current_suntimes(self):
        """This is a unit test case for the api/current-suntimes/ endpoint. It retrieves the URL using the reverse()
        function based on the url pattern name (see urls.py). It tests that endpoint returns the expected JSON response
        with the required keys, and that returned data matches a regex format
        """
        url = reverse('current_suntimes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that the 'sunrise' and 'sunset' keys are present in the response
        self.assertIn('sunrise', response.data)
        self.assertIn('sunset', response.data)

        # Check if the 'sunrise' and 'sunset' are in the correct format using regex
        timestamp_pattern = re.compile(r'^\d{10}$')  # Matches a string of 10 digits
        self.assertTrue(timestamp_pattern.match(str(response.data['sunrise'])))
        self.assertTrue(timestamp_pattern.match(str(response.data['sunset'])))

    def test_current_suntimes_str(self):
        """This is a unit test case for the 'api/current-suntimes/<str:formatting>' endpoint. It retrieves the URL
        using the reverse() function based on the url pattern name (see urls.py), and uses the optional 'datetime'
        formatting. Tests that endpoint returns the expected JSON data with the required key, and that returned data
        matches a regex format
        """
        url = reverse('current_suntimes_str', kwargs={'formatting': 'datetime'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that the 'sunrise' and 'sunset' keys are present in the response
        self.assertIn('sunrise', response.data)
        self.assertIn('sunset', response.data)

        # Check if the 'sunrise' and 'sunset' are in the correct format using regex
        datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')  # Matches 'YYYY-MM-DD HH:MM:SS'
        self.assertTrue(datetime_pattern.match(response.data['sunrise']))
        self.assertTrue(datetime_pattern.match(response.data['sunset']))

    def test_current_weather(self):
        """This is a unit test case for the api/current-weather/ endpoint. It retrieves the URL using the reverse()
        function based on the url pattern name (see urls.py). It tests that endpoint returns the expected JSON response
        with the required keys and nested dictionary structures.
        """
        url = reverse('current_weather_data')
        response = self.client.get(url)

        # tests if status code is 200, successful response
        self.assertEqual(response.status_code, 200)

        # Check that relevant keys are present in the response data
        self.assertIn('coord', response.data)
        self.assertIn('weather', response.data)
        self.assertIn('main', response.data)
        self.assertIn('visibility', response.data)
        self.assertIn('wind', response.data)
        self.assertIn('clouds', response.data)
        self.assertIn('dt', response.data)
        self.assertIn('sys', response.data)
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('cod', response.data)

        # Check that relevant keys are present in nested 'coord' dict
        self.assertIn('lon', response.data['coord'])
        self.assertIn('lat', response.data['coord'])

        # Check the relevant keys are present in nested 'weather' dict
        weather = response.data['weather'][0]
        self.assertIn('id', weather)
        self.assertIn('main', weather)
        self.assertIn('description', weather)
        self.assertIn('icon', weather)

        # Check the relevant keys are present in nested 'main' dict
        self.assertIn('temp', response.data['main'])
        self.assertIn('feels_like', response.data['main'])
        self.assertIn('temp_min', response.data['main'])
        self.assertIn('temp_max', response.data['main'])
        self.assertIn('pressure', response.data['main'])
        self.assertIn('humidity', response.data['main'])

        # Check the relevant keys are present in nested 'wind' dict
        self.assertIn('speed', response.data['wind'])
        self.assertIn('deg', response.data['wind'])

        # Check the relevant keys are present in nested 'clouds' dict
        self.assertIn('all', response.data['clouds'])

        # Check the relevant keys are present in nested 'sys' dict
        self.assertIn('type', response.data['sys'])
        self.assertIn('id', response.data['sys'])
        self.assertIn('country', response.data['sys'])

    def test_future_weather(self):
        """This is a unit test case for the api/future-weather/<str:timestamp>/ endpoint. It retrieves the URL using the
        reverse() function based on the url pattern name (see urls.py). Tests that endpoint returns the expected JSON
        data with the required keys and nested dictionary structures.
        """
        # sample timestamp, can be replaced with appropriate value if required
        timestamp = '1688810400'
        url = reverse('future_weather_data', kwargs={'timestamp': timestamp})
        response = self.client.get(url)

        # tests if status code is 200, successful response
        self.assertEqual(response.status_code, 200)

        # Check that relevant keys are present in the response data
        self.assertIn('dt', response.data)
        self.assertIn('main', response.data)
        self.assertIn('visibility', response.data)
        self.assertIn('weather', response.data)
        self.assertIn('clouds', response.data)
        self.assertIn('wind', response.data)
        self.assertIn('pop', response.data)
        self.assertIn('sys', response.data)
        self.assertIn('dt_txt', response.data)

        # Check the relevant keys are present in 'main' dict
        main = response.data['main']
        self.assertIn('temp', main)
        self.assertIn('feels_like', main)
        self.assertIn('temp_min', main)
        self.assertIn('temp_max', main)
        self.assertIn('pressure', main)
        self.assertIn('sea_level', main)
        self.assertIn('grnd_level', main)
        self.assertIn('humidity', main)
        self.assertIn('temp_kf', main)

        # Check the relevant keys are present in 'weather' dict
        weather = response.data['weather'][0]
        self.assertIn('id', weather)
        self.assertIn('main', weather)
        self.assertIn('description', weather)
        self.assertIn('icon', weather)

        # Check the relevant keys are present in 'clouds' dict
        self.assertIn('all', response.data['clouds'])

        # Check the relevant keys are present in 'wind' dict
        wind = response.data['wind']
        self.assertIn('speed', wind)
        self.assertIn('deg', wind)
        self.assertIn('gust', wind)

        # Check the relevant keys are present in 'sys' dict
        self.assertIn('pod', response.data['sys'])

    def test_current_time(self):
        """This is a unit test case for the 'api/current-time/' endpoint. It retrieves the URL using the
        reverse() function based on the url pattern name (see urls.py). Tests that endpoint returns the expected JSON
        data with the required keys, and that returned data is in expected format.
        """
        url = reverse('current_manhattan_time')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check 'timestamp' key in response
        self.assertIn('timestamp', response.data)

        # use regex to test if timestamp matches expected pattern (10 digits)
        timestamp_pattern = re.compile(r'^\d{10}$')
        self.assertTrue(timestamp_pattern.match(str(response.data['timestamp'])))

    def test_current_time_str(self):
        """This is a unit test case for the 'api/current-time/<str:formatting>' endpoint. It retrieves the URL using the
        reverse() function based on the url pattern name (see urls.py), and uses the optional 'datetime' formatting.
        Tests that endpoint returns the expected JSON data with the required key, and that returned data is in expected
        format.
        """
        url = reverse('current_manhattan_time_str', kwargs={'formatting': 'datetime'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check 'datetime' key in response
        self.assertIn('datetime', response.data)

        # use regex to test if timestamp string matches expected pattern ('YYYY-MM-DD HH:MM:SS')
        datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
        self.assertTrue(datetime_pattern.match(response.data['datetime']))

    def test_future_suntimes(self):
        """This is a unit test case for the api/future-suntimes/{days_in_future}/ endpoint. It retrieves the URL using
        the reverse() function based on the url pattern name (see urls.py). It tests that endpoint returns the expected
        JSON response with the required keys, and that returned data matches a regex format.
        """
        # ints from 1-5 (inclusive) are valid for {days_in_future}, 2 chosen arbitrarily
        days_in_future = 2
        url = reverse('future_suntimes', kwargs={'days_in_future': days_in_future})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check 'sunrise' and 'sunset' keys in response
        self.assertIn('sunrise', response.data)
        self.assertIn('sunset', response.data)

        # Check 'sunrise' and 'sunset' match expected regex pattern (10 digits)
        timestamp_pattern = re.compile(r'^\d{10}$')
        self.assertTrue(timestamp_pattern.match(str(response.data['sunrise'])))
        self.assertTrue(timestamp_pattern.match(str(response.data['sunset'])))

    def test_future_suntimes_str(self):
        """This is a unit test case for the api/future-suntimes/{days_in_future}/{formatting}/ endpoint. It retrieves
        the URL using the reverse() function based on the url pattern name (see urls.py), and uses the optional
        'datetime' formatting. Tests that endpoint returns the expected JSON data with the required keys, and that
        returned data is in expected format.
        """
        # ints from 1-5 (inclusive) are valid for {days_in_future}, 2 chosen arbitrarily
        days_in_future = 2
        url = reverse('future_suntimes_str', kwargs={'days_in_future': days_in_future, 'formatting': 'datetime'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check 'sunrise' and 'sunset' keys in response
        self.assertIn('sunrise', response.data)
        self.assertIn('sunset', response.data)

        # Check 'sunrise' and 'sunset' match expected regex pattern ('YYYY-MM-DD HH:MM:SS')
        datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
        self.assertTrue(datetime_pattern.match(response.data['sunrise']))
        self.assertTrue(datetime_pattern.match(response.data['sunset']))

    def tearDown(self):
        # Nothing to teardown, may be required for future tests
        pass
