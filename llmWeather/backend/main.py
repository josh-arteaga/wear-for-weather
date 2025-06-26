# filepath: backend/main.py
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from backend.weather import fetch_weather
from backend.ollama_client import outfit_rec
import os

load_dotenv(dotenv_path="../.env")  # Loads variables from your .env file

app = FastAPI()

@app.get("/")
async def read_root(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    hours: int = Query(12, description="Number of forecasted hours")
):
    # Get weather data
    weather_data = await fetch_weather(lat, lon, hours)
    # Get outfit rec from LLM
    outfit = await outfit_rec(weather_data)
    # Return the resulting message
    return {
        "location": {"lat": lat,"lon": lon},
        "hours": hours,
        "outfit_recommendation": outfit
    }