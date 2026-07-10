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
    # Time how long everything takes
    total_time_start = time.time()
    client = OpenMeteoClient()

    frames = []
    for city, lat, lon in cities:
        # Catching errors if present
        try:
            start_date = "2000-01-01"
            end_date = "2026-01-01"
            start = time.time()
            weather = client.fetch(
                lat,
                lon,
                start_date,
                end_date
            )
            end = time.time()
            print(f"{city} weather data from {start_date} to {end_date} took {end-start:.4f} seconds to retrieve")
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
    
    print("\n")
    # Gather all frames, profile them (output to command line, then cleans odd or bad data)
    df = pd.concat(frames, ignore_index=True)
    profile_dataframe(df)
    df = clean_dataframe(df) # Note: this also prints the head
    
    print("\n")
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
    
    # Clearing old data from DB
    start = time.time()
    dg.clearValuesFromDB()
    end = time.time()
    print(f"Clearing the db took {end-start:.4f} seconds")
    
    # Clocking Performance
    start = time.time()
    dg.addToPostgresDB(cities=cities, df= df)
    end = time.time()
    print (f"Loading the db took {end - start:.4f} seconds")

    ## Previous version performance
    #start = time.time()
    #dg.addToPostgresDGOneByOne(cities=cities, df= df)
    #end = time.time()
    #print (f"The slower operation took {end - start:.4f} seconds")

    total_time_end = time.time()
    print(f"\nThe total execution time of this program is {total_time_end - total_time_start:.4f}")

if __name__ == "__main__":
    main()