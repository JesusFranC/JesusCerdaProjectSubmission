from meteoWeatherApi import OpenMeteoClient
from cleanweather import flatten_weather, profile_dataframe, clean_dataframe
import pandas as pd

cities = [("Long Beach", 33.7767, -118.1892),
          ("Monterey", 36.6002, -121.8947),
          ("Pacifica", 37.6138, -122.4869)]

def main():
    client = OpenMeteoClient()

    frames = []
    for city, lat, lon in cities:
        weather = client.fetch(
            lat,
            lon,
            "2020-01-01",
            "2026-12-31"
        )
        # Flatten
        frames.append(flatten_weather(city, weather))
    
    # Gather all frames, profile them (output to command line, then cleans odd or bad data)
    df = pd.concat(frames, ignore_index=True)
    profile_dataframe(df)
    df = clean_dataframe(df)

    # Get the head
    print(df.head())

if __name__ == "__main__":
    main()