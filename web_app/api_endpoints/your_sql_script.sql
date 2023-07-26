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

INSERT INTO cityframe.taxi_zones (location_id, zone, trees, trees_scaled, "neo-Georgian", "Greek Revival", "Romanesque Revival", "neo-Grec", "Renaissance Revival", "Beaux-Arts", "Queen Anne", "Italianate", "Federal", "neo-Renaissance") VALUES
(4, 'Alphabet City', 910, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(12, 'Battery Park', 11, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
(13, 'Battery Park City', 767, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(24, 'Bloomingdale', 794, 2, 0, 0, 5, 0, 35, 4, 0, 0, 0, 0),
(41, 'Central Harlem', 2485, 4, 0, 0, 24, 76, 110, 7, 27, 0, 0, 11),
(42, 'Central Harlem North', 3355, 5, 1, 0, 20, 139, 159, 7, 98, 1, 0, 1),
(43, 'Central Park', 932, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(45, 'Chinatown', 461, 1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0),
(48, 'Clinton East', 1253, 2, 0, 0, 0, 0, 1, 0, 6, 0, 0, 0),
(50, 'Clinton West', 634, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(68, 'East Chelsea', 1017, 2, 0, 94, 1, 4, 1, 0, 1, 106, 4, 1),
(74, 'East Harlem North', 2403, 4, 0, 0, 3, 0, 1, 0, 1, 0, 0, 0),
(75, 'East Harlem South', 1750, 3, 2, 0, 4, 1, 0, 0, 1, 0, 0, 3),
(79, 'East Village', 1512, 2, 0, 37, 8, 18, 50, 1, 30, 61, 6, 0),
(87, 'Financial District North', 185, 1, 0, 7, 4, 0, 0, 2, 0, 1, 4, 2),
(88, 'Financial District South', 82, 1, 1, 19, 0, 0, 1, 2, 0, 0, 2, 1),
(90, 'Flatiron', 621, 1, 0, 0, 0, 3, 1, 3, 2, 0, 0, 1),
(100, 'Garment District', 27, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1),
(103, 'Governor''s Island/Ellis Island/Liberty Island', 0, 1, 15, 7, 5, 0, 0, 10, 0, 0, 0, 17),
(107, 'Gramercy', 1087, 2, 1, 19, 2, 1, 2, 2, 0, 16, 0, 2),
(113, 'Greenwich Village North', 626, 1, 1, 116, 10, 8, 17, 5, 10, 20, 3, 1),
(114, 'Greenwich Village South', 546, 1, 1, 45, 18, 20, 59, 4, 13, 41, 20, 2),
(116, 'Hamilton Heights', 2299, 3, 4, 0, 97, 11, 96, 92, 22, 0, 0, 15),
(120, 'Highbridge Park', 217, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(125, 'Hudson Sq', 475, 1, 0, 18, 0, 0, 0, 0, 0, 0, 37, 0),
(127, 'Inwood', 1350, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(128, 'Inwood Hill Park', 73, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(137, 'Kips Bay', 616, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(140, 'Lenox Hill East', 924, 2, 0, 0, 0, 0, 0, 23, 0, 0, 1, 4),
(141, 'Lenox Hill West', 1291, 2, 0, 0, 0, 0, 1, 0, 0, 6, 0, 0),
(142, 'Lincoln Square East', 1270, 2, 24, 0, 7, 74, 201, 19, 55, 4, 0, 53),
(143, 'Lincoln Square West', 752, 2, 0, 0, 22, 2, 61, 7, 4, 0, 0, 0),
(144, 'Little Italy/NoLiTa', 319, 1, 0, 5, 7, 14, 17, 3, 16, 21, 8, 0),
(148, 'Lower East Side', 941, 2, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0),
(151, 'Manhattan Valley', 1319, 2, 0, 0, 14, 0, 105, 19, 42, 0, 0, 0),
(152, 'Manhattanville', 862, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1),
(153, 'Marble Hill', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(158, 'Meatpacking/West Village West', 1022, 2, 6, 107, 15, 27, 4, 0, 9, 21, 21, 3),
(161, 'Midtown Center', 394, 1, 2, 0, 0, 0, 2, 9, 0, 0, 0, 3),
(162, 'Midtown East', 376, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0),
(163, 'Midtown North', 207, 1, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0),
(164, 'Midtown South', 202, 1, 1, 0, 2, 0, 5, 12, 1, 6, 0, 0),
(166, 'Morningside Heights', 1698, 3, 0, 1, 1, 0, 21, 7, 0, 0, 0, 0),
(170, 'Murray Hill', 1042, 2, 2, 0, 1, 0, 2, 5, 0, 37, 1, 0),
(186, 'Penn Station/Madison Sq West', 130, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(194, 'Randalls Island', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(202, 'Roosevelt Island', 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0),
(209, 'Seaport', 161, 1, 0, 16, 4, 0, 2, 0, 2, 3, 9, 1),
(211, 'SoHo', 373, 1, 0, 6, 4, 46, 42, 6, 3, 12, 12, 0),
(224, 'Stuy Town/Peter Cooper Village', 428, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(229, 'Sutton Place/Turtle Bay North', 1082, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(230, 'Times Sq/Theatre District', 176, 1, 4, 0, 1, 0, 0, 5, 0, 0, 0, 1),
(231, 'TriBeCa/Civic Center', 943, 2, 0, 4, 30, 51, 43, 8, 5, 187, 21, 31),
(232, 'Two Bridges/Seward Park', 935, 2, 1, 2, 1, 0, 0, 2, 0, 0, 4, 0),
(233, 'UN/Turtle Bay South', 704, 2, 0, 0, 0, 0, 0, 1, 0, 4, 0, 0),
(234, 'Union Sq', 409, 1, 0, 15, 10, 9, 8, 82, 9, 44, 0, 105),
(236, 'Upper East Side North', 2205, 3, 38, 1, 41, 63, 78, 45, 59, 17, 1, 42),
(237, 'Upper East Side South', 1875, 3, 65, 0, 16, 104, 9, 66, 33, 74, 0, 86),
(238, 'Upper West Side North', 2183, 3, 9, 0, 64, 16, 435, 33, 80, 2, 0, 64),
(239, 'Upper West Side South', 2114, 3, 6, 0, 156, 101, 496, 40, 130, 6, 0, 63),
(243, 'Washington Heights North', 2410, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(244, 'Washington Heights South', 2695, 5, 1, 0, 29, 0, 13, 5, 0, 0, 0, 2),
(246, 'West Chelsea/Hudson Yards', 794, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(249, 'West Village', 1481, 2, 1, 205, 26, 27, 12, 0, 16, 115, 71, 1),
(261, 'World Trade Center', 89, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3),
(262, 'Yorkville East', 1105, 2, 0, 0, 0, 0, 0, 0, 21, 0, 1, 0),
(263, 'Yorkville West', 1028, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

