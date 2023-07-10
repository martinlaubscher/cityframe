from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class WeatherAPITests(TestCase):
    def setUp(self):
        """This method sets up a client used to make HTTP requests to the endpoints
        """
        self.client = APIClient()

    def test_current_weather(self):
        """This is a unit test case for the api/current-weather/ endpoint. It retrieves the URL using the reverse()
        function based on the url pattern name. It tests that ndpoint returns the expected JSON response with the
        required keys and nested dictionary structures.
        """
        url = reverse('current_weather_data')
        response = self.client.get(url)

        # tests if status code is 200
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
        self.assertIn('timezone', response.data)
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
        self.assertIn('sunrise', response.data['sys'])
        self.assertIn('sunset', response.data['sys'])

    def tearDown(self):
        pass  # Nothing to teardown in this case
