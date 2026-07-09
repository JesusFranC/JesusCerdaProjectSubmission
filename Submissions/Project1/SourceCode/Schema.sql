CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL
);

CREATE TABLE weather_records (
    city_id INTEGER NOT NULL,
    record_date DATE NOT NULL,
    temp_max DECIMAL(5,2) NOT NULL,
    temp_min DECIMAL(5,2) NOT NULL,
    precipitation DECIMAL(8,2) NOT NULL,
    wind_speed DECIMAL(6,2) NOT NULL,

    PRIMARY KEY (city_id, record_date),
    FOREIGN KEY (city_id) REFERENCES cities(city_id),

    CHECK (temp_max >= temp_min),
    CHECK (wind_speed >= 0),
    CHECK (precipitation >= 0)
);