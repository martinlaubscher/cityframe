import os
import sys
from datetime import timedelta

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(current_path))

sys.path.append(cityframe_path)

from psycopg.rows import dict_row
from django.apps import apps
from api_endpoints.models import TaxiZones, Busyness, WeatherFc
from dateutil import tz
from datetime import datetime, timedelta

pool = apps.get_app_config('api_endpoints').pool


def psycopg_get_results(style, weather, zone_type, user_time, tree_range=(1, 5), busyness_range=(1, 5)):
    """
    Fetches records associated with the given architectural style, weather, tree range, busyness range, and user time. Uses psycopg.

    Args:
        style (str): Architectural style. It should match with the architectural style fields in the TaxiZones table.
        weather (str or None): The desired weather (main category). If not None, it should match one of the present values in the WeatherFc table.
        zone_type (str): The desired zone type. should match with one of the types in the zoning table.
        tree_range (tuple): A tuple of two integers indicating the lower and upper bounds of the tree range. Optional, defaults to (1, 5).
        busyness_range (tuple): A tuple of two integers indicating the lower and upper bounds of the busyness range. Optional, defaults to (1, 5).
        user_time (datetime): The desired time as a timezone-aware datetime object. Optional, defaults to the current time in New York timezone.

    Returns:
        list: A list of dictionaries (one dictonary per record) of the records matching the query.
    """

    zone_type_filter = ''
    if str.lower(zone_type) != 'all':
        zone_type_filter = f'AND "cityframe"."zone_types"."zone_type" = \'{zone_type}\''

    arch_style_filter = ''
    if str.lower(style) != 'all':
        arch_style_filter = f'AND "cityframe"."arch_styles"."style" = \'{style}\' AND "cityframe"."arch_styles"."building_count" > 0'

    if weather is None:
        time_from = user_time - timedelta(hours=12)
        time_to = user_time + timedelta(hours=12)

        sql = f'''
                SELECT "cityframe"."Results"."taxi_zone", "cityframe"."taxi_zones"."zone", "cityframe"."Results"."dt_iso", "cityframe"."Results"."bucket", "cityframe"."taxi_zones"."trees_scaled", "cityframe"."arch_styles"."building_count", "cityframe"."arch_styles"."main_style", "cityframe"."arch_styles"."main_count", "cityframe"."zone_types"."zone_percent", "cityframe"."zone_types"."main_type", "cityframe"."weather_fc"."temp", "cityframe"."weather_fc"."weather_main", "cityframe"."weather_fc"."weather_icon"
                FROM "cityframe"."Results"
                INNER JOIN "cityframe"."weather_fc" ON ("cityframe"."Results"."dt_iso" = "cityframe"."weather_fc"."dt_iso")
                INNER JOIN "cityframe"."taxi_zones" ON ("cityframe"."Results"."taxi_zone" = "cityframe"."taxi_zones"."location_id")
                LEFT OUTER JOIN "cityframe"."zone_types" ON ("cityframe"."taxi_zones"."location_id" = "cityframe"."zone_types"."location_id")
                LEFT OUTER JOIN "cityframe"."arch_styles" ON ("cityframe"."taxi_zones"."location_id" = "cityframe"."arch_styles"."location_id")
                WHERE ("cityframe"."Results"."dt_iso" BETWEEN '{time_from}'::timestamptz AND '{time_to}'::timestamptz {arch_style_filter} {zone_type_filter});'''
    else:
        sql = f'''
                SELECT "cityframe"."Results"."taxi_zone", "cityframe"."taxi_zones"."zone", "cityframe"."Results"."dt_iso", "cityframe"."Results"."bucket", "cityframe"."taxi_zones"."trees_scaled", "cityframe"."arch_styles"."building_count", "cityframe"."arch_styles"."main_style", "cityframe"."arch_styles"."main_count", "cityframe"."zone_types"."zone_percent", "cityframe"."zone_types"."main_type", "cityframe"."weather_fc"."temp", "cityframe"."weather_fc"."weather_main", "cityframe"."weather_fc"."weather_icon"
                FROM "cityframe"."Results"
                INNER JOIN "cityframe"."weather_fc" ON ("cityframe"."Results"."dt_iso" = "cityframe"."weather_fc"."dt_iso")
                INNER JOIN "cityframe"."taxi_zones" ON ("cityframe"."Results"."taxi_zone" = "cityframe"."taxi_zones"."location_id")
                LEFT OUTER JOIN "cityframe"."zone_types" ON ("cityframe"."taxi_zones"."location_id" = "cityframe"."zone_types"."location_id")
                LEFT OUTER JOIN "cityframe"."arch_styles" ON ("cityframe"."taxi_zones"."location_id" = "cityframe"."arch_styles"."location_id")
                WHERE ("cityframe"."weather_fc"."weather_main" = '{weather}' {arch_style_filter} {zone_type_filter});'''

    # Create a new transaction
    with pool.connection() as conn:

        # Create a new cursor to execute the SQL statement
        with conn.cursor(row_factory=dict_row) as cur:
            # Execute SQL statement
            cur.execute(sql)

            # Fetch the results as dictionaries
            records = cur.fetchall()

    return records


