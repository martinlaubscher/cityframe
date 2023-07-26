CREATE SCHEMA IF NOT EXISTS cityframe;
CREATE TABLE cityframe.weather_fc (
    dt BIGINT PRIMARY KEY,
    dt_iso TIMESTAMP WITH TIME ZONE,
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

CREATE TABLE IF NOT EXISTS cityframe."results"
(
    taxi_zone bigint,
    prediction real,
    bucket integer,
    dt_iso timestamp with time zone,
    id bigint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS cityframe."results"
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS cityframe.taxi_zones
(
    location_id integer NOT NULL DEFAULT nextval('cityframe.taxi_zones_location_id_seq'::regclass),
    zone character varying COLLATE pg_catalog."default",
    trees integer,
    trees_scaled integer,
    "neo-Georgian" integer,
    "Greek Revival" integer,
    "Romanesque Revival" integer,
    "neo-Grec" integer,
    "Renaissance Revival" integer,
    "Beaux-Arts" integer,
    "Queen Anne" integer,
    "Italianate" integer,
    "Federal" integer,
    "neo-Renaissance" integer,
    CONSTRAINT taxi_zones_pkey PRIMARY KEY (location_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS cityframe.taxi_zones
    OWNER to postgres;

INSERT INTO cityframe.weather_current
(dt, dt_iso, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds_all,
 weather_id, weather_main, weather_description, weather_icon, timezone)
VALUES
(1689791647, '2023-08-02 12:00:00', 297.5, 298.03, 295.16, 300.16, 1018, 78, 8047, 3.13, 194, 100, 721, 'Haze', 'haze',
 '50d', -14400);

INSERT INTO cityframe.weather_fc(
	dt, dt_iso, temp, visibility, feels_like, temp_min, temp_max, pressure, humidity, wind_speed, wind_deg, wind_gust, pop, rain_1h, snow_1h, clouds_all, weather_id, weather_main, weather_description, weather_icon)
VALUES (
    1690290000,
    '2023-07-25 13:00:00.000000 +00:00',
    297.36,
    10000,
    297.66,
    297.36,
    298.49,
    1020,
    70,
    2.71,
    236,
    3.87,
    0,
    0,
    0,
    0,
    800,
    'Clear',
    'clear sky',
    '01d'
);

INSERT INTO cityframe.results (taxi_zone, prediction, bucket, dt_iso, id)
VALUES
(4, 6.3052654, 2, '2023-07-25 13:00:00.000000 +00:00', 1),
(4, 8.086619, 2, '2023-07-25 14:00:00.000000 +00:00', 2),
(4, 10.359337, 3, '2023-07-25 15:00:00.000000 +00:00', 3),
(4, 10.460033, 3, '2023-08-03 15:00:00.000000 +00:00', 219),
(4, 12.408764, 3, '2023-08-03 16:00:00.000000 +00:00', 220);

INSERT INTO cityframe.taxi_zones (taxi_zone, prediction, bucket, dt_iso, id) VALUES
(4, 6.3052654, 2, '2023-07-25 13:00:00.000000 +00:00', 1),
(4, 8.086619, 2, '2023-07-25 14:00:00.000000 +00:00', 2),
(4, 10.359337, 3, '2023-07-25 15:00:00.000000 +00:00', 3),
(4, 10.7665205, 3, '2023-07-25 16:00:00.000000 +00:00', 4),
(4, 10.563214, 3, '2023-07-25 17:00:00.000000 +00:00', 5),
(4, 12.097611, 3, '2023-07-25 18:00:00.000000 +00:00', 6),
(4, 13.619446, 3, '2023-07-25 19:00:00.000000 +00:00', 7),
(4, 15.719019, 3, '2023-07-25 20:00:00.000000 +00:00', 8),
(4, 17.899107, 3, '2023-07-25 21:00:00.000000 +00:00', 9),
(4, 16.971943, 3, '2023-07-25 22:00:00.000000 +00:00', 10),
(4, 15.783954, 3, '2023-07-25 23:00:00.000000 +00:00', 11),
(4, 9.821317, 3, '2023-07-26 00:00:00.000000 +00:00', 12),
(4, 8.591915, 2, '2023-07-26 01:00:00.000000 +00:00', 13),
(4, 7.020133, 2, '2023-07-26 02:00:00.000000 +00:00', 14),
(4, 8.793227, 2, '2023-07-26 03:00:00.000000 +00:00', 15),
(4, 4.564851, 2, '2023-07-26 04:00:00.000000 +00:00', 16),
(4, 3.7669141, 2, '2023-07-26 05:00:00.000000 +00:00', 17),
(4, 2.7539542, 1, '2023-07-26 06:00:00.000000 +00:00', 18),
(4, 2.017613, 1, '2023-07-26 07:00:00.000000 +00:00', 19),
(4, 2.9776967, 1, '2023-07-26 08:00:00.000000 +00:00', 20);
