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
from itertools import islice


def get_results(style, busyness_range, user_time):
    """
    Fetches records associated with the architectural style and busyness range at a specific time.

    Args:
        style (str): Architectural style. It should match with the architectural style fields in the taxi_zones table.
        busyness_range (tuple): A tuple of two integers indicating the lower and upper bounds of the busyness range.
        user_time (str): The desired time in "YYYY-MM-DD HH:MM" format.

    Returns:
        dict: A dictionary containing information about each taxi zone including zone details, busyness level, number of trees, architectural style count, and weather information.

    Raises:
        FieldDoesNotExist: If the input style field does not exist in the TaxiZones model.
    """
    style_dict_reverse = {
        'neo_georgian': 'neo-Georgian',
        'greek_revival': 'Greek Revival',
        'romanesque_revival': 'Romanesque Revival',
        'neo_grec': 'neo-Grec',
        'renaissance_revival': 'Renaissance Revival',
        'beaux_arts': 'Beaux-Arts',
        'queen_anne': 'Queen Anne',
        'italianate': 'Italianate',
        'federal': 'Federal',
        'neo_renaissance': 'neo-Renaissance'
    }

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
                style_dict_reverse.get(style): getattr(taxi_zone, style),
                'weather': {
                    'temp': record.dt_iso.temp,
                    'weather_description': record.dt_iso.weather_description,
                    'weather_icon': record.dt_iso.weather_icon
                }
            }

    return results


def generate_response(target_busyness, target_style, target_dt):
    """
    Generates a dictionary containing top 10 results based on the target busyness, style, and date-time.

    Args:
        target_busyness (int): The desired level of busyness.
        target_style (str): The desired architectural style. It should match with one of the architectural styles in the taxi_zones table.
        target_dt (str): The desired date and time in "YYYY-MM-DD HH:MM" format.

    Returns:
        dict: A dictionary containing the top 10 results sorted according to the difference from the target busyness
        level and the count of the target style. The dictionary includes details of each zone such as the zone name,
        date and time, busyness level, number of trees, count of the target architectural style, and weather information.
    """

    results = {}

    # dictionary to translate the style names to django model variables
    style_dict = {
        'neo-Georgian': 'neo_georgian',
        'Greek Revival': 'greek_revival',
        'Romanesque Revival': 'romanesque_revival',
        'neo-Grec': 'neo_grec',
        'Renaissance Revival': 'renaissance_revival',
        'Beaux-Arts': 'beaux_arts',
        'Queen Anne': 'queen_anne',
        'Italianate': 'italianate',
        'Federal': 'federal',
        'neo-Renaissance': 'neo_renaissance'
    }

    lower = higher = target_busyness

    while len(results) < 10:
        results = get_results(style_dict.get(target_style), (lower, higher), target_dt)
        lower -= 1
        higher += 1

    # calculate the difference to the desired busyness level
    for key, value in results.items():
        value['busyness_diff'] = abs(target_busyness - value['busyness'])

    # sort the dictionary first according to the difference to the desired busyness level, then to the count
    sorted_dict = dict(
        sorted(results.items(), key=lambda item: (item[1]['busyness_diff'], -item[1][target_style])))

    # Remove the temporary 'busyness_diff' from the dictionaries
    for value in sorted_dict.values():
        del value['busyness_diff']

    sliced_dict = dict(islice(sorted_dict.items(), 10))

    return sliced_dict


start_time = time.time()  # Start timing

response = generate_response(3, 'Renaissance Revival', '2023-07-25 11:00')

end_time = time.time()  # End timing
execution_time = end_time - start_time  # Calculate the execution time
print(f"The function execution took: {execution_time} seconds\n")  # Print the execution time

print(response)
