import requests
import os
import json
import config

def fetch_weather():
    KEY = config.ACCUWEATHER_API_KEY #os.getenv("ACCUWEATHER_API_KEY")
    CITY_KEY = "287713"  # Cluj-Napoca
    url = f"https://dataservice.accuweather.com/forecasts/v1/daily/1day/{CITY_KEY}?apikey={KEY}&metric=true"
    print(f"[INFO] Forecast URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        forecast = data["DailyForecasts"][0]

        # min_temp = forecast["Temperature"]["Minimum"]["Value"]
        # max_temp = forecast["Temperature"]["Maximum"]["Value"]
        # day_phrase = forecast["Day"]["PrecipitationIntensity"] + " " + forecast["Day"]["IconPhrase"]
        # night_phrase = forecast["Night"]["IconPhrase"]

        day = forecast.get("Day", {})
        day_precip = day.get("PrecipitationIntensity", "")
        day_phrase = day.get("IconPhrase", "")
        day_complete = f"{day_precip} {day_phrase}".strip()

        night = forecast.get("Night", {})
        night_precip = night.get("PrecipitationIntensity", "")
        night_phrase = night.get("IconPhrase", "")
        night_complete = f"{night_precip} {night_phrase}".strip()

        temp = forecast.get("Temperature", {})
        min_temp = temp.get("Minimum", {}).get("Value", "")
        max_temp = temp.get("Maximum", {}).get("Value", "")

        weather_emoji = get_weather_emoji(day_phrase)
        mobile_link = forecast.get("MobileLink", "")

        print(f"[INFO] Day: {day_complete}, Night: {night_complete}")
        print(f"[INFO] Min: {min_temp}°C, Max: {max_temp}°C")

        forecast_summary = (
           f"{weather_emoji}  Weather in Cluj-Napoca today "
           f"🌞 {day_complete}, 🌙 {night_complete}. "
           f"🌡️ 🔺{max_temp}/🔻{min_temp} °C"
           f"🔗 [More details]({mobile_link})"
           
)
        print(f"[INFO] Forecast: {forecast_summary}")

        return forecast_summary
    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return "Weather data unavailable"

def get_weather_emoji(description: str) -> str:
    desc = description.lower()
    if "thunder" in desc:
        return "⛈️"
    elif "rain" in desc or "showers" in desc or "drizzle" in desc:
        return "🌧️"
    elif "snow" in desc or "flurries" in desc:
        return "❄️"
    elif "cloud" in desc:
        return "☁️"
    elif "sun" in desc or "clear" in desc:
        return "☀️"
    elif "fog" in desc or "mist" in desc:
        return "🌫️"
    else:
        return "🌤"
