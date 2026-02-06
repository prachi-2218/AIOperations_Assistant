import os
import requests
from utils.cache import cached_function

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@cached_function(ttl_seconds=300)  # Cache for 5 minutes
def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    return {
        "city": city,
        "temp_c": data["main"]["temp"],
        "condition": data["weather"][0]["description"]
    }
