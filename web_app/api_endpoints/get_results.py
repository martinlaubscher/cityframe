import os
import django

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_app.settings_dev'
django.setup()

from django.db.models import F
from django.core.exceptions import FieldDoesNotExist
from api_endpoints.models import TaxiZones, Busyness
import time
from dateutil import tz
from datetime import datetime


def get_architecture_data(style, busyness_range, user_time):
    # Validate input style field exists in TaxiZones model
    try:
        TaxiZones._meta.get_field(style)
    except FieldDoesNotExist:
        return "Invalid style input. No such field exists in TaxiZones model."

    # Get top 5 TaxiZones IDs according to input style
    top_zones_ids = TaxiZones.objects.filter(**{style + '__gt': 0}).order_by(F(style).desc()).values_list('id',
                                                                                                          flat=True)

    # creating a datetime object from the string received by the post request
    ny_time = datetime.strptime(user_time, "%Y-%m-%d %H:%M")

    # setting timezone to NY
    ny_time = ny_time.replace(tzinfo=tz.gettz('America/New_York'))

    # Get all Busyness records within the given busyness range and associated with the top zones
    records = Busyness.objects.filter(bucket__range=busyness_range, taxi_zone__in=top_zones_ids,
                                      dt_iso__dt_iso=ny_time)

    results = {}

    # Iterate over the records
    for record in records:
        # Get the associated TaxiZone
        taxi_zone = TaxiZones.objects.get(id=record.taxi_zone.id)

        # If this zone id is not in results yet, add a new dictionary with zone's details
        if record.taxi_zone.id not in results:
            results[record.taxi_zone.id] = {
                'zone': record.taxi_zone.zone,
                'dt_iso': record.dt_iso.dt_iso.astimezone(tz.gettz('America/New_York')).strftime('%Y-%m-%d %H:%M %z'),
                'busyness': record.bucket,
                'trees': taxi_zone.trees,
                style: getattr(taxi_zone, style),
                'weather': {
                    'temp': record.dt_iso.temp,
                    'weather_description': record.dt_iso.weather_description,
                    'weather_icon': record.dt_iso.weather_icon
                }
            }

    return results


start_time = time.time()  # Start timing

results = get_architecture_data('renaissance_revival', (1, 3), "2023-07-25 11:00")

end_time = time.time()  # End timing

execution_time = end_time - start_time  # Calculate the execution time

print(f"The function execution took: {execution_time} seconds")  # Print the execution time

print(results)

print(len(results))
