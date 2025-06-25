# backend/weather.py
import httpx, os
BASE = "https://api.weatherapi.com/v1/forecast.json" # Base API endpoint

async def fetch_weather(lat: float, lon: float, hours: int = 12):
    params = {
        "key": os.getenv("WEATHER_API_KEY"),            # param keys set by API endpoint
        "q": f"{lat},{lon}",
        "days": 3,
        "aqi": "no",
        "alerts": "no",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(BASE, params=params)         # await is special with async functions, can start/stop functions once started
        r.raise_for_status()
        data = r.json()
        return data["forecast"]["forecastday"][0]["hour"][:hours]   # only prints back the hours specified on line 5
        # the rest of this data is from a python dictionary generated for the machines talking. 
