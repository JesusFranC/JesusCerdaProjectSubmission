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

def profile_dataframe(df: pd.DataFrame):
    print("--- Data Types ---")
    print(df.dtypes)

    # Null or missing rows
    print("\n--- Missing rows ---")
    print(df.isnull().sum())

    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())

    print ("\n--- Data Structure/Head ---")
    print(df.head())

    print("\n--- Summary Statistics ---")
    print(df.describe())

def clean_dataframe(df):
    # Get count of how many rows we started with
    original_rows = len(df)

    # Clean the data of duplicates, nulls, and odd rows (I went a bit over and under the most extreme recorded surface temperatures)
    before = len(df)
    df = df.drop_duplicates()
    if before - len(df):
        print(f"Removed {before - len(df)} duplicate rows")

    before = len(df)
    df = df.dropna()
    if before - len(df):
        print(f"Removed {before - len(df)} null rows")
    
    before = len(df)
    df = df[df["temp_min"] > -140]
    if before - len(df):
        print(f"Removed {before - len(df)} rows with abnormally low temperature")

    before = len(df)
    df = df[df["temp_max"] < 140]
    if before - len(df):
        print(f"Removed {before - len(df)} rows with abnormally high temperature")
    
    before = len(df)
    df = df[df["wind_speed"] >= 0]
    if before - len(df):
        print(f"Removed {before - len(df)} rows with invalid wind speeds")
    
    # Get count of affected rows
    cleaned_rows = len(df)
    print(f"Original row count: {original_rows}")
    print(f"Rows removed:       {original_rows - cleaned_rows}")
    print(f"Rows remaining:     {cleaned_rows}")
    return df