# ============================ PART 1 ============================
from config import HF_API_KEY
import requests, base64, os, re, time, json
from datetime import datetime
from PIL import Image
from colorama import init, Fore, Style

init(autoreset=True)

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}   # supported image formats

VISION_MODELS = [
    # --- novita ---
    "moonshotai/Kimi-K2.6:novita",
    # --- together (vision capable) ---
    "Qwen/Qwen3-VL-8B-Instruct:together",
    "google/gemma-4-31B-it:together",
    "moonshotai/Kimi-K2.5:together",
    "Qwen/Qwen3.5-9B:together",
    "Qwen/Qwen3.5-397B-A17B:together",
    "meta-llama/Llama-Guard-4-12B:together",
    # --- sambanova (last resort) ---
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",
]

TEXT_MODELS = [
    # --- together ---
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mistral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
    "meta-llama/Llama-3.3-70B-Instruct:together",
    # --- sambanova (fast text models) ---
    "meta-llama/Llama-3.3-70B-Instruct:sambanova",
    "openai/gpt-oss-120b:sambanova",
]


def _data_url(path: str) -> str:                                 # unchanged from original
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")


def query_hf_api(payload: dict):                                 # unchanged from original
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS, json=payload, timeout=120)
    except requests.RequestException as e:
        return None, f"Request failed: {e}"
    if r.status_code != 200:
        try:
            j = r.json()
            msg = j.get("error", {}).get("message") or str(j)
        except Exception:
            msg = (r.text or "").strip() or r.reason or "Request failed."
        return None, f"Status {r.status_code}: {msg}"
    try:
        return r.json(), None
    except Exception:
        return None, "Non-JSON response received from the API."


def _extract_text(data) -> str:                                  # unchanged from original
    msg = (data or {}).get("choices", [{}])[0].get("message", {}) or {}
    return (msg.get("content") or "").strip()


def _run_models(models, messages, max_tokens=160, temperature=0.3):  # unchanged from original
    last_err = None
    for model in models:
        data, err = query_hf_api({"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature})
        if err:
            last_err = err
            continue
        out = _extract_text(data)
        if out:
            return out, None
        last_err = "Empty response from model."
    return None, last_err or "All models failed."


def _words(text: str):                                           # unchanged from original
    return re.findall(r"\S+", (text or "").strip())


def _exact_n_words(text: str, n: int) -> str:                   # unchanged from original
    return " ".join(_words(text)[:n])


def _ensure_sentence_end(text: str) -> str:                     # unchanged from original
    t = (text or "").strip()
    if t and t[-1] not in ".!?":
        t += "."
    return t


# ============================ PART 2 (PASTE INTO PART 1) ============================
# Paste this block by REPLACING the two stub functions in Part 1:
# - generate_text(...)
# - generate_exact_sentence(...)

def generate_text(prompt: str, max_new_tokens: int = 220) -> str:   # unchanged from original
    msgs = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    out, err = _run_models(
        TEXT_MODELS,
        msgs,
        max_tokens=max_new_tokens,
        temperature=0.3
    )

    if out:
        return out

    raise Exception(err or "Text generation failed.")


def generate_exact_sentence(prompt: str, n_words: int, max_new_tokens: int, tries: int = 6) -> str:  # unchanged from original
    for _ in range(tries):

        strict_prompt = f"""
{prompt}

IMPORTANT RULES:
- Write EXACTLY {n_words} words.
- One sentence only.
- No title.
- No bullets.
- No numbering.
- End with a period.
"""

        text = generate_text(strict_prompt, max_new_tokens=max_new_tokens)

        words = _words(text)

        if len(words) == n_words:
            return _ensure_sentence_end(text)

        if len(words) > n_words:
            return _ensure_sentence_end(" ".join(words[:n_words]))

        time.sleep(1)

    text = generate_text(prompt, max_new_tokens=max_new_tokens)
    words = _words(text)

    if len(words) >= n_words:
        return _ensure_sentence_end(" ".join(words[:n_words]))

    while len(words) < n_words:
        words.append("detail")

    return _ensure_sentence_end(" ".join(words[:n_words]))


# ============================ PART 2 (PASTE INTO PART 1) ============================

def get_basic_caption(image_path: str) -> str:                  # unchanged from original
    print(f"{Fore.YELLOW}🖼️  Generating basic caption ...")
    msgs = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Write one complete sentence describing this image."},
            {"type": "image_url", "image_url": {"url": _data_url(image_path)}},
        ],
    }]
    cap, err = _run_models(VISION_MODELS, msgs, max_tokens=90, temperature=0.2)
    return cap if cap else f"[Error] {err}"


# ── New helper: scan folder and return valid image paths ─────────────────────

