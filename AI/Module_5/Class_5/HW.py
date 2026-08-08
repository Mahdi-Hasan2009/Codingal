# ============================================================
#  Snap-to-Caption  —  AI-Powered Image-to-Text (Part 1)
# ============================================================
from config import HF_API_KEY
import requests, base64, os, re
from PIL import Image
from colorama import init, Fore, Style

init(autoreset=True)

# ── API সেটআপ ──────────────────────────────────────────────
ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS    = {"Authorization": f"Bearer {HF_API_KEY}",
              "Content-Type": "application/json"}

# ── মডেল লিস্ট ─────────────────────────────────────────────
VISION_MODELS = [
    "moonshotai/Kimi-K2.6:novita",
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",
    "meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova",
]

TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mistral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
]


# ── Helper: ছবিকে base64 এ বদলাও ──────────────────────────
def image_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


# ── Helper: API তে request পাঠাও ───────────────────────────
def call_api(payload: dict):
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS,
                          json=payload, timeout=120)
    except requests.RequestException as e:
        return None, f"Request failed: {e}"

    if r.status_code != 200:
        try:
            msg = r.json().get("error", {}).get("message") or r.text
        except Exception:
            msg = r.text or "Unknown error"
        return None, f"Status {r.status_code}: {msg}"

    try:
        return r.json(), None
    except Exception:
        return None, "API থেকে ভুল response এলো।"


# ── Helper: API response থেকে text বের করো ─────────────────
def get_text(data) -> str:
    msg = (data or {}).get("choices", [{}])[0].get("message", {})
    return (msg.get("content") or "").strip()


# ── Helper: একাধিক মডেল try করো, যেটা কাজ করে সেটা নাও ──
def try_models(models, messages, max_tokens=160):
    for model in models:
        data, err = call_api({
            "model":       model,
            "messages":    messages,
            "max_tokens":  max_tokens,
            "temperature": 0.3,
        })
        if err:
            continue
        text = get_text(data)
        if text:
            return text, None
    return None, "সব মডেল ব্যর্থ হয়েছে।"


# ── Step 1: ছবি দেখে basic caption বানাও ───────────────────
def get_basic_caption(image_path: str) -> str:
    print(f"{Fore.YELLOW}🖼️  ছবি বিশ্লেষণ করা হচ্ছে...")

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


# ── Step 2: caption কে ৩০ শব্দে expand করো ────────────────
def expand_to_30_words(caption: str) -> str:
    print(f"{Fore.YELLOW}✍️  Description তৈরি করা হচ্ছে...")

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

    # ৩০ শব্দ নিশ্চিত করো
    words = result.split()
    final = " ".join(words[:30])
    if not final.endswith("."):
        final += "."

    return final, None


# ── Main: সব কিছু একসাথে চালাও ────────────────────────────
def main():

    # ── ছবির path নাও ──
    image_path = input(
        f"{Fore.BLUE}📁 ছবির path দাও (যেমন: cat.jpg): {Style.RESET_ALL}"
    ).strip()

    # ── ফাইল আছে কিনা চেক করো ──
    if not os.path.exists(image_path):
        print(f"{Fore.RED}❌ ফাইল পাওয়া যায়নি: '{image_path}'")
        return

    # ── ছবি খোলা যায় কিনা চেক করো ──
    try:
        Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}❌ ছবি খোলা যায়নি: {e}")
        return

    # ── Step 1: Basic Caption ──
    caption, err = get_basic_caption(image_path)

    if err:
        print(f"{Fore.RED}❌ Caption তৈরি করা সম্ভব হয়নি: {err}")
        return

    print(f"\n{Fore.GREEN}✅ Basic Caption:{Style.RESET_ALL} {Fore.YELLOW}{caption}\n")

    # ── Step 2: Expand করতে চাও? ──
    choice = input(
        f"{Fore.CYAN}❓ এটাকে ৩০ শব্দে বড় করতে চাও? (yes/no): {Style.RESET_ALL}"
    ).strip().lower()

    if choice in ("yes", "y", "হ্যাঁ", "ha"):
        description, err = expand_to_30_words(caption)

        if err:
            print(f"{Fore.RED}❌ Description তৈরি করা সম্ভব হয়নি: {err}")
        else:
            print(f"\n{Fore.GREEN}✅ Description (30 words):{Style.RESET_ALL} "
                  f"{Fore.YELLOW}{description}\n")
    else:
        print(f"\n{Fore.GREEN}👋 ঠিক আছে! শুধু caption রাখা হলো।")


# ── চালু করো ───────────────────────────────────────────────
if __name__ == "__main__":
    main()