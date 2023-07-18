from django.db import models
import datetime
import pytz


class WeatherFc(models.Model):
    dt = models.BigIntegerField(primary_key=True)
    dt_iso = models.DateTimeField()
    temp = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    visibility = models.IntegerField()
    wind_speed = models.FloatField()
    wind_deg = models.IntegerField()
    wind_gust = models.FloatField()
    pop = models.FloatField
    rain_1h = models.FloatField(blank=True, null=True)
    snow_1h = models.FloatField(blank=True, null=True)
    clouds_all = models.IntegerField()
    weather_id = models.IntegerField()
    weather_main = models.CharField(max_length=255)
    weather_description = models.CharField(max_length=255)
    weather_icon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cityframe\".\"weather_fc'

    @classmethod
    def get_latest(cls):
        """Get all weather data from the database."""
        current_utc_timestamp = datetime.datetime.now(pytz.UTC)
        try:
            # retrieves record with closest match to current timestamp
            weather_data = cls.objects.filter(dt_iso__lte=current_utc_timestamp).latest('dt_iso')

            # formats the DB record as json, any hardcoded values are consistent across all records and not stored in DB
            weather_data_json = {
                "coord": {"lon": -73.9663, "lat": 40.7834},
                "weather": [
                    {
                        "id": weather_data.weather_id,
                        "main": weather_data.weather_main,
                        "description": weather_data.weather_description,
                        "icon": weather_data.weather_icon,
                    }
                ],
                "base": "stations",
                "main": {
                    "temp": weather_data.temp,
                    "feels_like": weather_data.feels_like,
                    "temp_min": weather_data.temp_min,
                    "temp_max": weather_data.temp_max,
                    "pressure": weather_data.pressure,
                    "humidity": weather_data.humidity,
                },
                "visibility": weather_data.visibility,
                "wind": {
                    "speed": weather_data.wind_speed,
                    "deg": weather_data.wind_deg,
                },
                "clouds": {
                    "all": weather_data.clouds_all,
                },
                "dt": weather_data.dt,
                "sys": {
                    "type": 1,
                    "id": 5141,
                    "country": "US",
                },
                "id": 5125771,
                "name": "Manhattan",  # replace with actual name if available
                "cod": 200,  # replace with actual cod if available
            }
            return weather_data_json
            # return cls.objects.latest('dt_iso')
        except cls.DoesNotExist:
            return None

    @classmethod
    def save_data(cls, data):
        """Saves weather data to the database.
        """
        weather_data = cls(**data)
        weather_data.save()
