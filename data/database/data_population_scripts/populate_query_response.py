import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

import random
from datetime import datetime
import pytz
import requests


def generate_queries():
    # Define possible styles
    styles = ["neo-Georgian", "Beaux-Arts", "Renaissance Revival", "neo-Grec",
              "Romanesque Revival", "Greek Revival", "Queen Anne", "Italianate",
              "neo-Renaissance", "Federal"]

    # Define the New York timezone
    ny_tz = pytz.timezone('America/New_York')

    # Initialize the random number generator
    random.seed()

    # Define the URL for the POST request
    url = "http://127.0.0.1:8000/api/submit-main"

    # Generate 10 queries
    for _ in range(10):
        # Generate random values for busyness, trees, and style
        busyness = random.randint(1, 5)
        trees = random.randint(1, 5)
        style = random.choice(styles)

        # Generate a random time for today in New York
        now = datetime.now(ny_tz)
        random_time = now.replace(hour=random.randint(0, 23), minute=0, second=0)

        # Create the query
        query = {
            "busyness": busyness,
            "trees": trees,
            "time": random_time.strftime("%Y-%m-%d %H:%M"),
            "style": style
        }

        # Send the POST request
        response = requests.post(url, data=query)

        # Check the status of the request
        if response.status_code == 200:
            print(f"Successfully sent query: {query}")
        else:
            print(f"Failed to send query: {query}. Status code: {response.status_code}")


if __name__ == '__main__':
    generate_queries()
