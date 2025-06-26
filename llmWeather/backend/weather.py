# backend/weather.py
import httpx, os
from typing import List, Dict

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL= "https://api.weatherapi.com/v1/forecast.json" # Base API endpoint

_client = httpx.AsyncClient(timeout=10)

async def fetch_weather(lat: float, lon: float, hours: int = 72) -> List[Dict]:
    params = {
        "q": f"{lat},{lon}",
        "days": 3,
        "aqi": "no",
        "alerts": "no",
    }

    try:
        r = await _client.get(BASE_URL, params=params)
        r.raise_for_status()
        data = r.json()

    # Flatten -> grab the 'hours' entries starting from 'now'
        hourly = []
        for day in data["forecast"]["forecastday"]:
            hourly.extend(day["hour"])
        return hourly[:hours]

    except httpx.HTTPError as e:
        raise RuntimeError(f"Weather API call failed: {e}") from e


#   async with httpx.AsyncClient(timeout=10) as client:
#       r = await client.get(BASE, params=params)         # await is special with async functions, can start/stop functions once started
#       r.raise_for_status()
#       data = r.json()
#       return data["forecast"]["forecastday"][0]["hour"][:hours]   # only prints back the hours specified on line 5
#       # the rest of this data is from a python dictionary generated for the machines talking. 
