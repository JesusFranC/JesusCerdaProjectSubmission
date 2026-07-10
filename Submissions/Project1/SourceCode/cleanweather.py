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
    print("\n--- Missing/Null value rows ---")
    print(df.isnull().sum())

    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())

    print ("\n--- Data Structure/Head ---")
    print(df.head())

    print("\n--- Missing Dates by City ---")
    for city in df["city"].unique():
        city_df = df[df["city"] == city]
        
        expected_dates = pd.date_range(
            start=city_df["date"].min(),
            end=city_df["date"].max(),
            freq="D"
        )

        missing_dates = expected_dates.difference(city_df["date"])

        print(f"\n{city}:")
        print(f"Expected days: {len(expected_dates)}")
        print(f"Actual days:   {len(city_df)}")
        print(f"Missing days:  {len(missing_dates)}")

        if len(missing_dates) > 0:
            print("Missing dates:")
            print(missing_dates)

    print("\n--- Data Size ---")
    bytes_used = df.memory_usage(deep=True).sum()
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(bytes_used)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            print(f"DataFrame size: {size:.2f} {unit}")
            break
        size /= 1024

    #print("\n--- Summary Statistics ---")
    #print(df.describe())

def clean_dataframe(df):
    print("--- Data Cleaning ---")
    
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