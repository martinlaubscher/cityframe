from django.db import connections
import json
import datetime
from dateutil import tz


class CommonSetup:
    """
    A class to provide common setup methods for test environments.

    This class contains methods to deserialize dates, import test data, and set up
    common requirements for the test database.
    """

    @classmethod
    def deserialize_date(cls, iso_str):
        """
        Convert an ISO formatted date string into a datetime object.

        Args:
            iso_str (str): An ISO formatted date string.

        Returns:
            datetime.datetime: A datetime object corresponding to the given date string.
            None if the given string is empty or None.
        """

        return datetime.datetime.fromisoformat(iso_str) if iso_str else None

    @classmethod
    def import_test_data(cls, cursor):
        """
        Import test data from a JSON file and insert it into the database.

        Args:
            cursor (cursor): A database cursor object to execute SQL commands.
        """

        with open('tests/setup/test_data.json', 'r') as f:
            data_to_import = json.load(f)

        for table, rows in data_to_import.items():
            if rows:
                # quote the column names to handle special characters - needed for building style columns
                columns = [f'"{column}"' for column in rows[0].keys()]
                values_placeholders = ', '.join(['%s'] * len(columns))
                columns_str = ', '.join(columns)
                insert_query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_placeholders})"
                for row in rows:
                    # convert date strings back to datetime objects
                    row_values = [cls.deserialize_date(value) if isinstance(value, str) and '-' in value else value for
                                  value in row.values()]
                    cursor.execute(insert_query, row_values)

    @classmethod
    def common_setup(cls):
        """
        Perform common setup tasks required for both Selenium and Django tests.

        This method sets up the test environment, including initializing the test database
        and importing the necessary test data.
        """

        current_dt = datetime.datetime.now(tz=tz.UTC).replace(minute=0, second=0, microsecond=0)
        cursor = connections['default'].cursor()

        with open('tests/setup/test_db_setup.sql') as f:
            cursor.execute(f.read())

        cls.import_test_data(cursor)

        cursor.execute(f"UPDATE cityframe.\"Results\" SET dt_iso = '{current_dt}'")
        cursor.execute(f"UPDATE cityframe.weather_fc SET dt_iso = '{current_dt}'")

        cursor.close()
