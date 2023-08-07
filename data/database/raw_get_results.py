import os
import sys
from datetime import timedelta

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(current_path))

sys.path.append(cityframe_path)

from psycopg.rows import dict_row
from dateutil import tz
from django.apps import apps

pool = apps.get_app_config('api_endpoints').pool

def raw_get_results(style, weather, zone_type, user_time, tree_range=(1, 5), busyness_range=(1, 5)):

    if weather is None:
        time_from = user_time - timedelta(hours=12)
        time_to = user_time + timedelta(hours=12)

        sql = f'''
        SELECT "cityframe"."Results"."taxi_zone", "cityframe"."taxi_zones"."zone", "cityframe"."Results"."dt_iso", "cityframe"."Results"."bucket", "cityframe"."taxi_zones"."trees_scaled", "cityframe"."taxi_zones"."{style}", "cityframe"."zoning"."{zone_type}", "cityframe"."weather_fc"."temp", "cityframe"."weather_fc"."weather_main", "cityframe"."weather_fc"."weather_icon"
        FROM "cityframe"."Results"
        INNER JOIN "cityframe"."weather_fc" ON ("cityframe"."Results"."dt_iso" = "cityframe"."weather_fc"."dt_iso")
        INNER JOIN "cityframe"."taxi_zones" ON ("cityframe"."Results"."taxi_zone" = "cityframe"."taxi_zones"."location_id")
        LEFT OUTER JOIN "cityframe"."zoning" ON ("cityframe"."taxi_zones"."location_id" = "cityframe"."zoning"."location_id")
        WHERE ("cityframe"."Results"."dt_iso" BETWEEN '{time_from}'::timestamptz AND '{time_to}'::timestamptz AND "cityframe"."Results"."taxi_zone" IN (SELECT U0."location_id" FROM "cityframe"."taxi_zones" U0 WHERE U0."{style}" > 0));'''
    else:
        sql = f'''
        SELECT "cityframe"."Results"."taxi_zone", "cityframe"."taxi_zones"."zone", "cityframe"."Results"."dt_iso", "cityframe"."Results"."bucket", "cityframe"."taxi_zones"."trees_scaled", "cityframe"."taxi_zones"."{style}", "cityframe"."zoning"."{zone_type}", "cityframe"."weather_fc"."temp", "cityframe"."weather_fc"."weather_main", "cityframe"."weather_fc"."weather_icon"
        FROM "cityframe"."Results"
        INNER JOIN "cityframe"."weather_fc" ON ("cityframe"."Results"."dt_iso" = "cityframe"."weather_fc"."dt_iso")
        INNER JOIN "cityframe"."taxi_zones" ON ("cityframe"."Results"."taxi_zone" = "cityframe"."taxi_zones"."location_id")
        LEFT OUTER JOIN "cityframe"."zoning" ON ("cityframe"."taxi_zones"."location_id" = "cityframe"."zoning"."location_id")
        WHERE ("cityframe"."weather_fc"."weather_main" = '{weather}' AND "cityframe"."Results"."taxi_zone" IN (SELECT U0."location_id" FROM "cityframe"."taxi_zones" U0 WHERE U0."{style}" > 0));'''

    # Create a new transaction
    with pool.connection() as conn:

        # Create a new cursor to execute the SQL statement
        with conn.cursor(row_factory=dict_row) as cur:
            # Execute SQL statement
            cur.execute(sql)

            # Fetch the results as dictionaries
            records = cur.fetchall()

    results = {}
    ny_tz = tz.gettz('America/New_York')
    for record in records:
        key = f"{record['taxi_zone']}_{record['dt_iso']}"
        ny_dt_iso = record['dt_iso'].astimezone(ny_tz)
        results[key] = {
            'id': str(record['taxi_zone']),
            'zone': record['zone'],
            'dt_iso': ny_dt_iso.strftime('%Y-%m-%d %H:%M'),
            'dt_iso_tz': ny_dt_iso,
            'busyness': record['bucket'],
            'trees': record['trees_scaled'],
            'style': record[f'{style}'],
            'zone_type': record[f'{zone_type}'],
            'weather': {
                'temp': record['temp'],
                'weather_description': record['weather_main'],
                'weather_icon': record['weather_icon']
            }
        }

    return results
