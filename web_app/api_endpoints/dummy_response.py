from random import randint, randrange
from sqlalchemy import create_engine, URL, MetaData, Table, select, func
from credentials import pg_conn


def create_response():
    """
    Creates a response dictionary with data from 10 randomly selected records
    from the 'weather_fc' table in the 'cityframe' schema of a database.

    The response dictionary maps each randomly selected zone ID (from a predefined list)
    to a dictionary containing datetime, busyness, tree density, style and weather data.
    The weather data is obtained from the 'weather_fc' table and the rest are either
    predefined (style) or randomly generated (busyness, tree density).

    For each zone ID, the function randomly selects a row from the 'weather_fc' table,
    uses this row's data to populate the corresponding values in the response dictionary,
    and then removes the zone ID from the list to avoid duplication.

    The 'dt_iso' field is converted to a string in the format 'YYYY-MM-DD HH:MM' before
    it is added to the response dictionary.

    Returns:
         A dictionary mapping zone IDs to dictionaries containing datetime, busyness, tree density, style and weather data.
    """
    zone_ids = [4, 12, 13, 24, 41, 42, 43, 45, 48, 50, 68, 74, 75, 79, 87, 88, 90, 100, 103, 107, 113, 114, 116, 120,
                125, 127, 128, 137, 140, 141, 142, 143, 144, 148, 151, 152, 153, 158, 161, 162, 163, 164, 166, 170, 186,
                194, 202, 209, 211, 224, 229, 230, 231, 232, 233, 234, 236, 237, 238, 239, 243, 244, 246, 249, 261, 262,
                263]

    dummy_response = {}

    pg_url = URL.create(
        "postgresql+psycopg",
        **pg_conn
    )

    engine = create_engine(pg_url)
    table = Table("weather_fc", MetaData(), autoload_with=engine, schema="cityframe")

    with engine.begin() as connection:
        random_weather_query = select(table).order_by(func.random()).limit(10)
        random_weather = connection.execute(random_weather_query).fetchall()

    for row in random_weather:
        random_index = randint(0, len(zone_ids) - 1)
        random_zone = zone_ids.pop(random_index)

        dummy_response[random_zone] = {"dt_iso": row.dt_iso.strftime('%Y-%m-%d %H:%M'),
                                       "busyness": randrange(1, 6),
                                       "trees": randrange(1, 6),
                                       "style": "default",
                                       "weather":
                                           {"temp": row.temp,
                                            "wind_speed": row.wind_speed,
                                            "weather_description": row.weather_description,
                                            "weather_icon": row.weather_icon
                                            }
                                       }
    return dummy_response
