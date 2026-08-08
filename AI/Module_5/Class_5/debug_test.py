# ── Debug Script: Find out exactly why models are failing ────
from config import HF_API_KEY
import requests, base64

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS    = {"Authorization": f"Bearer {HF_API_KEY}",
              "Content-Type": "application/json"}

VISION_MODELS = [
    "moonshotai/Kimi-K2.6:novita",
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",
    "meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova",
]

# Convert image to base64
image_path = input("Enter image path: ").strip()
with open(image_path, "rb") as f:
    data_url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe this image in one sentence."},
        {"type": "image_url", "image_url": {"url": data_url}},
    ],
}]

# Try each model and print the EXACT error
for model in VISION_MODELS:
    print(f"\n⏳ Trying: {model}")
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS, json={
            "model": model,
            "messages": messages,
            "max_tokens": 80,
            "temperature": 0.3,
        }, timeout=120)
        print(f"   Status: {r.status_code}")
        print(f"   Response: {r.text[:300]}")  # show first 300 chars
    except Exception as e:
        print(f"   Exception: {e}")