import requests

class OpenMeteoClient:
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    def fetch(self, lat, lon, start_date, end_date):
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/Los_Angeles"
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        return response.json()