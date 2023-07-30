import os
import django

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_app.settings_dev'
django.setup()

from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.utils.timezone import is_aware
from api_endpoints.models import TaxiZones, Busyness, WeatherFc, Results
from dateutil import tz
from datetime import datetime
from itertools import islice
from pymcdm.weights import entropy_weights
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

    # Get TaxiZones IDs having at least one building in the desired style and within the desired trees_scaled range
    top_zones_ids = TaxiZones.objects.filter(**{style + '__gt': 0}, trees_scaled__range=tree_range).values_list('id',
                                                                                                                flat=True)
    # Get all Busyness records within the given busyness range and associated with the top zones
    records = Busyness.objects.filter(bucket__range=busyness_range, taxi_zone__in=top_zones_ids,
                                      dt_iso__dt_iso=user_time)

    results = {}

    for record in records:
        taxi_zone = TaxiZones.objects.get(id=record.taxi_zone.id)
        # If this zone id is not in results yet, add a new dictionary with zone's details
        if record.taxi_zone.id not in results:
            results[record.taxi_zone.id] = {
                'zone': record.taxi_zone.zone,
                'dt_iso': record.dt_iso.dt_iso.astimezone(tz.gettz('America/New_York')).strftime('%Y-%m-%d %H:%M'),
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

    ny_dt = get_ny_dt(target_dt)

    # if the time supplied is earlier than the earliest available time, take that one
    # if the time supplied is later than the latest available time, take that one
    earliest_dt_iso = WeatherFc.objects.earliest('dt_iso').dt_iso
    latest_dt_iso = WeatherFc.objects.latest('dt_iso').dt_iso
    ny_dt = max(min(ny_dt, latest_dt_iso), earliest_dt_iso)

    results = get_results(style_dict.get(target_style), user_time=ny_dt)

    # check for errors
    if isinstance(results, Exception):
        return check_error_type(results)

    # prep alternatives with values for three criteria used in mcdm method in a numpy array:
    # difference to target busyness level, difference to target tree level, and building count
    alts = np.array([[abs(target_busyness - value['busyness']),
                      abs(target_trees - value['trees']),
                      value['style']] for value in results.values()], dtype=int)

    # define types of criteria (-1 for minimisation, 1 for maximisation)
    types = np.array([-1, -1, 1])

    # set weights for criteria (default is entropy_weights)
    weights = mcdm_weights(alts)

    # initialise mcdm method (default is MAIRCA)
    method = mcdm_method()

    # determine preferences and ranking for alternatives
    pref = method(alts, weights, types)
    ranking = rankdata(pref)

    # assign rankings to results
    for idx, key in enumerate(results.keys()):
        results[key]['rank'] = ranking[idx]

    # sort results by rank
    sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['rank'])}

    # keep only top 10
    top_results = dict(islice(sorted_results.items(), 10))

    # update the rank to be 1-10 for the top results (without repetitions / omissions)
    for idx, key in enumerate(top_results.keys()):
        top_results[key]['rank'] = idx + 1

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
