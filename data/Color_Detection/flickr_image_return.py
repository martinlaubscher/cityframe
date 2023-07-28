import requests

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
        "radius": 5,  # Radius in km. You can adjust this value as needed.
        "sort": "relevance",
        "per_page": 1,  # You can adjust the number of images returned here.
        "geo_context": 2  # outdoor photos
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

# Replace 'YOUR_API_KEY' with your actual Flickr API key
api_key = "5fdce5ee86d5986e46fb9477e27cc578"
latitude = 40.758332724348996
longitude = -73.98642379545548

image_url = get_flickr_image(api_key, latitude, longitude)

if image_url:
    print("Image URL:", image_url)
