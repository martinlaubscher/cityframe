import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(current_path))

sys.path.append(cityframe_path)

from sqlalchemy import MetaData, Table, create_engine, URL
from credentials import pg_conn


# create url for connection to database
pg_url = URL.create(
    "postgresql+psycopg",
    **pg_conn
)

# intialise sql engine and table objects
engine = create_engine(pg_url, echo=True)

metadata = MetaData()

# Specify the tables you want to drop.
weather_fc_table = Table('weather_fc', metadata, autoload_with=engine, schema='cityframe')
taxi_zones_table = Table('taxi_zones', metadata, autoload_with=engine, schema='cityframe')

# Drop the tables.
with engine.begin() as connection:
    weather_fc_table.drop(connection)
    taxi_zones_table.drop(connection)
