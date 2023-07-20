import requests
import psycopg2
from data_apis.creds import pg_url, openweather_key
from datetime import datetime


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
        'weather_main': data['weather'][0]['main'],
        'weather_description': data['weather'][0]['description'],
        'weather_icon': data['weather'][0]['icon'],
        'timezone': data['timezone']
    }

    # Connect to db
    conn = psycopg2.connect(pg_url.render_as_string(hide_password=False))
    cur = conn.cursor()

    # Delete all existing records in the table
    cur.execute("DELETE FROM cityframe.weather_current;")

    # Construct SQL query
    query = """
        INSERT INTO cityframe.weather_current (dt, dt_iso, temp, feels_like, temp_min, temp_max, pressure, humidity, 
        visibility, wind_speed, wind_deg, clouds_all, weather_id, weather_main, weather_description, weather_icon, 
        timezone)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    # Execute the SQL query
    cur.execute(query, (
        weather_data['dt'], weather_data['dt_iso'], weather_data['temp'], weather_data['feels_like'],
        weather_data['temp_min'], weather_data['temp_max'], weather_data['pressure'], weather_data['humidity'],
        weather_data['visibility'], weather_data['wind_speed'], weather_data['wind_deg'], weather_data['clouds_all'],
        weather_data['weather_id'], weather_data['weather_main'], weather_data['weather_description'],
        weather_data['weather_icon'], weather_data['timezone']
    ))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cur.close()
    conn.close()


update_weather()
