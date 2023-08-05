from django.db import models
import datetime
import pytz
from django.utils import timezone


class WeatherFc(models.Model):
    dt = models.BigIntegerField(primary_key=True)
    dt_iso = models.DateTimeField(unique=True)
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
                "name": "Manhattan",
                "cod": 200,
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


class WeatherCurrent(models.Model):
    dt = models.BigIntegerField(primary_key=True)
    dt_iso = models.DateTimeField(default=timezone.now)
    temp = models.FloatField(default=0)
    feels_like = models.FloatField(default=0)
    temp_min = models.FloatField(default=0)
    temp_max = models.FloatField(default=0)
    pressure = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    visibility = models.IntegerField(default=0)
    wind_speed = models.FloatField(default=0)
    wind_deg = models.IntegerField(default=0)
    clouds_all = models.IntegerField(default=0)
    weather_id = models.IntegerField(default=0)
    weather_main = models.CharField(max_length=200)
    weather_description = models.CharField(max_length=200)
    weather_icon = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'cityframe\".\"weather_current'

    # this will likely be done outside of django, on a cronjob with a python script
    # def save(self, *args, **kwargs):
    #     # Delete all other objects in the table
    #     WeatherCurrent.objects.all().delete()
    #
    #     # Call the "real" save() method
    #     super(WeatherCurrent, self).save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        """Get current weather data from the database.
        """
        try:
            # retrieves record of current weather
            weather_data = cls.objects.get()

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
                "name": "Manhattan",
                "cod": 200,
            }
            return weather_data_json
        except cls.DoesNotExist:
            return None


class TaxiZones(models.Model):
    id = models.IntegerField(primary_key=True, db_column='location_id')
    zone = models.CharField(max_length=100)
    trees = models.IntegerField()
    trees_scaled = models.IntegerField()
    neo_georgian = models.IntegerField(db_column='neo-Georgian')
    greek_revival = models.IntegerField(db_column='Greek Revival')
    romanesque_revival = models.IntegerField(db_column='Romanesque Revival')
    neo_grec = models.IntegerField(db_column='neo-Grec')
    renaissance_revival = models.IntegerField(db_column='Renaissance Revival')
    beaux_arts = models.IntegerField(db_column='Beaux-Arts')
    queen_anne = models.IntegerField(db_column='Queen Anne')
    italianate = models.IntegerField(db_column='Italianate')
    federal = models.IntegerField(db_column='Federal')
    neo_renaissance = models.IntegerField(db_column='neo-Renaissance')

    class Meta:
        managed = False
        db_table = 'cityframe\".\"taxi_zones'


class Busyness(models.Model):
    id = models.IntegerField(primary_key=True)
    taxi_zone = models.ForeignKey(TaxiZones, on_delete=models.CASCADE, db_column='taxi_zone')
    prediction = models.FloatField()
    bucket = models.IntegerField()
    dt_iso = models.ForeignKey(WeatherFc, to_field='dt_iso', on_delete=models.CASCADE, db_column='dt_iso')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['taxi_zone', 'dt_iso'], name='unique_zone_dt')
        ]
        managed = False
        db_table = 'cityframe\".\"Results'


class Results(models.Model):
    id = models.BigAutoField(primary_key=True)
    taxi_zone = models.BigIntegerField()
    prediction = models.FloatField()
    bucket = models.IntegerField()
    dt_iso = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cityframe\".\"Results'


class Query(models.Model):
    busyness = models.IntegerField()
    trees = models.IntegerField()
    time = models.CharField(max_length=255)
    style = models.CharField(max_length=255)
    query_time = models.DateTimeField()

    class Meta:
        db_table = 'cityframe\".\"user_query'


class Response(models.Model):
    id = models.AutoField(primary_key=True)
    zone_id = models.IntegerField()
    zone = models.CharField(max_length=255)
    dt_iso = models.CharField(max_length=255)
    busyness = models.IntegerField()
    trees = models.IntegerField()
    style = models.IntegerField()
    weather = models.JSONField()
    rank = models.IntegerField()
    submission = models.ForeignKey(Query, related_name='responses', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cityframe\".\"user_query_response'


class Zoning(models.Model):
    location_id = models.OneToOneField(TaxiZones, on_delete=models.CASCADE, primary_key=True, db_column='location_id')
    commercial = models.FloatField()
    manufacturing = models.FloatField()
    park = models.FloatField()
    residential = models.FloatField()
    special = models.FloatField()
    zone_type = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'cityframe\".\"zoning'