from django.core.management.base import BaseCommand
from django.db import transaction
from random import randint
from api_endpoints.models import Busyness, WeatherFc, TaxiZones


class Command(BaseCommand):
    help = 'Populate Busyness table with all combinations of dt_iso from WeatherFc and id from TaxiZones'

    def handle(self, *args, **options):

        # clear table
        Busyness.objects.all().delete()

        weather_fc_dts = WeatherFc.objects.values_list('dt_iso', flat=True)
        taxi_zones_ids = TaxiZones.objects.values_list('id', flat=True)

        with transaction.atomic():
            for weather_fc_dt in weather_fc_dts:
                for taxi_zone_id in taxi_zones_ids:
                    busyness, created = Busyness.objects.get_or_create(
                        busy=randint(1, 5),
                        dt=WeatherFc.objects.get(dt_iso=weather_fc_dt),
                        location_id=TaxiZones.objects.get(id=taxi_zone_id),
                    )
