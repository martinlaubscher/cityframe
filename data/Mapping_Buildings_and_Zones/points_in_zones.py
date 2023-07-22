import geopandas as gpd
from collections import defaultdict


def get_filtered_gdf(gdf, feature_name, points_id):
    """

    Function to filter a GeoDataFrame by a given value for a given feature.

    Args:

        gdf (GeoDataFrame): GeoDataFrame to be filtered
        feature_name (str): name of feature to be used as filter
        points_id (str): value to filter feature by
        
    Returns:

        GeoDataFrame: filtered GeoDataFrame

    """
    filtered_gdf = gdf[gdf[feature_name] == points_id]
    
    return filtered_gdf


def rank_zones_by_point_presence(polygons_gdf, points_gdf):
    """
    
    Function to filter polygons by the presence or absence of points within those polygons.

    Args:

        polygons_gdf (GeoDataFrame): the polygons to be filtered
        points_gdf (GeoDataFrame): the points to act as a filter

    Returns:

        Dictionary in which the key is the name_id(str) of a polygon and the value(int) the number of points present within that polygon.
        eg. {'Seaport' : 23, 'SoHo' : 46}

    """
   
    zones_list = []
    # Filter the polygons based on point inclusion
    filtered_polygons_gdf = polygons_gdf[polygons_gdf.geometry.apply(lambda poly: any(poly.contains(point) for point in points_gdf.geometry))]

    # Create a dictionary to map zone to point count
    zone_point_count = defaultdict(int)

    # Iterate over the filtered polygons and count the points within each polygon
    for _, polygon in filtered_polygons_gdf.iterrows():
        zone = polygon['zone']
        points_within_polygon = points_gdf[points_gdf.geometry.within(polygon.geometry)]
        point_count = len(points_within_polygon)
        zone_point_count[zone] = point_count

    # Keep a list of the taxi zones which are now being used
    zones_list.extend(filtered_polygons_gdf['zone'])

    return zone_point_count


def sort_dictionary(dictionary):
    """
    Function to sort a dictionary by its values in descending order.

    Returns:

        Dictionary sorted by its values in descending order.
        eg. {'SoHo' : 46, 'Seaport' : 20}

    """
    sorted_dict = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
    return sorted_dict


def map_points_to_zones(points_gdf, polygons_gdf, feature_name):
    """
    Function to loop through and map all points from a points gdf to a polygons gdf.

    Args:

        points_gdf (GeoDataFrame): points to be mapped to polygons
        polygons_gdf (GeoDataFrame): polygons to be mapped to points
        feature_name (str): name of feature to be used as filter and key in dictionary

    Returns:

        Dictionary mapping feature_name(str) to dictionary(dict) of ranked polygons by points count.

    Function Dependencies:

        get_filtered_gdf(gdf, feature_name, points_id)
        rank_zones_by_point_presence(polygons_gdf, points_gdf)
        sort_dictionary(dictionary)

    """

    points_in_zones = {}

    for point_id in points_gdf[feature_name].unique():
        filtered_points_gdf = get_filtered_gdf(points_gdf, feature_name, point_id)
        zone_point_count = rank_zones_by_point_presence(polygons_gdf, filtered_points_gdf)
        sorted_dict = sort_dictionary(zone_point_count)
        points_in_zones[point_id] = sorted_dict
    
    return points_in_zones


# *** tests ***
# building_points = gpd.read_file("../GeoJSON/Building_points.geojson")
# zone_polygons = gpd.read_file("../GeoJSON/manhattan_taxi_zones.geojson")
# building_feature_filter = 'Style_Prim'
#
# building_counts_in_zones = map_points_to_zones(building_points, zone_polygons, building_feature_filter)
# print(building_counts_in_zones)
# print(building_counts_in_zones.keys())
#
# tree_points = gpd.read_file("../GeoJSON/tree_points.geojson")
# zone_polygons = gpd.read_file("../GeoJSON/manhattan_taxi_zones.geojson")
# tree_counts_in_zones = rank_zones_by_point_presence(zone_polygons, tree_points)
# print(tree_counts_in_zones)
