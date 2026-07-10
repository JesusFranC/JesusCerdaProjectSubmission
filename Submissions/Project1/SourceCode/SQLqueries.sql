-- Highest recorded temp for each city
SELECT c.city_name, ROUND(MAX(w.temp_max), 2)
FROM cities as c
JOIN weather_records AS w ON c.city_id = w.city_id
GROUP BY c.city_name;

-- Highest recorded temp for each city per year
SELECT
    c.city_name,
    EXTRACT(YEAR FROM w.record_date) AS year,
    ROUND(MAX(w.temp_max), 2) AS highest_temp
FROM cities c
JOIN weather_records w
    ON c.city_id = w.city_id
GROUP BY
    c.city_name,
    EXTRACT(YEAR FROM w.record_date)
ORDER BY
    c.city_name,
    year;

-- Average precipitation across each month (average total mm per month)
WITH monthly_precipitation AS (
    SELECT
        city_id,
        DATE_TRUNC('month', record_date) AS month,
        SUM(precipitation) AS monthly_total
    FROM weather_records
    GROUP BY city_id, DATE_TRUNC('month', record_date)
)
SELECT
    c.city_name,
    ROUND(AVG(mp.monthly_total), 2) AS avg_monthly_precipitation
FROM monthly_precipitation mp
JOIN cities c
    ON mp.city_id = c.city_id
GROUP BY c.city_name
ORDER BY c.city_name;

-- Windiest week of the year per city (by highest average wind speed)
WITH weekly_wind AS (
    SELECT
        city_id,
        EXTRACT(YEAR FROM record_date) AS year,
        DATE_TRUNC('week', record_date) AS week_start,
        AVG(wind_speed) AS avg_wind_speed
    FROM weather_records
    GROUP BY
        city_id,
        EXTRACT(YEAR FROM record_date),
        DATE_TRUNC('week', record_date)
),
ranked_weeks AS (
    SELECT
        city_id,
        year,
        week_start,
        avg_wind_speed,
        ROW_NUMBER() OVER (
            PARTITION BY city_id, year
            ORDER BY avg_wind_speed DESC
        ) AS rn
    FROM weekly_wind
)
SELECT
    c.city_name,
    rw.year,
    rw.week_start,
    ROUND(rw.avg_wind_speed, 2) AS avg_wind_speed
FROM ranked_weeks rw
JOIN cities c
    ON rw.city_id = c.city_id
WHERE rw.rn = 1
ORDER BY
    c.city_name,
    rw.year;

-- Average rainfall per city
SELECT c.city_name, AVG(w.precipitation)
FROM cities AS c
JOIN weather_records AS w ON c.city_id = w.city_id
GROUP BY city_name;

-- Average Rainfall per city on rainy days
SELECT c.city_name, AVG(w.precipitation)
FROM cities AS c
JOIN weather_records AS w ON c.city_id = w.city_id
WHERE w.precipitation > 0
GROUP BY city_name;

-- Days with extreme heat (Top 10% historically over all of dataset, calculated individually per city)
WITH temp_thresholds AS (
    SELECT
        city_id,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY temp_max) AS extreme_temp
    FROM weather_records
    GROUP BY city_id
)
SELECT
    c.city_name,
    EXTRACT(YEAR FROM w.record_date) AS year,
    COUNT(*) AS extreme_temperature_days
FROM weather_records w
JOIN temp_thresholds t
    ON w.city_id = t.city_id
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.temp_max >= t.extreme_temp
GROUP BY
    c.city_name,
    EXTRACT(YEAR FROM w.record_date)
ORDER BY
    c.city_name,
    year;

-- Days with extreme cold(Bottom 10% historically over all of dataset, calculated individually per city)
WITH temp_thresholds AS (
    SELECT
        city_id,
        PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY temp_min) AS extreme_cold
    FROM weather_records
    GROUP BY city_id
)
SELECT
    c.city_name,
    EXTRACT(YEAR FROM w.record_date) AS year,
    COUNT(*) AS extreme_cold_days
FROM weather_records w
JOIN temp_thresholds t
    ON w.city_id = t.city_id
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.temp_min <= t.extreme_cold
GROUP BY
    c.city_name,
    EXTRACT(YEAR FROM w.record_date)
ORDER BY
    c.city_name,
    year;

-- Days with extreme wind (Top 10% historically over all of dataset, calculated individually per city)
WITH wind_thresholds AS (
    SELECT
        city_id,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY wind_speed) AS extreme_wind
    FROM weather_records
    GROUP BY city_id
)
SELECT
    c.city_name,
    EXTRACT(YEAR FROM w.record_date) AS year,
    COUNT(*) AS extreme_wind_days
FROM weather_records w
JOIN wind_thresholds t
    ON w.city_id = t.city_id
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.wind_speed >= t.extreme_wind
GROUP BY
    c.city_name,
    EXTRACT(YEAR FROM w.record_date)
ORDER BY
    c.city_name,
    year;