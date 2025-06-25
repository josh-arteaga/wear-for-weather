# filepath: backend/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from backend.weather import fetch_weather
from backend.ollama_client import outfit_rec
import os

load_dotenv(dotenv_path="../.env")  # Loads variables from your .env file

app = FastAPI()

@app.get("/")
def read_root():
    weather_api_key = os.getenv("WEATHER_API_KEY")
    return {"message": "FastAPI is running!", "weather_api_key": weather_api_key}