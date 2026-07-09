from meteoWeatherApi import OpenMeteoClient
from cleanweather import flatten_weather, profile_dataframe, clean_dataframe
import pandas as pd
import requests

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

    # Store to DB

if __name__ == "__main__":
    main()