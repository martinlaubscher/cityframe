import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(current_path))
taxi_path = os.path.join(current_path, "..", "GeoJSON", "manhattan_taxi_zones.geojson")
building_path = os.path.join(current_path, "..", "GeoJSON", "Building_points.geojson")

sys.path.append(cityframe_path)

from sqlalchemy import inspect, create_engine, URL, Table, MetaData, Column, Integer, BigInteger, String, Float, \
    DateTime, Index, ForeignKey
from sqlalchemy.schema import CreateSchema
import geopandas as gpd
from credentials import pg_conn
from data.Mapping_Buildings_and_Zones.points_in_zones import map_points_to_zones


class Schema:
    """
    This class represents a database schema.

    Class Attributes:
        schemas (list): A list of all Schema objects.
    """

    schemas = []

    def __init__(self, schema_name):
        """
        Initialise a Schema object and add it to the list of schemas.

        Args:
            schema_name (str): The name of the schema.
        """

        self.name = schema_name
        Schema.schemas.append(self)

    def check(self):
        """
        Check if the schema exists in the database.

        Returns:
            bool: True if the schema does not exist, False otherwise.
        """

        return self.name not in inspector.get_schema_names()

    def create(self):
        """
        Create the schema in the database if it does not already exist.
        """

        if self.check():
            with engine.begin() as connection:
                connection.execute(CreateSchema(self.name))

    @classmethod
    def create_all(cls):
        """
        Create all schemas in the 'schemas' list that do not already exist in the database.
        """

        for schema in cls.schemas:
            schema.create()


class DatabaseTable(Table):
    """
    This class represents a database table.

    Class Attributes:
        tables (list): A list of all DatabaseTable objects.
    """

    tables = []
    meta = MetaData()

    def __init__(self, name, metadata, *args, **kw):
        """
        Initialise a DatabaseTable object and add it to the list of tables.

        Args:
            name (str): The name of the table.
            metadata (MetaData): MetaData instance associated with this table.
            *args: Variable length argument list.
            **kw: Arbitrary keyword arguments.
        """

        super().__init__(name, metadata, *args, **kw)
        DatabaseTable.tables.append(self)

    @classmethod
    def create_all(cls):
        """
        Create all tables in the 'tables' list that do not already exist in the database.
        """

        for table in cls.tables:
            table.metadata.create_all(engine, checkfirst=True)


if __name__ == '__main__':
    # Create the sqlalchemy url
    pg_url = URL.create(
        "postgresql+psycopg",
        **pg_conn
    )

    # Create an engine that connects to the database
    engine = create_engine(pg_url, echo=True)

    # Initialise inspector
    inspector = inspect(engine)

    # Initialise schemas to be added (currently, only cityframe)
    Schema('cityframe')

    # initialise database tables to be added
    DatabaseTable(
        'weather_fc', DatabaseTable.meta,
        Column('dt', BigInteger, primary_key=True),
        Column('dt_iso', DateTime(timezone=True), unique=True),
        Column('temp', Float),
        Column('visibility', Integer),
        Column('feels_like', Float),
        Column('temp_min', Float),
        Column('temp_max', Float),
        Column('pressure', Integer),
        Column('humidity', Integer),
        Column('wind_speed', Float),
        Column('wind_deg', Integer),
        Column('wind_gust', Float),
        Column('pop', Float),
        Column('rain_1h', Float),
        Column('snow_1h', Float),
        Column('clouds_all', Integer),
        Column('weather_id', Integer),
        Column('weather_main', String),
        Column('weather_description', String),
        Column('weather_icon', String),
        schema='cityframe'
    )

    DatabaseTable(
        'weather_current', DatabaseTable.meta,
        Column('dt', BigInteger, primary_key=True),
        Column('dt_iso', DateTime),
        Column('temp', Float),
        Column('visibility', Integer),
        Column('feels_like', Float),
        Column('temp_min', Float),
        Column('temp_max', Float),
        Column('pressure', Integer),
        Column('humidity', Integer),
        Column('wind_speed', Float),
        Column('wind_deg', Integer),
        Column('wind_gust', Float, default=0),
        Column('rain_1h', Float, default=0),
        Column('snow_1h', Float, default=0),
        Column('clouds_all', Integer, default=0),
        Column('weather_id', Integer),
        Column('weather_main', String),
        Column('weather_description', String),
        Column('weather_icon', String),
        Column('timezone', Integer),
        schema='cityframe'
    )

    # # initialising taxi_zones table
    # taxi_zones = DatabaseTable(
    #     'taxi_zones', DatabaseTable.meta,
    #     # Column('id', Integer, autoincrement=True, primary_key=True),
    #     Column('location_id', Integer, primary_key=True),
    #     Column('zone', String),
    #     Column('trees', Integer),
    #     Column('trees_scaled', Integer),
    #     # Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=4326)),
    #     schema='cityframe'
    # )
    #
    # # getting architecture styles
    # building_points = gpd.read_file(building_path)
    # zone_polygons = gpd.read_file(taxi_path)
    # building_feature_filter = 'Style_Prim'
    # building_counts_in_zones = map_points_to_zones(building_points, zone_polygons, building_feature_filter)
    #
    # # looping through styles to add corresponding columns to taxi_zones table
    # for i in building_counts_in_zones.keys():
    #     taxi_zones.append_column(Column(i, Integer))

    zones = DatabaseTable(
        'zones', DatabaseTable.meta,
        Column('location_id', Integer, primary_key=True),
        Column('zone', String),
        Column('trees', Integer),
        Column('trees_scaled', Integer),
        Column('main_zone_style', String),
        Column('main_zone_style_value', Integer),
        Column('main_zone_type', String),
        Column('main_zone_type_value', Float),
        schema='cityframe'

    )

    zone_styles = DatabaseTable(
        'zone_styles', DatabaseTable.meta,
        Column('location_id', Integer, primary_key=True),
        Column('zone_style', String, primary_key=True),
        Column('zone_style_value', Integer),
        schema='cityframe'
    )

    zone_types = DatabaseTable(
        'zone_types', DatabaseTable.meta,
        Column('location_id', Integer, primary_key=True),
        Column('zone_type', String, primary_key=True),
        Column('zone_type_value', Float),
        schema='cityframe'
    )

    # creating all schemas initialised previously - if they don't exist yet
    Schema.create_all()
    # creating all database tables initialised previously - if they don't exist yet
    DatabaseTable.create_all()
