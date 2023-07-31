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
    wind_gust INT NOT NULL,
    rain_1h FLOAT NOT NULL,
    snow_1h FLOAT NOT NULL,
    clouds_all INT NOT NULL,
    weather_id INT NOT NULL,
    weather_main VARCHAR(200) NOT NULL,
    weather_description VARCHAR(200) NOT NULL,
    weather_icon VARCHAR(200) NOT NULL,
    timezone INT NOT NULL
);

CREATE TABLE cityframe."Results" (
    taxi_zone bigint,
    prediction real,
    bucket integer,
    dt_iso timestamp with time zone,
    id bigint
);

-- TABLESPACE pg_default;

ALTER TABLE IF EXISTS cityframe."Results"
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS cityframe.taxi_zones (
    location_id integer NOT NULL,
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
);

-- TABLESPACE pg_default;

ALTER TABLE IF EXISTS cityframe.taxi_zones
    OWNER to postgres;

