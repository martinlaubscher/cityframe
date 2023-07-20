from sqlalchemy import inspect, create_engine, Table, MetaData, Column, Integer, BigInteger, String, Float, DateTime
from sqlalchemy.schema import CreateSchema
from creds import pg_url


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
    # Create an engine that connects to the database
    engine = create_engine(pg_url, echo=True)

    # Initialise inspector
    inspector = inspect(engine)

    # Initialise schemas to be added (currently, only cityframe)
    Schema('cityframe')

    # initialise database tables to be added
    DatabaseTable(
        'weather_fc', MetaData(),
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
        'weather_current', MetaData(),
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

    # creating all schemas initialised previously - if they don't exist yet
    Schema.create_all()
    # creating all database tables initialised previously - if they don't exist yet
    DatabaseTable.create_all()
