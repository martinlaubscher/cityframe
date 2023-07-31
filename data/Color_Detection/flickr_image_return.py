import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(current_path))
taxi_path = os.path.join(current_path, "..", "GeoJSON", "taxi_zones_with_centroid.geojson")

sys.path.append(cityframe_path)

import requests
import geopandas as gpd
from credentials import flickr_api_key

def get_flickr_image(api_key, lat, lon):
    base_url = "https://api.flickr.com/services/rest/"
    method = "flickr.photos.search"
    params = {
        "api_key": api_key,
        "method": method,
        "format": "json",
        "nojsoncallback": 1,
        "lat": lat,
        "lon": lon,
        "radius": 2,  # Radius in km. You can adjust this value as needed.
        "sort": "relevance",
        "per_page": 1,  # You can adjust the number of images returned here.
        "geo_context": 2,  # outdoor photos
        "accuracy": 14,  # accuracy of location information (street level ~16)
        "content_types": 0  # photos only
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["stat"] == "ok" and "photos" in data and "photo" in data["photos"] and len(data["photos"]["photo"]) > 0:
            # Get the first photo from the response
            photo = data["photos"]["photo"][0]
            image_url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
            return image_url
        else:
            print("Error: No photos found in the search.")
    else:
        print("Error: API request to Flickr failed.")

    return None

gdf = gpd.read_file(taxi_path)
api_key = flickr_api_key
print(gdf.shape)
image_urls = []

for index, row in gdf.iterrows():
    point = row['point']
    split = point.split()
    lng = split[0]
    lat = split[1]
    image_url = get_flickr_image(api_key, lat, lng)
    if image_url is None:
        image_url = "https://i1.sndcdn.com/artworks-CyTzk0PMsjHFfr7D-S8wWcw-t500x500.jpg"
    image_urls.append(image_url)
print(len(image_urls))
print(image_urls)


