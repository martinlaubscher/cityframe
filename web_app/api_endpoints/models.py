from django.db import models


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
        db_table = 'cityframe\".\"weather_fc'

    @classmethod
    def get_latest(cls):
        """Get all weather data from the database."""
        try:
            return cls.objects.latest('dt_iso')
        except cls.DoesNotExist:
            return None

    @classmethod
    def save_data(cls, data):
        """Save weather data to the database."""
        weather_data = cls(**data)
        weather_data.save()
