import os
import django

# Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_app.settings_dev'
django.setup()

from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.utils.timezone import is_aware
from api_endpoints.models import TaxiZones, Busyness, WeatherFc, Results
from dateutil import tz
from datetime import datetime, timedelta
from pymcdm.weights import entropy_weights, equal_weights
from pymcdm.methods import MAIRCA
from pymcdm.helpers import rankdata
import numpy as np


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


def get_ny_dt(target_dt=datetime.now(tz=tz.gettz('America/New_York'))):
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

    # setting timezone to ny. if the supplied value/object is tz aware, convert it. if it is naive, assume it's ny time.
    if is_aware(ny_dt):
        return ny_dt.astimezone(tz.gettz('America/New_York'))
    else:
        return ny_dt.replace(tzinfo=tz.gettz('America/New_York'))


def get_results(style, tree_range=(1, 5), busyness_range=(1, 5), user_time=get_ny_dt()):
    """
    Fetches records associated with the given architectural style, tree range, busyness range, and user time.

    Args:
        style (str): Architectural style. It should match with the architectural style fields in the TaxiZones table.
        tree_range (tuple): A tuple of two integers indicating the lower and upper bounds of the tree range. Optional, defaults to (1, 5).
        busyness_range (tuple): A tuple of two integers indicating the lower and upper bounds of the busyness range. Optional, defaults to (1, 5).
        user_time (datetime): The desired time as a timezone-aware datetime object. Optional, defaults to the current time in New York timezone.

    Returns:
        dict: A dictionary containing information about each TaxiZone including zone details, busyness level, number of trees, architectural style count, and weather information.
    """

    weather = {'Clear': 1, 'Clouds': 2, 'Drizzle': 3, 'Fog': 4, 'Haze': 5, 'Mist': 6, 'Rain': 7, 'Smoke': 8, 'Snow': 9,
               'Squall': 10, 'Thunderstorm': 11}

    # Get TaxiZones IDs having at least one building in the desired style
    top_zones_ids = TaxiZones.objects.filter(**{style + '__gt': 0}).values_list('id', flat=True)
    results = {}

    print(f'filtered zones by style after {(datetime.utcnow() - start_time).total_seconds()} seconds')

    # define the timespan in which to look for results
    time_from = user_time - timedelta(hours=12)
    time_to = user_time + timedelta(hours=12)

    records = Busyness.objects.select_related('taxi_zone').filter(
        taxi_zone__in=top_zones_ids,
        dt_iso__dt_iso__range=(time_from, time_to))

    print(f'filtered busyness records after {(datetime.utcnow() - start_time).total_seconds()} seconds')

    for record in records:
        taxi_zone = record.taxi_zone
        # unique key using zone_id and timestamp - in case more than one time per zone is returned in the future
        key = f"{taxi_zone.id}_{record.dt_iso.dt_iso}"
        results[key] = {
            'id': str(taxi_zone.id),
            'zone': taxi_zone.zone,
            'dt_iso': record.dt_iso.dt_iso.astimezone(tz.gettz('America/New_York')).strftime('%Y-%m-%d %H:%M'),
            'dt_iso_tz': record.dt_iso.dt_iso.astimezone(tz.gettz('America/New_York')),
            'busyness': record.bucket,
            'trees': taxi_zone.trees_scaled,
            'style': getattr(taxi_zone, style),
            'weather': {'temp': record.dt_iso.temp, 'weather_description': record.dt_iso.weather_description,
                        'weather_icon': record.dt_iso.weather_icon}
        }

    return results


def generate_response(target_busyness, target_trees, target_style, target_dt, mcdm_method=MAIRCA,
                      mcdm_weights=entropy_weights):
    """
    Generates a dictionary containing top results based on the target busyness, style, and date-time.

    Args:
        target_busyness (int): The desired level of busyness.
        target_trees (int): The desired level of trees.
        target_style (str): The desired architectural style. It should match with one of the architectural styles in the taxi_zones table.
        target_dt (str or datetime): The desired date and time in "YYYY-MM-DD HH:MM" format or a datetime object.
        mcdm_method (callable): The multi-criteria decision-making method to be used. Optional, defaults to MAIRCA.
        mcdm_weights (callable): A function to calculate weights for the MCDM method. Optional, defaults to entropy_weights.

    Returns:
        dict: A dictionary containing the top 10 results.

    Raises:
        FieldDoesNotExist: If the target_style is not a valid architectural style.
    """

    global start_time
    start_time = datetime.utcnow()

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
    ny_dt = get_ny_dt(target_dt)

    # if the time supplied is earlier than the earliest available time, take that one
    # if the time supplied is later than the latest available time, take that one
    earliest_dt_iso = WeatherFc.objects.earliest('dt_iso').dt_iso
    latest_dt_iso = WeatherFc.objects.latest('dt_iso').dt_iso
    ny_dt = max(min(ny_dt, latest_dt_iso), earliest_dt_iso)

    print(f'requesting results after {(datetime.utcnow() - start_time).total_seconds()} seconds')

    results = get_results(style_dict.get(target_style), user_time=ny_dt)

    print(f'received results after {(datetime.utcnow() - start_time).total_seconds()} seconds')

    # check for errors
    if isinstance(results, Exception):
        return check_error_type(results)

    # prep alternatives with values for four criteria used in mcdm method in a numpy array:
    alts = np.array([[abs(target_busyness - value['busyness']),
                      abs(target_trees - value['trees']),
                      value['style'],
                      abs((ny_dt - value['dt_iso_tz']).total_seconds())] for value in
                     results.values()], dtype=int)

    print(f'prepared alts after {(datetime.utcnow() - start_time).total_seconds()} seconds')

    # define types of criteria (-1 for minimisation, 1 for maximisation)
    types = np.array([-1, -1, 1, -1])

    # set weights for criteria (default is entropy_weights)
    weights = mcdm_weights(alts)

    # initialise mcdm method (default is MAIRCA)
    method = mcdm_method()

    # determine preferences and ranking for alternatives
    pref = method(alts, weights, types)
    ranking = rankdata(pref)

    print(f'mcdm done after {(datetime.utcnow() - start_time).total_seconds()} seconds')

    # assign rankings to results
    for idx, key in enumerate(results.keys()):
        results[key]['rank'] = ranking[idx]

    # sort results by rank
    sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['rank'])}

    print(f'ranking done after {(datetime.utcnow() - start_time).total_seconds()} seconds')

    # Create a dictionary to track zone occurrences
    zone_occurrences = {}

    max_entries_per_zone = 1

    # Keep only top 10 with each zone appearing no more than twice
    top_results = {}
    for k, v in sorted_results.items():
        zone_name = v['zone']
        if zone_occurrences.get(zone_name, 0) < max_entries_per_zone:
            zone_occurrences[zone_name] = zone_occurrences.get(zone_name, 0) + 1
            top_results[k] = v
            if len(top_results) == 10:
                break

    # update the rank to be 1-10 for the top results (without repetitions / omissions)
    for idx, key in enumerate(top_results.keys()):
        top_results[key]['rank'] = idx + 1
        del top_results[key]['dt_iso_tz']

    print(f'top results ready after {(datetime.utcnow()-start_time).total_seconds()} seconds')

    return top_results


def current_busyness():
    ny_dt = get_ny_dt()

    # find records where dt_iso = ny_dt
    results = Results.objects.filter(dt_iso=ny_dt)

    # New dict to store the busyness for each taxi zone
    busyness_dict = {}

    for result in results:
        busyness_dict[result.taxi_zone] = result.bucket

    return busyness_dict