def get_valid_images(folder: str) -> list:                       # new function for multi-image
    """Scans a folder and returns sorted list of valid image paths."""
    if not os.path.isdir(folder):                                # check folder exists
        print(f"{Fore.RED}❌ '{folder}' is not a valid folder!")
        return []

    found = []
    for filename in os.listdir(folder):                          # iterate every file
        ext = os.path.splitext(filename)[1].lower()              # extract extension
        if ext in VALID_EXTENSIONS:                              # only valid formats
            full_path = os.path.join(folder, filename)           # build full path
            found.append(full_path)                              # collect it

    return sorted(found)                                         # alphabetical order


# ── New feature: generate a short poem from the basic caption ────────────────

def generate_poem(basic_caption: str) -> str:                    # new poem feature
    """Generates a 4-line creative poem inspired by the image caption."""
    prompt = (
        "Write a short, creative 4-line poem inspired by this scene. "
        "No title. No extra explanation. Just 4 lines.\n\n"
        "Scene: " + basic_caption
    )
    try:
        return generate_text(prompt, max_new_tokens=120)         # call text model
    except Exception as e:
        return f"[Error] {e}"


# ── New feature: generate hashtags from the basic caption ────────────────────

def generate_hashtags(basic_caption: str) -> str:                # new hashtag feature
    """Generates 10 relevant social-media hashtags from the image caption."""
    prompt = (
        "Generate exactly 10 relevant social media hashtags for this image. "
        "Output ONLY the hashtags separated by spaces. No explanation. No numbering.\n\n"
        "Image description: " + basic_caption
    )
    try:
        return generate_text(prompt, max_new_tokens=80)          # call text model
    except Exception as e:
        return f"[Error] {e}"


# ── Process one image and return a result dict ────────────────────────────────

def process_single_image(image_path: str, choice: str) -> dict: # new helper for batch
    """Runs the chosen output type on one image and returns a result dict."""
    filename = os.path.basename(image_path)
    print(f"\n{Fore.CYAN}📸 Processing: {Style.BRIGHT}{filename}")

    basic_caption = get_basic_caption(image_path)                # always get caption first
    print(f"{Fore.YELLOW}📝 Basic caption: {basic_caption}")

    result = {"filename": filename, "basic_caption": basic_caption}  # start result dict

    if basic_caption.startswith("[Error]"):                      # vision failed → skip
        print(f"{Fore.RED}❌ Skipping — vision model failed.")
        result["output"] = basic_caption
        return result

    if choice == "1":                                            # 5-word caption
        out = _ensure_sentence_end(_exact_n_words(basic_caption, 5))
        print(f"{Fore.GREEN}✅ Caption (5 words): {Fore.YELLOW}{Style.BRIGHT}{out}")
        result["caption_5"] = out

    elif choice == "2":                                          # 30-word description
        prompt = ("Rewrite as EXACTLY 30 words. Single paragraph. One complete sentence. "
                  "End with a period. No title/bullets.\n\nText: " + basic_caption)
        try:
            out = generate_exact_sentence(prompt, 30, max_new_tokens=220, tries=6)
            print(f"{Fore.GREEN}✅ Description (30 words): {Fore.YELLOW}{Style.BRIGHT}{out}")
            result["description_30"] = out
        except Exception as e:
            print(f"{Fore.RED}❌ Description failed: {e}")
            result["description_30"] = f"[Error] {e}"

    elif choice == "3":                                          # 50-word summary
        prompt = ("Write EXACTLY 50 words. Single paragraph. One complete sentence. "
                  "End with a period. No title/bullets/extra text.\n\nImage seed: " + basic_caption)
        try:
            out = generate_exact_sentence(prompt, 50, max_new_tokens=280, tries=7)
            print(f"{Fore.GREEN}✅ Summary (50 words): {Fore.YELLOW}{Style.BRIGHT}{out}")
            result["summary_50"] = out
        except Exception as e:
            print(f"{Fore.RED}❌ Summary failed: {e}")
            result["summary_50"] = f"[Error] {e}"

    elif choice == "5":                                          # poem (new)
        out = generate_poem(basic_caption)
        print(f"{Fore.GREEN}✅ Poem:\n{Fore.YELLOW}{Style.BRIGHT}{out}")
        result["poem"] = out

    elif choice == "6":                                          # hashtags (new)
        out = generate_hashtags(basic_caption)
        print(f"{Fore.GREEN}✅ Hashtags: {Fore.YELLOW}{Style.BRIGHT}{out}")
        result["hashtags"] = out

    return result


def print_menu():                                                # unchanged from original
    print(f"""{Style.BRIGHT}{Fore.GREEN}
================ Image-to-Text Conversion =================
Select output type:
1. Caption (5 words)
2. Description (30 words)
3. Summary (50 words)
4. Exit
5. Poem (4 lines)                          [NEW]
6. Hashtags (10 tags)                      [NEW]
7. Process entire folder & save JSON       [NEW]
=============================================================
""")


