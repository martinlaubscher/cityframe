import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
taxi_path = os.path.join(current_path, "../..", "GeoJSON", "manhattan_taxi_zones.geojson")
building_path = os.path.join(current_path, "../..", "GeoJSON", "Building_points.geojson")
tree_path = os.path.join(current_path, "../..", "GeoJSON", "tree_points.geojson")

sys.path.append(cityframe_path)

from sqlalchemy import create_engine, URL, MetaData, Table, desc, func
from sqlalchemy.dialects.postgresql import insert
import json
from credentials import pg_conn
import geopandas as gpd
from data.Mapping_Buildings_and_Zones.points_in_zones import map_points_to_zones, rank_zones_by_point_presence, \
    map_to_scale
from data.database.data_population_scripts.populate_zone_types import populate_zone_types
from data.database.data_population_scripts.populate_zone_styles import populate_zone_styles


# SCRIPT TO POPULATE THE TAXI_ZONES TABLE WITH STATIC DATA FROM TAXI ZONES, BUILDINGS, AND TREES GEOJSON FILES

populate_zone_types()
populate_zone_styles()

# create url for connection to database
pg_url = URL.create(
    "postgresql+psycopg",
    **pg_conn
)

# intialise sql engine and table objects
engine = create_engine(pg_url, echo=True)
zones_table = Table('zones', MetaData(), autoload_with=engine, schema='cityframe')
zone_styles_table = Table('zone_styles', MetaData(), autoload_with=engine, schema='cityframe')
zone_types_table = Table('zone_types', MetaData(), autoload_with=engine, schema='cityframe')

# list storing dictionaries that each represent one record in the db
vals = []

# read files needed to map buildings/trees to taxi zones
building_points = gpd.read_file(building_path)
tree_points = gpd.read_file(tree_path)
zone_polygons = gpd.read_file(taxi_path)
building_feature_filter = 'Style_Prim'

# create dictionaries for buildings/trees per taxi zone
building_counts_in_zones = map_points_to_zones(building_points, zone_polygons, building_feature_filter)
tree_counts_in_zones = rank_zones_by_point_presence(zone_polygons, tree_points)
tree_counts_scaled = map_to_scale(tree_counts_in_zones)



# connect to db
with engine.begin() as connection:
    # clear table
    connection.execute(zones_table.delete())

    # load taxi zone geojson
    with open(taxi_path, 'r') as f:
        data = json.load(f)
    # loop through taxi zones and add id + zone name to dictionary for that zone
    for feature in data['features']:
        properties = feature['properties']
        row = {'location_id': int(properties['location_id']),
               'zone': str.lower(properties['zone']),
               'trees': tree_counts_in_zones.get(properties['zone'], 0),
               'trees_scaled': tree_counts_scaled.get(properties['zone'], 1)}
        # add tree count to dictionary
        # add tree counts mapped to scale 1-5 to dictionary
        # append the dictionary representing the record to the list of all records
        vals.append(row)
    # sort the contents of vals by the location id
    vals = sorted(vals, key=lambda i: i['location_id'])

    # Get the style with the highest count per location_id from the zone_styles table
    zone_style_maxes = {}
    for location_id in [val['location_id'] for val in vals]:
        result = connection.execute(
            zone_styles_table.select()
            .where(zone_styles_table.c.location_id == location_id)
            .order_by(desc(zone_styles_table.c.zone_style_value))
            .limit(1)
        ).fetchone()

        if result:
            zone_style_maxes[location_id] = {
                'zone_style': result[1],
                'zone_style_value': result[2]
            }

    # Get the type with the highest percentage per location_id from the zone_types table
    zone_type_maxes = {}
    for location_id in [val['location_id'] for val in vals]:
        result = connection.execute(
            zone_types_table.select()
            .where(zone_types_table.c.location_id == location_id)
            .order_by(desc(zone_types_table.c.zone_type_value))
            .limit(1)
        ).fetchone()

        if result:
            zone_type_maxes[location_id] = {
                'zone_type': result[1],
                'zone_type_value': result[2]
            }

    # Update vals to include the new columns
    for val in vals:
        if val['location_id'] in zone_style_maxes:
            val.update(zone_style_maxes[val['location_id']])

        if val['location_id'] in zone_type_maxes:
            val.update(zone_type_maxes[val['location_id']])

    # prepare the insert statement - on conflict do nothing is necessary since zone 103 has three entries
    # due to it consisting of three islands
    insert_stmt = insert(zones_table).on_conflict_do_nothing()
    # executing the query
    connection.execute(insert_stmt, vals)
