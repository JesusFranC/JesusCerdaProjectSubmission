from meteoWeatherApi import OpenMeteoClient
from cleanweather import flatten_weather, profile_dataframe, clean_dataframe
import pandas as pd
import requests
from postgresCrudDAO import genericDao
from project1DataGateway import dfToGateway
import time

cities = [("Long Beach", 33.7767, -118.1892),
          ("Monterey", 36.6002, -121.8947),
          ("Pacifica", 37.6138, -122.4869)]

def main():
    client = OpenMeteoClient()

    frames = []
    for city, lat, lon in cities:
        # Catching errors if present
        try:
            weather = client.fetch(
                lat,
                lon,
                "2020-01-01",
                "2026-07-01"
            )
            # Flatten
            frames.append(flatten_weather(city, weather))
        
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error while fetching weather for {city}:")
            print(e)
            continue

        except requests.exceptions.RequestException as e:
            print(f"Request failed while fetching weather for {city}:")
            print(e)
            continue
    
    # Early exit if the api failed
    if not frames:
        print("No weather data was successfully retrieved.")
        return
    
    # Gather all frames, profile them (output to command line, then cleans odd or bad data)
    df = pd.concat(frames, ignore_index=True)
    profile_dataframe(df)
    df = clean_dataframe(df) # Note: this also prints the head

    # Load to DB
    host = "localhost"
    port = 5432
    database = "WeatherData"
    user = "postgres"      # TODO: implement from ENV, or Fill in yourself before executing
    password = "password"  # TODO: implement from ENV, or Fill in yourself before executing

    conn_string = (
        f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )
    dao = genericDao(conn_string= conn_string)
    dg = dfToGateway(dao= dao)

    print("\n")
    # Clocking Performance
    start = time.time()
    dg.addToPostgresDB(cities=cities, df= df)
    end = time.time()
    print (f"The improved operation took {end - start:.4f} seconds")
    dg.clearValuesFromDB()

    ## Previous version performance
    #start = time.time()
    #dg.addToPostgresDGOneByOne(cities=cities, df= df)
    #end = time.time()
    #print (f"The slower operation took {end - start:.4f} seconds")
    
    start = time.time()
    dg.clearValuesFromDB()
    end = time.time()
    print(f"Clearing the db takes {end-start:.4f} seconds")


if __name__ == "__main__":
    main()