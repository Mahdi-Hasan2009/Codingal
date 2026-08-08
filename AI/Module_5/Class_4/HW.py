import base64, requests, os, json          #  os (folder ops), json (save results)
from datetime import datetime               #  to create timestamp in filename
from config import HF_API_KEY

API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
MODELS = [
    "zai-org/GLM-4.5V",
    "Qwen/Qwen2.5-VL-72B-Instruct",
    "Qwen/Qwen2.5-VL-32B-Instruct",
    "google/gemma-3-27b-it",
]

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}  #  define which formats are valid


# ── Previous utility functions (completely unchanged) ─────────────────────────

def data_url(b: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(b).decode("utf-8")


def extract_err(r: requests.Response) -> str:
    try:
        j = r.json()
        return j.get("error", {}).get("message") or str(j)
    except Exception:
        return (r.text or "").strip() or r.reason or "Request failed."


def box(title: str, lines: list[str], icon: str):
    w = max(30, len(title) + 4, *(len(x) for x in lines))
    print("\n" + "┏" + "━" * (w + 2) + "┓")
    print(f"┃ {icon} {title.ljust(w - 2)} ┃")
    print("┣" + "━" * (w + 2) + "┫")
    for x in lines:
        print(f"┃ {x.ljust(w)} ┃")
    print("┗" + "━" * (w + 2) + "┛\n")


# ──  New function: scans folder and returns valid image paths ───────────────

def get_valid_images(folder: str) -> list[str]:          #  entire function is new
    if not os.path.isdir(folder):                        #  check if folder exists
        print(f"❌ '{folder}' is not a valid folder!")
        return []

    found = []
    for filename in os.listdir(folder):                  # iterate every file in folder
        ext = os.path.splitext(filename)[1].lower()      #  extract extension (.JPG → .jpg)
        if ext in VALID_EXTENSIONS:                      #  only accept valid extensions
            full_path = os.path.join(folder, filename)   #  folder + filename = full path
            found.append(full_path)                      #  add to list

    return sorted(found)                                 #  sort in alphabetical order


# ──  Previous caption logic → extracted into its own function (reusable) ───

def get_caption(image_path: str) -> str:                 #  entire function is new
    """Returns a caption for one image. Returns an error string if it fails."""

    try:
        with open(image_path, "rb") as f:                # was inside main function before
            img = f.read()                               # now extracted here
    except Exception as e:
        return f"[File read error: {e}]"                 #  return error as string

    base = {
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Give a short caption for this image."},
                {"type": "image_url", "image_url": {"url": data_url(img)}},
            ],
        }],
        "max_tokens": 60,
        "temperature": 0.2,
    }

    last = "Unknown error"                               #  default error message
    for model in MODELS:
        payload = dict(base, model=model)
        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
        except requests.RequestException as e:
            last = f"Request failed: {e}"
            continue

        if r.status_code != 200:
            last = extract_err(r)
            continue

        try:
            d = r.json()
        except Exception:
            last = "Non-JSON response."
            continue

        cap = (d.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        if cap:
            return cap                                   #  return directly (no box)
        last = "No caption in response."

    return f"[Error: {last}]"                           #  all models failed, return error


# ──  New main function: handles multiple images + saves summary file ────────

def caption_multiple_images():                           #  entire function is new
    # ── 1. Get folder path
    folder = input("📁 Enter image folder path: ").strip()  #  folder input (was single file before)

    # ── 2. Find valid images
    images = get_valid_images(folder)                    # scan the folder
    if not images:
        print("⚠️  No valid images found!")
        return

    print(f"\n✅ Found {len(images)} image(s). Starting...\n")  #  show count

    # ── 3. Process each image
    results = []                                         #  list to collect all captions

    for i, path in enumerate(images, 1):                 #  loop over every image
        filename = os.path.basename(path)                #  extract filename from full path
        print(f"[{i}/{len(images)}] 🔄 {filename}")      #  show progress

        caption = get_caption(path)                      #  call caption function
        print(f"         ✏️  {caption}\n")               #  print result

        results.append({                                 #  add as dict to list
            "filename": filename,
            "caption": caption,
        })

    # ── 4. Save to summary file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # 🆕 create unique timestamp
    summary_path = os.path.join(folder, f"captions_{timestamp}.json")  # 🆕 build file path

    with open(summary_path, "w", encoding="utf-8") as f:  # 🆕 open file for writing
        json.dump(results, f, indent=2, ensure_ascii=False)  # 🆕 save as JSON

    print(f"\n🎉 Done! Summary saved → {summary_path}")  # 🆕 final message


# ── Entry point (same as before) ─────────────────────────────────────────────

def main():
    caption_multiple_images()                            # 🆕 calls the new function


if __name__ == "__main__":
    main()
