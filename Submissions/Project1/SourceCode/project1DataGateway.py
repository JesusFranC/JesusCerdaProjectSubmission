from postgresCrudDAO import genericDao

class dfToGateway:
    def __init__(self, dao:genericDao):
        self.dao = dao
    
    def addToPostgresDGOneByOne(self, cities, df):
        city_ids = {}

        # Insert cities and retrieve IDs
        for city_name, latitude, longitude in cities:
            sql = """
                INSERT INTO cities (
                    city_name,
                    latitude,
                    longitude
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (city_name)
                DO UPDATE SET
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude
                RETURNING city_id;
            """

            result = self.dao.get_one(
                sql,
                (city_name, latitude, longitude)
            )
            city_ids[city_name] = result[0]

        # Insert weather records
        sql = """
            INSERT INTO weather_records (
                city_id,
                record_date,
                temp_max,
                temp_min,
                precipitation,
                wind_speed
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (city_id, record_date)
            DO UPDATE SET
                temp_max = EXCLUDED.temp_max,
                temp_min = EXCLUDED.temp_min,
                precipitation = EXCLUDED.precIPITATION,
                wind_speed = EXCLUDED.wind_speed;
        """

        for _, row in df.iterrows():
            self.dao.execute(
                sql,
                (
                    city_ids[row["city"]],
                    row["date"],
                    row["temp_max"],
                    row["temp_min"],
                    row["precipitation"],
                    row["wind_speed"]
                )
            )
    
    def addToPostgresDB(self, cities, df):
        city_ids = {}

        # Insert cities and retrieve IDs
        for city_name, latitude, longitude in cities:
            sql = """
                INSERT INTO cities (
                    city_name,
                    latitude,
                    longitude
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (city_name)
                DO UPDATE SET
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude
                RETURNING city_id;
            """

            result = self.dao.get_one(
                sql,
                (city_name, latitude, longitude)
            )

            city_ids[city_name] = result[0]

        # Prepare weather records for batch insert
        sql = """
            INSERT INTO weather_records (
                city_id,
                record_date,
                temp_max,
                temp_min,
                precipitation,
                wind_speed
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (city_id, record_date)
            DO UPDATE SET
                temp_max = EXCLUDED.temp_max,
                temp_min = EXCLUDED.temp_min,
                precipitation = EXCLUDED.precipitation,
                wind_speed = EXCLUDED.wind_speed;
        """

        weather_records = []

        for _, row in df.iterrows():
            weather_records.append(
                (
                    city_ids[row["city"]],
                    row["date"],
                    row["temp_max"],
                    row["temp_min"],
                    row["precipitation"],
                    row["wind_speed"]
                )
            )

        inserted = self.dao.execute_many(sql, weather_records)

        #print(f"Inserted/updated {inserted} weather records")
        #print(f"Processed {len(city_ids)} cities")

    # TODO: These queries, and more, are written in my SQLqueries.sql file in this repository
    # In order to speed up development time, I have opted not to write these into the python program here, and just execute the queries in pgAdmin
    def queryHighestTemp(self):
        pass

    def queryTotalMontlyPrecipitation(self):
        pass

    def queryWindiestWeekOfTheYear(self):
        pass

    def queryAverageRainfallPerCity(self):
        pass

    def queryFrequencyOfExtremeTemps(self):
        pass

    def clearValuesFromDB(self):
        sql = "TRUNCATE TABLE cities RESTART IDENTITY CASCADE"
        self.dao.execute(sql, ())