# filepath: backend/main.py
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.weather import fetch_weather, _client as weather_client
from backend.ollama_client import outfit_rec, _client as ollama_client
import os

load_dotenv(dotenv_path="../.env")  # Loads variables from your .env file

app = FastAPI()
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],  # Allows all origins (dev only)
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
 )

@app.get("/weather")
async def get_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    hours: int = Query(12, ge=1, le=72, description="Number of forecasted hours")
):
    try:
        hourly_slice = await fetch_weather(lat, lon, hours)
    except RuntimeError as e:
        # Weather provider flaked out → surface a 503 to caller
        raise HTTPException(status_code=503, detail=str(e)) from e

    try:
        rec = await outfit_rec(hourly_slice)
    except RuntimeError as e:
        # Ollama isn’t running or prompt failed
        raise HTTPException(status_code=502, detail=str(e)) from e

    return {
        "location": {"lat": lat, "lon": lon},
        "hours": hours,
        "outfit_recommendation": rec,
    }

@app.post("/recommend")
async def recommend_outfit(request: Request):
    try:
        body = await request.json()
        weather_data = body.get("weather", [])

        if not weather_data:
            raise HTTPException(status_code=400, detail="No weather data provided in request body")
            
        rec = await outfit_rec(weather_data)
        return {"outfit": rec}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Uncomment and configure CORS middleware as needed
