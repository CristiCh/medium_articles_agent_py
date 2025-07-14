import requests
import os
import json

def fetch_weather():
    # This is illustrative; replace with a real AccuWeather API key & endpoint
    KEY = os.getenv("ACCUWEATHER_API_KEY")
    CITY_KEY = "287713"  # Cluj-Napoca
    url = f"https://dataservice.accuweather.com/forecasts/v1/daily/1day/{CITY_KEY}?apikey={KEY}"
    print(f"[INFO] Final AccuWeather URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[0]
        # desc = data["WeatherText"]
        # temp = data["Temperature"]["Metric"]["Value"]
        headline_text = data["Headline"]["Text"]
        max_temp_f = data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"]
        max_temp_c = (max_temp_f - 32) * 5 / 9
        return f"{headline_text}, {max_temp_c:.1f}°C"
    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return "Weather data unavailable"
