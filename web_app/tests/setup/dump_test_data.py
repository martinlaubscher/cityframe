import os
import django

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_app.settings_dev'
django.setup()

import json
import datetime
from django.db import connections


def custom_serializer(o):
    """
    Custom serializer for JSON serialization of datetime objects.

    Args:
        o (object): The object to be serialized.

    Returns:
        str: The ISO format of the datetime object if it is an instance of datetime.

    Raises:
        TypeError: If the object is not an instance of datetime.
    """

    if isinstance(o, datetime.datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {type(o)} is not JSON serializable")


def export_production_data():
    """
    Exports production data from specific tables into a JSON file.

    Connects to the default database and executes SELECT queries on specified tables,
    then exports the results into a JSON file named 'test_data.json'. The tables and queries are
    defined within the 'export_queries' dictionary.

    Uses the custom_serializer function to handle datetime objects.

    Note: Ensure that database connections and table structures are correctly set up before running this function.
    """

    cursor = connections['default'].cursor()

    export_queries = {'cityframe.weather_current': 'SELECT * FROM cityframe.weather_current',
                      'cityframe.weather_fc': 'SELECT * FROM cityframe.weather_fc LIMIT 1',
                      'cityframe.taxi_zones': 'SELECT * FROM cityframe.taxi_zones',
                      'cityframe."Results"': 'SELECT DISTINCT ON (taxi_zone) * FROM cityframe."Results"'}

    export_data = {}

    for table, query in export_queries.items():
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        export_data[table] = [dict(zip(columns, row)) for row in rows]

    with open('test_data.json', 'w') as f:
        json.dump(export_data, f, default=custom_serializer)


if __name__ == '__main__':
    export_production_data()