def main():
    # ── Single image path input (unchanged) ──────────────────────────────────
    image_path = input(f"{Fore.BLUE}Enter the path of the image (e.g., test.jpg): {Style.RESET_ALL}")
    if not os.path.exists(image_path):
        print(f"{Fore.RED}❌ The file '{image_path}' does not exist.")
        return
    try:
        Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to open image: {e}")
        return

    basic_caption = get_basic_caption(image_path)               # unchanged
    print(f"{Fore.YELLOW}📝 Basic caption: {Style.BRIGHT}{basic_caption}\n")

    while True:
        print_menu()
        choice = input(f"{Fore.CYAN}Enter your choice (1-7): {Style.RESET_ALL}").strip()

        if basic_caption.startswith("[Error]") and choice in {"1", "2", "3", "5", "6"}:
            basic_caption = get_basic_caption(image_path)       # retry vision if failed
            print(f"{Fore.YELLOW}📝 Basic caption: {Style.BRIGHT}{basic_caption}\n")

        # ── choices 1-4 unchanged ────────────────────────────────────────────

        if choice == "1":                                        # unchanged
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Caption (5 words): {Style.BRIGHT}{basic_caption}\n")
            else:
                out = _ensure_sentence_end(_exact_n_words(basic_caption, 5))
                print(f"{Fore.GREEN}✅ Caption (5 words): {Fore.YELLOW}{Style.BRIGHT}{out}\n")

        elif choice == "2":                                      # unchanged
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Failed to generate description: {basic_caption}")
                continue
            prompt = ("Rewrite as EXACTLY 30 words. Single paragraph. One complete sentence. "
                      "End with a period. No title/bullets.\n\nText: " + basic_caption)
            try:
                out = generate_exact_sentence(prompt, 30, max_new_tokens=220, tries=6)
                print(f"{Fore.GREEN}✅ Description (30 words): {Fore.YELLOW}{Style.BRIGHT}{out}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Failed to generate description: {e}")

        elif choice == "3":                                      # unchanged
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Failed to generate summary: {basic_caption}")
                continue
            prompt = ("Write EXACTLY 50 words. Single paragraph. One complete sentence. "
                      "End with a period. No title/bullets/extra text.\n\nImage seed: " + basic_caption)
            try:
                out = generate_exact_sentence(prompt, 50, max_new_tokens=280, tries=7)
                print(f"{Fore.GREEN}✅ Summary (50 words): {Fore.YELLOW}{Style.BRIGHT}{out}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Failed to generate summary: {e}")

        elif choice == "4":                                      # unchanged
            print(f"{Fore.GREEN}👋 Goodbye!")
            break

        # ── choice 5: Poem (new) ─────────────────────────────────────────────

        elif choice == "5":                                      # new poem feature
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Failed to generate poem: {basic_caption}")
                continue
            out = generate_poem(basic_caption)
            print(f"{Fore.GREEN}✅ Poem:\n{Fore.YELLOW}{Style.BRIGHT}{out}\n")

        # ── choice 6: Hashtags (new) ─────────────────────────────────────────

        elif choice == "6":                                      # new hashtag feature
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Failed to generate hashtags: {basic_caption}")
                continue
            out = generate_hashtags(basic_caption)
            print(f"{Fore.GREEN}✅ Hashtags: {Fore.YELLOW}{Style.BRIGHT}{out}\n")

        # ── choice 7: Process entire folder & save JSON (new) ────────────────

        elif choice == "7":                                      # new multi-image + save feature
            folder = input(f"{Fore.BLUE}Enter folder path containing images: {Style.RESET_ALL}").strip()
            images = get_valid_images(folder)                    # scan folder
            if not images:
                print(f"{Fore.RED}⚠️  No valid images found in that folder.")
                continue

            print(f"\n{Fore.GREEN}✅ Found {len(images)} image(s).")
            print(f"{Fore.CYAN}Which output to generate for all images?")
            print("  1=Caption  2=Description  3=Summary  5=Poem  6=Hashtags")
            batch_choice = input(f"{Fore.CYAN}Choice: {Style.RESET_ALL}").strip()

            if batch_choice not in {"1", "2", "3", "5", "6"}:   # validate batch choice
                print(f"{Fore.RED}❌ Invalid choice for batch mode.")
                continue

            all_results = []                                     # collect all results

            for i, img_path in enumerate(images, 1):            # loop every image
                print(f"\n{Fore.MAGENTA}[{i}/{len(images)}] ──────────────────────────")
                result = process_single_image(img_path, batch_choice)  # process it
                all_results.append(result)                       # save to list

            # save all results to a timestamped JSON file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # unique timestamp
            save_path = os.path.join(folder, f"results_{timestamp}.json")  # file path
            with open(save_path, "w", encoding="utf-8") as f:   # open for writing
                json.dump(all_results, f, indent=2, ensure_ascii=False)  # write JSON

            print(f"\n{Fore.GREEN}🎉 Done! Results saved → {Style.BRIGHT}{save_path}\n")

        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()