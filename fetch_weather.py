import requests
import os

def fetch_weather():
    # This is illustrative; replace with a real AccuWeather API key & endpoint
    KEY = os.getenv("ACCUWEATHER_API_KEY")
    CITY_KEY = "287713"  # Cluj-Napoca
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{CITY_KEY}?apikey={KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[0]
        desc = data["WeatherText"]
        temp = data["Temperature"]["Metric"]["Value"]
        return f"{desc}, {temp:.1f}°C"
    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return "Weather data unavailable"