from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class WeatherAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_current_weather(self):
        url = reverse('current_weather_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that the keys are present in the response
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

        # Check the 'coord' dictionary
        self.assertIn('lon', response.data['coord'])
        self.assertIn('lat', response.data['coord'])

        # Check the 'weather' list
        weather = response.data['weather'][0]
        self.assertIn('id', weather)
        self.assertIn('main', weather)
        self.assertIn('description', weather)
        self.assertIn('icon', weather)

        # Check the 'main' dictionary
        self.assertIn('temp', response.data['main'])
        self.assertIn('feels_like', response.data['main'])
        self.assertIn('temp_min', response.data['main'])
        self.assertIn('temp_max', response.data['main'])
        self.assertIn('pressure', response.data['main'])
        self.assertIn('humidity', response.data['main'])

        # Check the 'wind' dictionary
        self.assertIn('speed', response.data['wind'])
        self.assertIn('deg', response.data['wind'])

        # Check the 'clouds' dictionary
        self.assertIn('all', response.data['clouds'])

        # Check the 'sys' dictionary
        self.assertIn('type', response.data['sys'])
        self.assertIn('id', response.data['sys'])
        self.assertIn('country', response.data['sys'])
        self.assertIn('sunrise', response.data['sys'])
        self.assertIn('sunset', response.data['sys'])

    def tearDown(self):
        pass  # Nothing to teardown in this case
