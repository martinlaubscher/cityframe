import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

sys.path.append(cityframe_path)

import requests
import psycopg
from credentials import pg_conn, openweather_key
from datetime import datetime
from sqlalchemy import URL


def update_weather():
    url = f'https://api.openweathermap.org/data/2.5/weather?lat=40.7831&lon=-73.9712&appid={openweather_key}'
    response = requests.get(url)
    data = response.json()

    dt_iso = datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')

    weather_data = {
        'dt': data['dt'],
        'dt_iso': dt_iso,
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'temp_min': data['main']['temp_min'],
        'temp_max': data['main']['temp_max'],
        'pressure': data['main']['pressure'],
        'humidity': data['main']['humidity'],
        'visibility': data['visibility'],
        'wind_speed': data['wind']['speed'],
        'wind_deg': data['wind']['deg'],
        'clouds_all': data['clouds']['all'],
        'weather_id': data['weather'][0]['id'],
        'weather_main': str.lower(data['weather'][0]['main']),
        'weather_description': data['weather'][0]['description'],
        'weather_icon': data['weather'][0]['icon'],
        'timezone': data['timezone']
    }

    # These values exist only when the weather conditions exist, assigned 0 if not in data
    if 'wind' in data and 'gust' in data['wind']:
        gust = data['wind']['gust']
    else:
        gust = 0

    if 'rain' in data and '1h' in data['rain']:
        rain_1h = data['rain']['1h']
    else:
        rain_1h = 0

    if 'snow' in data and '1h' in data['snow']:
        snow_1h = data['snow']['1h']
    else:
        snow_1h = 0

    weather_data.update({
        'wind_gust': gust,
        'rain_1h': rain_1h,
        'snow_1h': snow_1h,
    })

    pg_url = URL.create(
        "postgresql",
        **pg_conn
    )

    # Connect to db
    conn = psycopg.connect(pg_url.render_as_string(hide_password=False))
    cur = conn.cursor()

    # Delete all existing records in the table
    cur.execute("DELETE FROM cityframe.weather_current;")

    # Construct SQL query
    query = """
        INSERT INTO cityframe.weather_current (dt, dt_iso, temp, feels_like, temp_min, temp_max, pressure, humidity, 
        visibility, wind_speed, wind_deg, clouds_all, weather_id, weather_main, weather_description, weather_icon, 
        timezone, wind_gust, rain_1h, snow_1h)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    # Execute the SQL query
    cur.execute(query, (
        weather_data['dt'], weather_data['dt_iso'], weather_data['temp'], weather_data['feels_like'],
        weather_data['temp_min'], weather_data['temp_max'], weather_data['pressure'], weather_data['humidity'],
        weather_data['visibility'], weather_data['wind_speed'], weather_data['wind_deg'], weather_data['clouds_all'],
        weather_data['weather_id'], weather_data['weather_main'], weather_data['weather_description'],
        weather_data['weather_icon'], weather_data['timezone'], weather_data['wind_gust'], weather_data['rain_1h'],
        weather_data['snow_1h']
    ))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cur.close()
    conn.close()


if __name__ == '__main__':
    update_weather()
