import pandas as pd

def flatten_weather(city_name, json_data):
    daily = json_data["daily"]

    df = pd.DataFrame({
        "city": city_name,
        "date": daily["time"],
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "precipitation": daily["precipitation_sum"],
        "wind_speed": daily["wind_speed_10m_max"]
    })

    # basic cleaning
    df["date"] = pd.to_datetime(df["date"])

    return df