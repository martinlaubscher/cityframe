import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(current_path))
taxi_path = os.path.join(current_path, "../..", "GeoJSON", "manhattan_taxi_zones.geojson")
building_path = os.path.join(current_path, "../..", "GeoJSON", "Building_points.geojson")
tree_path = os.path.join(current_path, "../..", "GeoJSON", "tree_points.geojson")

sys.path.append(cityframe_path)

from sqlalchemy import create_engine, URL, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
import json
from credentials import pg_conn
import geopandas as gpd
from data.Mapping_Buildings_and_Zones.points_in_zones import map_points_to_zones, rank_zones_by_point_presence, \
    map_to_scale

# SCRIPT TO POPULATE THE TAXI_ZONES TABLE WITH STATIC DATA FROM TAXI ZONES, BUILDINGS, AND TREES GEOJSON FILES

# create url for connection to database
pg_url = URL.create(
    "postgresql+psycopg",
    **pg_conn
)

# intialise sql engine and table objects
engine = create_engine(pg_url, echo=True)
table = Table('taxi_zones', MetaData(), autoload_with=engine, schema='cityframe')

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
    connection.execute(table.delete())

    # load taxi zone geojson
    with open(taxi_path, 'r') as f:
        data = json.load(f)
    # loop through taxi zones and add id + zone name to dictionary for that zone
    for feature in data['features']:
        properties = feature['properties']
        row = {'location_id': int(properties['location_id']), 'zone': properties['zone']}
        # loop through building styles and add count of buildings for each style to dictionary
        for style in building_counts_in_zones.keys():
            row[style] = building_counts_in_zones[style].get(properties['zone'], 0)
        # add tree count to dictionary
        row['trees'] = tree_counts_in_zones.get(properties['zone'], 0)
        # add tree counts mapped to scale 1-5 to dictionary
        row['trees_scaled'] = tree_counts_scaled.get(properties['zone'], 1)
        # append the dictionary representing the record to the list of all records
        vals.append(row)
    # sort the contents of vals by the location id
    vals = sorted(vals, key=lambda i: i['location_id'])
    # prepare the insert statement - on conflict do nothin is necessary since zone 103 has three entries
    # due to it consisting of three islands
    insert_stmt = insert(table).on_conflict_do_nothing()
    # executing the query
    connection.execute(insert_stmt, vals)
