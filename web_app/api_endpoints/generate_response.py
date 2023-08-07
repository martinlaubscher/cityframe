import os
import django

# Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_app.settings_dev'
django.setup()

from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.utils.timezone import is_aware
from api_endpoints.models import TaxiZones, Busyness, WeatherFc
from dateutil import tz
from datetime import datetime, timedelta
from pymcdm.weights import critic_weights
from pymcdm.methods import MAIRCA
from pymcdm.helpers import rankdata
import numpy as np
from api_endpoints.get_results import django_get_results, psycopg_get_results


def check_error_type(e):
    """
    Checks the type of the raised exception and returns a corresponding message.

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


def check_ny_dt(target_dt):
    """
    Converts the given target date and time to a New York timezone-aware datetime object.

    Args:
        target_dt (str or datetime): The desired date and time in "YYYY-MM-DD HH:MM" format or a datetime object.
            Optional, defaults to the current time in the New York timezone.

    Returns:
        datetime: A datetime object representing the time in the New York timezone.

    Raises:
        ValueError: If the input is neither a correctly formatted string nor a datetime object.
    """

    # creating a datetime object from the string received by the post request.
    # if the input is neither a correctly formatted string nor a datetime object, raise an error
    if isinstance(target_dt, str):
        ny_dt = datetime.strptime(target_dt, "%Y-%m-%d %H:%M").replace(minute=0)
    elif isinstance(target_dt, datetime):
        ny_dt = target_dt.replace(minute=0, second=0, microsecond=0)
    else:
        raise ValueError("Invalid date input. Expected a string or datetime object.")

    # print(f'check_ny_dt time: {ny_dt}')

    # setting timezone to ny. if the supplied value/object is tz aware, convert it. if it is naive, assume it's ny time.
    if is_aware(ny_dt):
        return ny_dt.astimezone(tz=tz.gettz('America/New_York'))
    else:
        return ny_dt.replace(tzinfo=tz.gettz('America/New_York'))


def generate_response(target_busyness, target_trees, target_style, target_type, target_dt, weather=None,
                      mcdm_method=MAIRCA,
                      mcdm_weights=critic_weights):
    """
    Generates a dictionary containing top results based on the target busyness, style, date-time, and weather.

    Args:
        target_busyness (int): The desired level of busyness.
        target_trees (int): The desired level of trees.
        target_style (str): The desired architectural style. It should match with one of the architectural styles in the taxi_zones table.
        target_dt (str or datetime): The desired date and time in "YYYY-MM-DD HH:MM" format or a datetime object.
        weather (str): The desired weather (main category). Optional, defaults to None.
        mcdm_method (callable): The multi-criteria decision-making method to be used. Optional, defaults to MAIRCA.
        mcdm_weights (callable): A function to calculate weights for the MCDM method. Optional, defaults to entropy_weights.

    Returns:
        dict: A dictionary containing the top 10 results.

    Raises:
        FieldDoesNotExist: If the target_style is not a valid architectural style.
    """

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

    # checking if style is valid
    if style_dict.get(target_style) is None:
        raise FieldDoesNotExist(
            f"The style '{target_style}' is invalid. It should be one of these: {tuple(style_dict.keys())}")

    # validate supplied time
    ny_dt = check_ny_dt(target_dt)

    # if the time supplied is earlier than the earliest available time, take that one
    # if the time supplied is later than the latest available time, take that one
    earliest_dt_iso = WeatherFc.objects.earliest('dt_iso').dt_iso
    latest_dt_iso = WeatherFc.objects.latest('dt_iso').dt_iso
    ny_dt = max(min(ny_dt, latest_dt_iso), earliest_dt_iso)

    # results = django_get_results(style_dict.get(target_style), weather, target_type, ny_dt)
    records = psycopg_get_results(target_style, weather, target_type, ny_dt)

    # if there are no records matching the query, return an empty dictionary
    if len(records) == 0:
        return records

    # check for errors
    if isinstance(records, Exception):
        return check_error_type(records)

    # Create empty array of the right shape
    alts = np.empty((len(records), 5), dtype=int)

    # Fill the array
    for i, record in enumerate(records):
        alts[i, 0] = abs(target_busyness - record['bucket'])
        alts[i, 1] = abs(target_trees - record['trees_scaled'])
        alts[i, 2] = record['building_count']
        alts[i, 3] = record['zone_percent']
        alts[i, 4] = abs((ny_dt - record['dt_iso']).total_seconds())

    # define types of criteria (-1 for minimisation, 1 for maximisation)
    types = np.array([-1, -1, 1, 1, -1])

    # set weights for criteria (default is entropy_weights)
    weights = mcdm_weights(alts)

    # initialise mcdm method (default is MAIRCA)
    method = mcdm_method()

    # determine preferences and ranking for alternatives
    pref = method(alts, weights, types)
    ranking = rankdata(pref)

    ranked_records = sorted((dict(rank=ranking[i], **record) for i, record in enumerate(records)),
                            key=lambda r: r['rank'])

    # Create a dictionary to track zone occurrences
    zone_occurrences = {}

    max_entries_per_zone = 1

    # Keep only top 10 with each zone appearing no more than twice
    results = {}
    ny_tz = tz.gettz('America/New_York')
    rank = 1

    for record in ranked_records:
        if zone_occurrences.get(record['zone'], 0) < max_entries_per_zone:
            zone_occurrences[record['zone']] = zone_occurrences.get(record['zone'], 0) + 1
            key = f"{record['taxi_zone']}_{record['dt_iso']}"
            ny_dt_iso = record['dt_iso'].astimezone(ny_tz)
            results[key] = {
                'id': str(record['taxi_zone']),
                'zone': record['zone'],
                'dt_iso': ny_dt_iso.strftime('%Y-%m-%d %H:%M'),
                'busyness': record['bucket'],
                'trees': record['trees_scaled'],
                'style': record['building_count'],
                'zone_type': f'{round(record["zone_percent"])}% {target_type}',
                'rank': rank,
                'weather': {
                    'temp': record['temp'],
                    'weather_description': record['weather_main'],
                    'weather_icon': record['weather_icon']
                }
            }
            rank += 1
        if rank > 10:
            break
    return results


def current_busyness():
    ny_dt = datetime.now(tz=tz.gettz('America/New_York')).replace(minute=0, second=0, microsecond=0)

    # print(f'current time: {ny_dt}')

    # find records where dt_iso = ny_dt
    results = Busyness.objects.filter(dt_iso_id=ny_dt).values('taxi_zone_id', 'bucket')

    # if no results have been found, try the next hour
    # necessary if request is made just after predictions have been updated
    if len(results) == 0:
        results = Busyness.objects.filter(dt_iso_id=ny_dt + timedelta(hours=1)).values('taxi_zone_id', 'bucket')

    # print(f'results: {results}')

    # New dict to store the busyness for each taxi zone
    busyness_dict = {}

    for result in results:
        busyness_dict[result['taxi_zone_id']] = result['bucket']

    # print(f'busyness dict: {busyness_dict}')

    return busyness_dict


import timeit

# Define the number of repetitions
num_runs = 1000

# Use timeit to time the function using a lambda
total_time = timeit.timeit(lambda: generate_response(3,3,'Federal', 'park', '2023-08-10 15:00', 'Clear'), number=num_runs)

# Calculate the average time
average_time = total_time / num_runs

print(f"Average execution time over {num_runs} runs: {average_time:.5f} seconds")
