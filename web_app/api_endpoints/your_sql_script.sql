CREATE SCHEMA IF NOT EXISTS cityframe;
CREATE TABLE cityframe.weather_fc (
    dt BIGINT PRIMARY KEY,
    dt_iso TIMESTAMP,
    temp FLOAT,
    visibility INT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    pressure INT,
    humidity INT,
    wind_speed FLOAT,
    wind_deg INT,
    wind_gust FLOAT,
    pop FLOAT,
    rain_1h FLOAT,
    snow_1h FLOAT,
    clouds_all INT,
    weather_id INT,
    weather_main VARCHAR,
    weather_description VARCHAR,
    weather_icon VARCHAR
);

CREATE TABLE cityframe.weather_current (
    dt BIGINT PRIMARY KEY,
    dt_iso TIMESTAMP NOT NULL,
    temp FLOAT NOT NULL,
    feels_like FLOAT NOT NULL,
    temp_min FLOAT NOT NULL,
    temp_max FLOAT NOT NULL,
    pressure INT NOT NULL,
    humidity INT NOT NULL,
    visibility INT NOT NULL,
    wind_speed FLOAT NOT NULL,
    wind_deg INT NOT NULL,
    clouds_all INT NOT NULL,
    weather_id INT NOT NULL,
    weather_main VARCHAR(200) NOT NULL,
    weather_description VARCHAR(200) NOT NULL,
    weather_icon VARCHAR(200) NOT NULL,
    timezone INT NOT NULL
);

INSERT INTO cityframe.weather_current
(dt, dt_iso, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds_all,
 weather_id, weather_main, weather_description, weather_icon, timezone)
VALUES
(1689791647, '2023-08-02 12:00:00', 297.5, 298.03, 295.16, 300.16, 1018, 78, 8047, 3.13, 194, 100, 721, 'Haze', 'haze',
 '50d', -14400);

