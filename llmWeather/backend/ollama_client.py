# backend/ollama_client.py
import os, json, httpx
from typing import List, Dict

# Configure the LLM
OLLAMA_URL  = os.getenv("OLLAMA_URL",  "http://localhost:11434/api/generate")
MODEL       = os.getenv("OLLAMA_MODEL", "llama3")

# Re-use a single HTTP client (faster, fewer sockets)
_client = httpx.AsyncClient(timeout=30)

# System Prompt given to LLM each time API endpoint returns a response
PROMPT_TMPL = """
You are WardrobeGPT, an informal yet professional stylist for urban commuters.

Rules:
1️⃣ Return exactly two sentences.
    - Outfit advice (<120 characters)
    - Accessories  (<60 characters)
2️⃣ Be gender-inclusive.
3️⃣ No hashtags and only sparse emojis.

Weather JSON (next 12 hours):
{weather}
"""

# Plan B of pre-set responses in case the LLM call freaks out
def simple_rule_based(hourly_slice: List[Dict]) -> str:
    """
    Deterministic backup if the LLM call fails.

    Args:
        hourly_slice: first 12-hour chunk of WeatherAPI `hour` data.

    Returns:
        Two sentences (outfit + accessory).
    """
    temps     = [h["temp"] for h in hourly_slice]
    avg_temp  = sum(temps) / len(temps)
    raining   = any(h.get("will_it_rain") for h in hourly_slice)

    if raining:
        outfit = "Light rain jacket and waterproof shoes."
        gear   = "Pack a compact umbrella."
    elif avg_temp < 50:
        outfit = "Warm coat, scarf, and gloves."
        gear   = "Thermal layer recommended."
    elif avg_temp < 70:
        outfit = "Long-sleeve shirt or light sweater."
        gear   = "Layer up—mornings are cool."
    else:
        outfit = "T-shirt and breathable shorts."
        gear   = "Bring sunglasses and stay hydrated."

    return f"{outfit} {gear}"

# LLM call is made
async def outfit_rec(hourly: List[Dict]) -> str:
    """
    Ask the local Ollama model for a two-sentence wardrobe blurb.
    Falls back to rule-based logic on any HTTP / JSON error.
    """
    prompt = PROMPT_TMPL.format(weather=json.loads(json.dumps(hourly[:12], indent=2)))

    try:
        resp = await _client.post(
            OLLAMA_URL,
            json={
                "model" : MODEL,
                "prompt": prompt,
                "stream": False  # simpler—wait for full response
            },
        )
        resp.raise_for_status()
        blurb = resp.json()["response"].strip()
    except (httpx.HTTPError, KeyError, ValueError):
        blurb = simple_rule_based(hourly[:12])   # <- fallback

    return blurb