def django_get_results(style, weather, zone_type, user_time, tree_range=(1, 5), busyness_range=(1, 5)):
    """
    Fetches records associated with the given architectural style, weather, tree range, busyness range, and user time. Uses Django's ORM.

    Args:
        style (str): Architectural style. It should match with the architectural style fields in the TaxiZones table.
        weather (str or None): The desired weather (main category). If not None, it should match one of the present values in the WeatherFc table.
        zone_type (str): The desired zone type. should match with one of the types in the zoning table.
        tree_range (tuple): A tuple of two integers indicating the lower and upper bounds of the tree range. Optional, defaults to (1, 5).
        busyness_range (tuple): A tuple of two integers indicating the lower and upper bounds of the busyness range. Optional, defaults to (1, 5).
        user_time (datetime): The desired time as a timezone-aware datetime object. Optional, defaults to the current time in New York timezone.

    Returns:
        dict: A dictionary containing information about each TaxiZone including zone details, busyness level, number of trees, architectural style count, and weather information.
    """

    # Get TaxiZones IDs having at least one building in the desired style
    top_zones_ids = TaxiZones.objects.filter(**{style + '__gt': 0}).values_list('id', flat=True)

    if weather is None:
        # define the timespan in which to look for results
        time_from = user_time - timedelta(hours=12)
        time_to = user_time + timedelta(hours=12)
        records = Busyness.objects.select_related('taxi_zone').filter(
            taxi_zone__in=top_zones_ids,
            dt_iso__dt_iso__range=(time_from, time_to)).values('id', 'taxi_zone_id', 'taxi_zone__zone', 'dt_iso_id',
                                                               'bucket', 'taxi_zone__trees_scaled',
                                                               f'taxi_zone__{style}',
                                                               f'taxi_zone__zoning__{zone_type}',
                                                               'dt_iso__temp', 'dt_iso__weather_main',
                                                               'dt_iso__weather_icon')
    else:
        records = Busyness.objects.select_related('taxi_zone').filter(
            taxi_zone__in=top_zones_ids,
            dt_iso__weather_main=weather).values('id', 'taxi_zone_id', 'taxi_zone__zone', 'dt_iso_id',
                                                 'bucket', 'taxi_zone__trees_scaled',
                                                 f'taxi_zone__{style}',
                                                 f'taxi_zone__zoning__{zone_type}',
                                                 'dt_iso__temp', 'dt_iso__weather_main',
                                                 'dt_iso__weather_icon')

    records = tuple(records)

    results = {}
    ny_tz = tz.gettz('America/New_York')
    for record in records:
        key = f"{record['taxi_zone_id']}_{record['dt_iso_id']}"
        ny_dt_iso = record['dt_iso_id'].astimezone(ny_tz)
        results[key] = {
            'id': str(record['taxi_zone_id']),
            'zone': record['taxi_zone__zone'],
            'dt_iso': ny_dt_iso.strftime('%Y-%m-%d %H:%M'),
            'dt_iso_tz': ny_dt_iso,
            'busyness': record['bucket'],
            'trees': record['taxi_zone__trees_scaled'],
            'style': record[f'taxi_zone__{style}'],
            'zone_type': record[f'taxi_zone__zoning__{zone_type}'],
            'weather': {
                'temp': record['dt_iso__temp'],
                'weather_description': record['dt_iso__weather_main'],
                'weather_icon': record['dt_iso__weather_icon']
            }
        }

    return results
