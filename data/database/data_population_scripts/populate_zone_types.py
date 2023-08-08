import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
zoning_path = os.path.join(current_path, "../..", "GeoJSON", "zoning.geojson")
updated_zoning_path = os.path.join(current_path, "../..", "GeoJSON", "updated_zoning.geojson")
taxi_path = os.path.join(current_path, "../..", "GeoJSON", "manhattan_taxi_zones.geojson")

sys.path.append(cityframe_path)

import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, URL, text
from credentials import pg_conn


# remap the zone values to sth more meaningful
def remap_zonedist(value):
    if value.startswith('C'):
        return 'commercial'
    elif value.startswith('M'):
        return 'manufacturing'
    elif value == 'PARK':
        return 'park'
    else:
        return 'residential'


def populate_zone_types():
    # EPSG for NYC
    nyc_crs = 'EPSG:2263'

    # if the updated zoning file exists, use it. otherwise, create it first.
    if os.path.isfile(updated_zoning_path):
        zoning_gdf = gpd.read_file(updated_zoning_path).to_crs(nyc_crs)
    else:
        zoning_gdf = gpd.read_file(zoning_path).to_crs(nyc_crs)
        zoning_gdf['zonedist'] = zoning_gdf['zonedist'].apply(remap_zonedist)
        zoning_gdf.to_file(updated_zoning_path, driver='GeoJSON')

    # Load the taxi zone GeoJSON and set the crs to the nyc one
    taxi_gdf = gpd.read_file(taxi_path)
    taxi_gdf = taxi_gdf.to_crs(nyc_crs)

    # combine the three Governor's Island/Ellis Island/Liberty Island rows into one and delete the three old rows
    three_islands = taxi_gdf.loc[taxi_gdf['location_id'] == '103', 'geometry'].unary_union
    taxi_gdf = taxi_gdf[taxi_gdf['location_id'] != '103']
    three_islands_row = gpd.GeoDataFrame(pd.DataFrame([{'location_id': '103',
                                                        'geometry': three_islands,
                                                        'zone': 'Governor\'s Island/Ellis Island/Liberty Island'}]),
                                         geometry='geometry')

    # set the crs for the new (combined) row
    three_islands_row.set_crs(nyc_crs, inplace=True)

    # append the new row to the existing df
    taxi_gdf = gpd.GeoDataFrame(pd.concat([taxi_gdf, three_islands_row])).reset_index(drop=True)

    # spatial join between taxi zones and zoning districts
    joined_gdf = gpd.sjoin(taxi_gdf, zoning_gdf, how='left', predicate='intersects')

    # calculate intersection between taxi zones and zoning districts
    joined_gdf['intersection'] = joined_gdf.apply(
        lambda row: row['geometry'].intersection(zoning_gdf.loc[row['index_right'], 'geometry']) if pd.notnull(
            row['index_right']) else None, axis=1)

    # convert intersection to GeoSeries (so that the area can be calculated)
    joined_gdf['intersection'] = gpd.GeoSeries(joined_gdf['intersection'], crs=nyc_crs)

    # calculate the intersection area
    joined_gdf['area'] = joined_gdf['intersection'].area

    # group the df, summing the area per zone/district type
    result_df = joined_gdf.groupby(['location_id', 'zonedist']).agg({'area': 'sum'}).reset_index()
    # calculate how much of each zone is what district type
    result_df['zone_type_value'] = result_df.groupby('location_id')['area'].transform(lambda x: x / x.sum() * 100)
    result_df = result_df.drop(columns=['area'])

    result_df['location_id'] = result_df['location_id'].astype(int)

    result_df = result_df.rename(columns={'zonedist': 'zone_type'})

    result_df = result_df.sort_values(by='location_id')

    engine = create_engine(URL.create("postgresql+psycopg", **pg_conn))

    with engine.begin() as connection:
        connection.execute(text("DELETE FROM cityframe.zone_types;"))

    result_df.to_sql('zone_types', engine, schema='cityframe', if_exists='append', index=False)


if __name__ == '__main__':
    populate_zone_types()
