# ============================================================
#  Snap-to-Caption  —  AI-Powered Image-to-Text (Part 1)
# ============================================================
from config import HF_API_KEY
import requests, base64, os, re
from PIL import Image
from colorama import init, Fore, Style

# Automatically reset color after each print
init(autoreset=True)

# ── API Setup ───────────────────────────────────────────────
ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS    = {"Authorization": f"Bearer {HF_API_KEY}",
              "Content-Type": "application/json"}

# ── Vision Models (can understand images) ───────────────────
# Note: Kimi-K2.6 is a reasoning model — it puts its answer in
# "reasoning_content" instead of "content", so we handle that separately.
VISION_MODELS = [
    "moonshotai/Kimi-K2.6:novita",
    "meta-llama/Llama-4-Scout-17B-16E-Instruct:novita",
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct:novita",
]

# ── Text Models (can rewrite / expand text) ─────────────────
TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mistral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
]


# ── Helper: Convert image file to base64 string ─────────────
# The API cannot receive a file directly, so we convert it to
# a base64 encoded string that can be sent inside JSON.
def image_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


# ── Helper: Send a request to the HuggingFace API ───────────
# Returns (response_data, error_message).
# If the request succeeds, error_message is None.
# If it fails, response_data is None and error_message explains why.
def call_api(payload: dict):
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS,
                          json=payload, timeout=120)
    except requests.RequestException as e:
        return None, f"Request failed: {e}"

    # If status is not 200 OK, extract the error message
    if r.status_code != 200:
        try:
            msg = r.json().get("error", {}).get("message") or r.text
        except Exception:
            msg = r.text or "Unknown error"
        return None, f"Status {r.status_code}: {msg}"

    # Parse and return the JSON response
    try:
        return r.json(), None
    except Exception:
        return None, "Received a non-JSON response from the API."


# ── Helper: Extract the text content from API response ───────
# The API returns a nested JSON. This function digs into it
# and returns just the text string the model generated.
# Some reasoning models (like Kimi-K2.6) return an empty "content"
# and put the answer in "reasoning_content" instead — we check both.
def get_text(data) -> str:
    msg = (data or {}).get("choices", [{}])[0].get("message", {})
    # First try the normal "content" field
    text = (msg.get("content") or "").strip()
    if text:
        return text
    # Fallback: reasoning models store answer in "reasoning_content"
    return (msg.get("reasoning_content") or "").strip()


# ── Helper: Try multiple models until one works ──────────────
# If a model fails or returns empty text, we move on to the next one.
# Returns (text, error). If all models fail, returns (None, error).
def try_models(models, messages, max_tokens=160):
    for model in models:
        data, err = call_api({
            "model":       model,
            "messages":    messages,
            "max_tokens":  max_tokens,
            "temperature": 0.3,   # lower = more focused output
        })
        if err:
            continue  # this model failed, try the next one
        text = get_text(data)
        if text:
            return text, None  # success!
    return None, "All models failed."


# ── Step 1: Send image to a Vision model and get a caption ───
# The vision model looks at the image and writes one sentence
# describing what it sees.
def get_basic_caption(image_path: str):
    print(f"{Fore.YELLOW}🖼️  Analyzing image...")

    # Build the message with both text instruction and the image
    messages = [{
        "role": "user",
        "content": [
            {"type": "text",
             "text": "Write one short sentence describing what is in this image."},
            {"type": "image_url",
             "image_url": {"url": image_to_base64(image_path)}},
        ],
    }]

    caption, err = try_models(VISION_MODELS, messages, max_tokens=80)

    if err:
        return None, err
    return caption, None


# ── Step 2: Expand the caption into exactly 30 words ─────────
# We send the basic caption to a text model and ask it to
# rewrite it as a 30-word description.
def expand_to_30_words(caption: str):
    print(f"{Fore.YELLOW}✍️  Generating description...")

    prompt = (
        "Rewrite the following sentence as EXACTLY 30 words. "
        "Write only one paragraph. End with a period. "
        "Do not add any title, bullet points, or extra text.\n\n"
        f"Sentence: {caption}"
    )

    messages = [{"role": "user", "content": prompt}]

    result, err = try_models(TEXT_MODELS, messages, max_tokens=120)

    if err:
        return None, err

    # Safety check: trim to 30 words in case the model returned more
    words = result.split()
    final = " ".join(words[:30])
    if not final.endswith("."):
        final += "."

    return final, None


# ── Main function: ties everything together ──────────────────
def main():

    # Step 1: Ask the user for the image path
    image_path = input(
        f"{Fore.BLUE}📁 Enter the image path (e.g. cat.jpg): {Style.RESET_ALL}"
    ).strip()

    # Check if the file actually exists on disk
    if not os.path.exists(image_path):
        print(f"{Fore.RED}❌ File not found: '{image_path}'")
        return

    # Check if the file is a valid image that PIL can open
    try:
        Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}❌ Could not open image: {e}")
        return

    # Step 2: Generate the basic caption
    caption, err = get_basic_caption(image_path)

    if err:
        print(f"{Fore.RED}❌ Failed to generate caption: {err}")
        return

    # Show the basic caption to the user
    print(f"\n{Fore.GREEN}✅ Basic Caption:{Style.RESET_ALL} {Fore.YELLOW}{caption}\n")

    # Step 3: Ask the user if they want a 30-word description
    choice = input(
        f"{Fore.CYAN}❓ Do you want to expand this into a 30-word description? (yes/no): {Style.RESET_ALL}"
    ).strip().lower()

    if choice in ("yes", "y"):
        # Step 4: Expand the caption into 30 words
        description, err = expand_to_30_words(caption)

        if err:
            print(f"{Fore.RED}❌ Failed to generate description: {err}")
        else:
            print(f"\n{Fore.GREEN}✅ Description (30 words):{Style.RESET_ALL} "
                  f"{Fore.YELLOW}{description}\n")
    else:
        # User said no — just keep the basic caption
        print(f"\n{Fore.GREEN}👋 Okay! Keeping just the basic caption.")


# ── Entry point: run main() when script is executed ──────────
if __name__ == "__main__":
    main()