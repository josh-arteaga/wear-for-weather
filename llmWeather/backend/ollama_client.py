# backend/ollama_client.py
import os, httpx, asyncio

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate") # this is the default server local ollama models will run on
MODEL = os.getenv("OLLAMA_MODEL", "llama3")

async def outfit_rec(hourly):
    prompt = (
        "You're an urban commuter who is planning their day, Given this weather forecast JSON (next 12h), "
        "(provide recommendations for both genders) reply : what should I wear?\n\n"
        f"{hourly}"
    )
    async with httpx.AsyncClient(timeout=None) as c:
        r = await c.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt})  # await tells the program to wait for the server response before moving on
        r.raise_for_status()
        return r.json()["response"].strip()
