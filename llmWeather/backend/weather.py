# backend/weather.py
import httpx, os
from typing import List, Dict
from dotenv import load_dotenv
from pathlib import Path

# Only load .env if not already loaded (prevents double-loading)
if not os.getenv("WEATHER_API_KEY"):
    dotenv_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=dotenv_path)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise RuntimeError("WEATHER_API_KEY not in .env file or environment")
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"
_client = httpx.AsyncClient(timeout=10)

async def fetch_weather(lat: float, lon: float, hours: int = 72) -> List[Dict]:
    params = {
        "lat": lat,
        "lon": lon,
        "units": "imperial",  # or "metric" for Celsius
        "appid": WEATHER_API_KEY,
        "exclude": "minutely,daily,alerts"  # Only get hourly data
    }

    r = await _client.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()

    # Flatten -> grab the 'hours' entries starting from 'now''
    return data["hourly"][:hours]  # OpenWeather's hourly data is already flattened

# except httpx.HTTPError as e:
# raise RuntimeError(f"Weather API call failed: {e}") from e


#   async with httpx.AsyncClient(timeout=10) as client:
#       r = await client.get(BASE, params=params)         # await is special with async functions, can start/stop functions once started
#       r.raise_for_status()
#       data = r.json()
#       return data["forecast"]["forecastday"][0]["hour"][:hours]   # only prints back the hours specified on line 5
#       # the rest of this data is from a python dictionary generated for the machines talking.
