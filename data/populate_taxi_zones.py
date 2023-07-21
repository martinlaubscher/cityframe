from sqlalchemy import create_engine, URL, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
import json
from credentials import pg_conn
import geopandas as gpd
from Mapping_Buildings_and_Zones.buildings_in_zones import map_points_to_zones

pg_url = URL.create(
    "postgresql+psycopg",
    **pg_conn
)

engine = create_engine(pg_url, echo=True)
table = Table('taxi_zones', MetaData(), autoload_with=engine, schema='cityframe')

vals = []

building_points = gpd.read_file("GeoJSON/Building_points.geojson")
zone_polygons = gpd.read_file("GeoJSON/manhattan_taxi_zones.geojson")
building_feature_filter = 'Style_Prim'

building_counts_in_zones = map_points_to_zones(building_points, zone_polygons, building_feature_filter)

with engine.begin() as connection:
    with open('GeoJSON/manhattan_taxi_zones.geojson', 'r') as f:
        data = json.load(f)
    for feature in data['features']:
        properties = feature['properties']
        # geom = json.dumps(feature['geometry'])

        row = {'location_id': int(properties['location_id']), 'zone': properties['zone']}

        for style in building_counts_in_zones.keys():
            if building_counts_in_zones[style].get(properties['zone']) is not None:
                row[style] = building_counts_in_zones[style].get(properties['zone'])
            else:
                row[style] = 0

        vals.append(row)

    vals = sorted(vals, key=lambda i: i['location_id'])
    print(vals)
    insert_stmt = insert(table).on_conflict_do_nothing()
    connection.execute(insert_stmt, vals)
