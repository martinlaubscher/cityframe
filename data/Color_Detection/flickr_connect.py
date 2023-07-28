import requests
from credentials import flickr_api_key as key


def get_flickr_image(api_key, lat, lon):
    base_url = "https://api.flickr.com/services/rest/"
    method = "flickr.photos.search"
    params = {
        "api_key": api_key,
        "method": method,
        "format": "json",
        "nojsoncallback": 1,
        # "text": search_query,
        "sort": "relevance",
        # "has_geo": 1,  # photo is geotagged
        "geo_context": 2,  # photo taken outdoors
        "lat": lat,
        "lon": lon,
        "radius": 15,  # add radius for search from lat, lon point
        "per_page": 1  # You can adjust the number of images returned here.
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["stat"] == "ok" and "photos" in data and "photo" in data["photos"]:
            # Get the first photo from the response
            photo = data["photos"]["photo"][0]
            image_url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
            return image_url
        else:
            print("Error: Unable to retrieve photo from Flickr.")
    else:
        print("Error: API request to Flickr failed.")

    return None



search_query = "landscape"  # Change this to your desired search query

image_url = get_flickr_image(key , -74.01826464517814, 40.69283698869548)

if image_url:
    print("Image URL:", image_url)
    # Now, you can use the 'image_url' to display the image in your web app.
