import os
import django

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_app.settings_dev'
django.setup()

from django.db.models import F
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.utils.timezone import is_aware
from api_endpoints.models import TaxiZones, Busyness, WeatherFc
import time
from dateutil import tz
from datetime import datetime, timedelta
from itertools import islice


def check_error_type(e):
    """
    Checks the type of the raised exception and returns a corresponding message.

    This function takes as input an exception object, checks if it is an instance of
    Django's ObjectDoesNotExist or FieldDoesNotExist exceptions, and returns a string
    message indicating the type of exception caught. If the exception is neither
    ObjectDoesNotExist nor FieldDoesNotExist, it returns a message indicating that an
    unknown exception has been caught.

    Args:
        e (Exception): The exception object to be checked.

    Returns:
        str: A string message indicating the type of the caught exception.

    """

    if isinstance(e, ObjectDoesNotExist):
        return f"Caught an ObjectDoesNotExist exception.\n{e}"
    elif isinstance(e, FieldDoesNotExist):
        return f"Caught a FieldDoesNotExist exception.\n{e}"
    else:
        return f"Caught an unknown exception.\n{e}"


def get_results(style, busyness_range, user_time):
    """
    Fetches records associated with the architectural style and busyness range at a specific time.

    Args:
        style (str): Architectural style. It should match with the architectural style fields in the taxi_zones table.
        busyness_range (tuple): A tuple of two integers indicating the lower and upper bounds of the busyness range.
        user_time (str | datetime): The desired time in "YYYY-MM-DD HH:MM" format or as a datetime object.

    Returns:
        dict: A dictionary containing information about each taxi zone including zone details, busyness level,
        number of trees, architectural style count, and weather information.
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

    # Get top 5 TaxiZones IDs according to input style
    top_zones_ids = TaxiZones.objects.filter(**{style + '__gt': 0}).order_by(F(style).desc()).values_list('id',
                                                                                                          flat=True)

    # Get all Busyness records within the given busyness range and associated with the top zones
    records = Busyness.objects.filter(bucket__range=busyness_range, taxi_zone__in=top_zones_ids,
                                      dt_iso__dt_iso=user_time)

    results = {}

    # Iterate over the records
    for record in records:
        # Get the associated TaxiZone
        taxi_zone = TaxiZones.objects.get(id=record.taxi_zone.id)

        # If this zone id is not in results yet, add a new dictionary with zone's details
        try:
            if record.taxi_zone.id not in results:
                results[record.taxi_zone.id] = {
                    'zone': record.taxi_zone.zone,
                    'dt_iso': record.dt_iso.dt_iso.astimezone(tz.gettz('America/New_York')).strftime(
                        '%Y-%m-%d %H:%M %z'),
                    'busyness': record.bucket,
                    'trees': taxi_zone.trees_scaled,
                    style_dict_reverse.get(style): getattr(taxi_zone, style),
                    'weather': {
                        'temp': record.dt_iso.temp,
                        'weather_description': record.dt_iso.weather_description,
                        'weather_icon': record.dt_iso.weather_icon
                    }
                }
        except ObjectDoesNotExist as e:
            return e

    return results


def generate_response(target_busyness, target_style, target_dt):
    """
    Generates a dictionary containing top 10 results based on the target busyness, style, and date-time.

    Args:
        target_busyness (int): The desired level of busyness.
        target_style (str): The desired architectural style. It should match with one of the architectural styles in the taxi_zones table.
        target_dt (str | datetime): The desired date and time in "YYYY-MM-DD HH:MM" format or a datetime object.

    Returns:
        dict: A dictionary containing the top 10 results sorted according to the difference from the target busyness
        level and the count of the target style. The dictionary includes details of each zone such as the zone name,
        level and thdeltae count of the target style. The dictionary includes details of each zone such as the zone name,
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

    # checking if style is valid
    if style_dict.get(target_style) is None:
        raise FieldDoesNotExist(f"The style '{target_style}' is invalid. It should be one of these: {tuple(style_dict.keys())}")

    # creating a datetime object from the string received by the post request.
    # if the input is neither a correctly formatted string nor a datetime object, raise an error
    if isinstance(target_dt, str):
        ny_dt = datetime.strptime(target_dt, "%Y-%m-%d %H:%M").replace(minute=0)
    elif isinstance(target_dt, datetime):
        ny_dt = target_dt.replace(minute=0, second=0, microsecond=0)
    else:
        raise ValueError("Invalid date input. Expected a string or datetime object.")

    # setting timezone to ny. if the supplied value/object is tz aware, convert it. if it is naive, assume it's ny time.
    if is_aware(ny_dt):
        ny_dt = ny_dt.astimezone(tz.gettz('America/New_York'))
    else:
        ny_dt = ny_dt.replace(tzinfo=tz.gettz('America/New_York'))

    # if the time supplied is earlier than the earliest available time, take that one
    # if the time supplied is later than the latest available time, take that one
    earliest_dt_iso = WeatherFc.objects.earliest('dt_iso').dt_iso
    latest_dt_iso = WeatherFc.objects.latest('dt_iso').dt_iso
    ny_dt = max(min(ny_dt, latest_dt_iso), earliest_dt_iso)

    # expand the busyness range until there are ten results
    while len(results) < 10:
        results = get_results(style_dict.get(target_style), (lower, higher), ny_dt)
        # check for errors
        if isinstance(results, Exception):
            return check_error_type(results)
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

response = generate_response(3, 'Renaissance Revival', "2023-07-28 12:00")

end_time = time.time()  # End timing
execution_time = end_time - start_time  # Calculate the execution time
print(f"The function execution took: {execution_time} seconds\n")  # Print the execution time

print(response)
