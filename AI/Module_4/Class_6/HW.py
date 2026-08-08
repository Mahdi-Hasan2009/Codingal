import requests
import time
from openai import OpenAI
from groq import Groq
from config import HF_API_KEY, OPENAI_API_KEY, GROQ_API_KEY
from colorama import Fore, Style, init
import os

# Initialize colorama so terminal text can be colored
init(autoreset=True)

# Default model used when user does not specify one
DEFAULT_MODEL = "google/pegasus-xsum"


def build_api_url(model_name):
    # Build the full HuggingFace API endpoint URL for the given model
    return f"https://router.huggingface.co/hf-inference/models/{model_name}"


def query(payload, model_name=DEFAULT_MODEL, retries=3):
    """
    Sends a POST request to the HuggingFace Inference API.
    Automatically retries up to 3 times if the model is still loading.
    """
    api_url = build_api_url(model_name)
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    for attempt in range(retries):
        response = requests.post(api_url, headers=headers, json=payload)

        # If the response body is completely empty, the API had a server-side issue
        if not response.text.strip():
            print(Fore.RED + f"❌ Empty response from API. Status code: {response.status_code}")
            return None

        # Try converting the response text into a Python dictionary (JSON parsing)
        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            print(Fore.RED + f"❌ Could not parse JSON. Raw response: {response.text[:300]}")
            return None

        # HuggingFace returns {"error": "...", "estimated_time": X} when model is still warming up
        if isinstance(result, dict) and "error" in result:
            wait = result.get("estimated_time", 20)
            print(Fore.YELLOW + f"⏳ Model is loading, retrying in {wait:.0f}s... (attempt {attempt + 1}/{retries})")
            time.sleep(wait)
            continue

        # If we reach here, the response is valid — return it
        return result

    print(Fore.RED + "❌ Model failed to load after multiple retries.")
    return None


def query_openai(text, min_length, max_length):
    """
    Sends a summarization request to OpenAI's GPT-4o-mini model.
    Requires a valid paid OpenAI API key with available quota.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cheapest and fastest OpenAI model
        messages=[
            {
                "role": "system",
                "content": f"Summarize the given text. Keep it between {min_length} and {max_length} words."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content


def query_groq(text, min_length, max_length):
    """
    Sends a summarization request to Groq's LLaMA model.
    Groq is completely FREE and extremely fast.
    """
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Free LLaMA 3 hosted on Groq
        messages=[
            {
                "role": "system",
                "content": f"Summarize the given text. Keep it between {min_length} and {max_length} words."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content


def expand_text(text):
    """
    Takes a short prompt or plot outline and expands it
    into a detailed, descriptive paragraph using Groq LLaMA.
    """
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a creative writing assistant. "
                    "The user will give you a short prompt or plot outline. "
                    "Expand it into a detailed, descriptive, and engaging paragraph. "
                    "Keep the core meaning intact. Do not change the story — just make it richer."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content


def analyze_sentiment(text):
    """
    Passes the text through a HuggingFace classification model
    to detect emotional tone: Positive, Neutral, Negative.
    """
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    api_url = build_api_url(model_name)
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}

    print(Fore.BLUE + Style.BRIGHT + "\n🔍 Analyzing sentiment using HuggingFace RoBERTa...")

    for attempt in range(3):
        response = requests.post(api_url, headers=headers, json=payload)

        if not response.text.strip():
            print(Fore.RED + f"❌ Empty response. Status: {response.status_code}")
            return None

        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            print(Fore.RED + f"❌ Could not parse response: {response.text[:300]}")
            return None

        # Model still loading — wait and retry
        if isinstance(result, dict) and "error" in result:
            wait = result.get("estimated_time", 20)
            print(Fore.YELLOW + f"⏳ Model loading, retrying in {wait:.0f}s... ({attempt+1}/3)")
            time.sleep(wait)
            continue

        return result

    print(Fore.RED + "❌ Model failed to load after retries.")
    return None


def display_sentiment(result, user_name):
    """
    Takes the raw API result and displays it in a
    clean, readable percentage format with colors and a visual bar.
    """
    if not result or not isinstance(result, list):
        print(Fore.RED + "❌ Could not read sentiment result.")
        return

    sentiments = result[0]

    # Sort by score — highest percentage first
    sentiments = sorted(sentiments, key=lambda x: x["score"], reverse=True)

    print(Fore.GREEN + Style.BRIGHT + f"\n📊 Sentiment Analysis Result for {user_name}:")
    print(Fore.WHITE + "─" * 40)

    for item in sentiments:
        label = item["label"]
        score = item["score"]
        percentage = score * 100

        # Color code each sentiment type
        if "positive" in label.lower():
            color = Fore.GREEN
            emoji = "😊"
        elif "negative" in label.lower():
            color = Fore.RED
            emoji = "😠"
        else:
            color = Fore.YELLOW
            emoji = "😐"

        # Visual bar — each block = 5%
        bar_length = int(percentage / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)

        print(color + f"{emoji} {label:<10} {bar}  {percentage:.1f}%")

    print(Fore.WHITE + "─" * 40)

    # Show the dominant emotion
    top = sentiments[0]
    print(Fore.CYAN + Style.BRIGHT + f"\n✅ Overall Tone: {top['label']} ({top['score']*100:.1f}%)")


def shift_tone(text, tone):
    """
    Rewrites the given text in a specific tone/style
    using Groq LLaMA without changing the core meaning.
    """

    # Each tone option has a name and a system instruction for the AI
    tone_prompts = {
        "1": (
            "Professional",
            "Rewrite the following text in a formal, professional tone. "
            "Use clear, concise language suitable for a business setting."
        ),
        "2": (
            "Casual",
            "Rewrite the following text in a casual, friendly, and relaxed tone. "
            "Use everyday language as if talking to a close friend."
        ),
        "3": (
            "Shakespearean",
            "Rewrite the following text as if William Shakespeare wrote it. "
            "Use old English, poetic language, and dramatic flair."
        ),
        "4": (
            "Gen Z Slang",
            "Rewrite the following text using modern Gen Z internet slang. "
            "Use words like 'no cap', 'bussin', 'lowkey', 'slay', 'fr fr' etc."
        ),
        "5": (
            "Pirate",
            "Rewrite the following text as if a pirate is speaking. "
            "Use 'Arrr', 'matey', 'ye', 'landlubber' and other pirate expressions."
        ),
    }

    # Validate the tone choice
    if tone not in tone_prompts:
        print(Fore.RED + "❌ Invalid tone choice.")
        return None

    tone_name, system_instruction = tone_prompts[tone]

    print(Fore.BLUE + Style.BRIGHT + f"\n✍️ Shifting tone to: {tone_name}...")

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                # System message tells AI which tone/style to use
                "role": "system",
                "content": system_instruction
            },
            {
                # The original text to rewrite
                "role": "user",
                "content": text
            }
        ]
    )

    return tone_name, response.choices[0].message.content
def generate_keywords(text, mode):
    """
    Extracts important themes from the text and generates
    either SEO keywords or social media hashtags using Groq LLaMA.

    Args:
        text : input text to analyze
        mode : "1" for SEO Keywords, "2" for Hashtags

    Returns:
        Generated keywords or hashtags as a string
    """

    # Different instructions for SEO vs Hashtags
    if mode == "1":
        mode_name = "SEO Keywords"
        instruction = (
            "You are an SEO expert. "
            "Read the given text carefully and extract the most important themes. "
            "Generate a list of 10-15 SEO keywords that best represent the content. "
            "Format: return ONLY a numbered list of keywords, nothing else. "
            "Example:\n1. artificial intelligence\n2. machine learning\n3. healthcare AI"
        )
    elif mode == "2":
        mode_name = "Hashtags"
        instruction = (
            "You are a social media marketing expert. "
            "Read the given text carefully and extract the most important themes. "
            "Generate 15-20 relevant social media hashtags based on the content. "
            "Format: return ONLY hashtags separated by spaces, nothing else. "
            "Example: #ArtificialIntelligence #MachineLearning #AIHealthcare"
        )
    else:
        print(Fore.RED + "❌ Invalid mode choice.")
        return None, None

    print(Fore.BLUE + Style.BRIGHT + f"\n🔑 Generating {mode_name} using Groq LLaMA...")

    # Create Groq client
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                # Tell AI exactly what to generate
                "role": "system",
                "content": instruction
            },
            {
                # The text to extract keywords/hashtags from
                "role": "user",
                "content": text
            }
        ]
    )

    return mode_name, response.choices[0].message.content


def display_keywords(result, user_name):
    """
    Displays the generated keywords or hashtags
    in a clean, readable format with colors.

    Args:
        result    : tuple of (mode_name, generated_text)
        user_name : name of the user
    """
    if not result:
        print(Fore.RED + "❌ Failed to generate keywords.")
        return

    mode_name, content = result

    print(Fore.GREEN + Style.BRIGHT + f"\n🔑 {mode_name} for {user_name}:")
    print(Fore.WHITE + "─" * 40)

    # Hashtags — color each one cyan
    if mode_name == "Hashtags":
        hashtags = content.strip().split()
        for tag in hashtags:
            print(Fore.CYAN + f"  {tag}")

    # SEO Keywords — print numbered list in green
    else:
        lines = content.strip().split("\n")
        for line in lines:
            print(Fore.GREEN + f"  {line}")

    print(Fore.WHITE + "─" * 40)

def translate_text(text, language_choice):
    """
    Translates the given text into the user-selected language
    using Groq LLaMA. Supports top 20 most used languages worldwide.

    Args:
        text            : input text to translate
        language_choice : number string "1" to "20"

    Returns:
        Tuple of (language_name, translated_text), or None if failed
    """

    # Top 20 most spoken/used languages in the world
    languages = {
        "1":  "Spanish",
        "2":  "French",
        "3":  "Arabic",
        "4":  "Bengali",
        "5":  "Hindi",
        "6":  "Portuguese",
        "7":  "Russian",
        "8":  "Japanese",
        "9":  "German",
        "10": "Chinese (Simplified)",
        "11": "Korean",
        "12": "Turkish",
        "13": "Italian",
        "14": "Urdu",
        "15": "Indonesian",
        "16": "Thai",
        "17": "Vietnamese",
        "18": "Persian (Farsi)",
        "19": "Swahili",
        "20": "Dutch",
    }

    # Check if the choice is valid
    if language_choice not in languages:
        print(Fore.RED + "❌ Invalid language choice.")
        return None

    language_name = languages[language_choice]

    print(Fore.BLUE + Style.BRIGHT + f"\n🌍 Translating to {language_name} using Groq LLaMA...")

    # Create Groq client
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                # Tell AI to translate — nothing else, no explanation
                "role": "system",
                "content": (
                    f"You are a professional translator. "
                    f"Translate the given text into {language_name}. "
                    f"Return ONLY the translated text. "
                    f"Do not add any explanation, notes, or extra words."
                )
            },
            {
                # The text to translate
                "role": "user",
                "content": text
            }
        ]
    )

    return language_name, response.choices[0].message.content


def display_translation(result, user_name):
    
    if not result:
        print(Fore.RED + "❌ Translation failed.")
        return

    language_name, translated = result

    rtl_languages = ["Arabic", "Urdu", "Persian (Farsi)"]

    print(Fore.GREEN + Style.BRIGHT + f"\n🌍 Translation Result for {user_name}:")
    print(Fore.WHITE + "─" * 40)
    print(Fore.CYAN + f"  Language : {language_name}")
    print(Fore.WHITE + "─" * 40)

    if language_name in rtl_languages:

        # ফাইলটা HW.py এর একই folder এ save হবে
        script_folder = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(script_folder, f"translation_{language_name.replace(' ', '_')}.txt")

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"Translation for {user_name}\n")
            f.write(f"Language: {language_name}\n")
            f.write("─" * 40 + "\n")
            f.write(translated + "\n")

        print(Fore.YELLOW + f"  ⚠️  {language_name} is a Right-to-Left language.")
        print(Fore.YELLOW + f"  ⚠️  Terminal cannot display it correctly.")
        print(Fore.GREEN  + f"  ✅  Saved to: {file_name}")  # ← পুরো path দেখাবে
        print(Fore.CYAN   + f"  📂  Open the file in Notepad to read correctly.")

    else:
        print(Fore.GREEN + f"  {translated}")

    print(Fore.WHITE + "─" * 40)
    
def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
    """
    Central function that routes the summarization request
    to the correct AI provider based on the model name.

    'groq'   → Free LLaMA via Groq
    'openai' → Paid GPT-4o-mini
    other    → HuggingFace model
    """

    # Route 1: Groq (Free + Fast)
    if model_name.lower() == "groq":
        print(Fore.BLUE + Style.BRIGHT + "\n🤖 Performing AI summarization using Groq LLaMA (Free & Fast)")
        return query_groq(text, min_length, max_length)

    # Route 2: OpenAI (Paid)
    if model_name.lower() == "openai":
        print(Fore.BLUE + Style.BRIGHT + "\n🤖 Performing AI summarization using OpenAI GPT-4o-mini")
        return query_openai(text, min_length, max_length)

    # Route 3: HuggingFace (Free but slower)
    payload = {
        "inputs": text,
        "parameters": {"min_length": min_length, "max_length": max_length}
    }
    print(Fore.BLUE + Style.BRIGHT + f"\n🤖 Performing AI summarization using HuggingFace model: {model_name}")

    result = query(payload, model_name=model_name)

    if result is None:
        return None
    elif isinstance(result, list) and result and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED + "❌ Unexpected response format:", result)
        return None


# ── Program Entry Point ───────────────────────────────────────────────────────
if __name__ == "__main__":

    # Step 1: Greet the user
    print(Fore.YELLOW + Style.BRIGHT + "👋 Hi there! What's your name?")
    user_name = input("Your name: ").strip()
    if not user_name:
        user_name = "User"
    print(Fore.GREEN + f"Welcome, {user_name}! Let's give your text some AI magic ✨.")

    # Step 2: Ask what the user wants to do
    print(Fore.YELLOW + Style.BRIGHT + "\nWhat do you want to do?")
    print("  1. Summarize Text      → Make long text shorter")
    print("  2. Expand Text         → Make short text longer")
    print("  3. Sentiment Analysis  → Detect emotional tone")
    print("  4. Tone Shifter        → Rewrite in a different style")
    print("  5. Keyword Generator   → SEO keywords or Hashtags")
    print("  6. Translate Text      → Convert to another language")  
    task_choice = input("Enter 1-6: ").strip()

    # Step 3: Ask for the input text
    print(Fore.YELLOW + Style.BRIGHT + "\nPlease enter your text:")
    user_text = input("> ").strip()

    if not user_text:
        print(Fore.RED + "❌ No text provided. Exiting.")

    # ── Task 1: Summarize ─────────────────────────────────────────────────────
    elif task_choice == "1":
        print(Fore.YELLOW + "\nEnter the model name you want to use:")
        print(Fore.CYAN + "  • Press Enter  → HuggingFace Pegasus (default)")
        print(Fore.CYAN + "  • groq         → Free LLaMA via Groq ⚡")
        print(Fore.CYAN + "  • openai       → Paid GPT-4o-mini")
        print(Fore.CYAN + "  • HF model     → e.g. facebook/bart-large-cnn")
        model_choice = input("Model name (leave blank for default): ").strip()
        if not model_choice:
            model_choice = DEFAULT_MODEL

        print(Fore.YELLOW + "\nChoose your summarization style:")
        print("  1. Standard Summary  → Quick & concise  (50-150 words)")
        print("  2. Enhanced Summary  → Detailed & refined (80-200 words)")
        style_choice = input("Enter 1 or 2: ").strip()

        if style_choice == "2":
            min_length = 80
            max_length = 200
            print(Fore.BLUE + "Enhancing summarization process... 🔍")
        else:
            min_length = 50
            max_length = 150
            print(Fore.BLUE + "Using standard summarization settings... ⚡")

        summary = summarize_text(user_text, min_length, max_length, model_name=model_choice)

        if summary:
            print(Fore.GREEN + Style.BRIGHT + f"\n📝 AI Summarizer Output for {user_name}:")
            print(Fore.GREEN + summary)
        else:
            print(Fore.RED + "❌ Failed to generate summary.")

    # ── Task 2: Expand ────────────────────────────────────────────────────────
    elif task_choice == "2":
        print(Fore.BLUE + Style.BRIGHT + "\n✍️ Expanding your text using Groq LLaMA...")
        result = expand_text(user_text)

        if result:
            print(Fore.GREEN + Style.BRIGHT + f"\n📝 Expanded Text for {user_name}:")
            print(Fore.WHITE + "─" * 40)
            print(Fore.GREEN + result)
            print(Fore.WHITE + "─" * 40)
        else:
            print(Fore.RED + "❌ Failed to expand text.")

    # ── Task 3: Sentiment Analysis ────────────────────────────────────────────
    elif task_choice == "3":
        result = analyze_sentiment(user_text)
        display_sentiment(result, user_name)

    # ── Task 4: Tone Shifter ──────────────────────────────────────────────────
    elif task_choice == "4":
        print(Fore.YELLOW + Style.BRIGHT + "\nChoose a tone:")
        print("  1. Professional   → Formal & business-like")
        print("  2. Casual         → Friendly & relaxed")
        print("  3. Shakespearean  → Old English & dramatic")
        print("  4. Gen Z Slang    → no cap, bussin, slay 💅")
        print("  5. Pirate         → Arrr matey! 🏴‍☠️")
        tone_choice = input("Enter 1-5: ").strip()

        result = shift_tone(user_text, tone_choice)

        if result:
            tone_name, rewritten_text = result
            print(Fore.GREEN + Style.BRIGHT + f"\n🎨 {tone_name} Version for {user_name}:")
            print(Fore.WHITE + "─" * 40)
            print(Fore.GREEN + rewritten_text)
            print(Fore.WHITE + "─" * 40)
        else:
            print(Fore.RED + "❌ Failed to shift tone.")
    # ── Task 5: Keyword/Hashtag Generator ────────────────────────────────────
    elif task_choice == "5":
        print(Fore.YELLOW + Style.BRIGHT + "\nWhat do you want to generate?")
        print("  1. SEO Keywords  → For blogs, websites, search engines")
        print("  2. Hashtags      → For Instagram, Twitter, LinkedIn")
        mode_choice = input("Enter 1 or 2: ").strip()

        result = generate_keywords(user_text, mode_choice)
        display_keywords(result, user_name)
        
    # ── Task 6: Translation ───────────────────────────────────────────────────
    elif task_choice == "6":

        # Show all 20 language options
        print(Fore.YELLOW + Style.BRIGHT + "\nChoose a language:")
        print(Fore.CYAN + "  1.  Spanish          🇪🇸")
        print(Fore.CYAN + "  2.  French           🇫🇷")
        print(Fore.CYAN + "  3.  Arabic           🇸🇦")
        print(Fore.CYAN + "  4.  Bengali          🇧🇩")
        print(Fore.CYAN + "  5.  Hindi            🇮🇳")
        print(Fore.CYAN + "  6.  Portuguese       🇧🇷")
        print(Fore.CYAN + "  7.  Russian          🇷🇺")
        print(Fore.CYAN + "  8.  Japanese         🇯🇵")
        print(Fore.CYAN + "  9.  German           🇩🇪")
        print(Fore.CYAN + "  10. Chinese          🇨🇳")
        print(Fore.CYAN + "  11. Korean           🇰🇷")
        print(Fore.CYAN + "  12. Turkish          🇹🇷")
        print(Fore.CYAN + "  13. Italian          🇮🇹")
        print(Fore.CYAN + "  14. Urdu             🇵🇰")
        print(Fore.CYAN + "  15. Indonesian       🇮🇩")
        print(Fore.CYAN + "  16. Thai             🇹🇭")
        print(Fore.CYAN + "  17. Vietnamese       🇻🇳")
        print(Fore.CYAN + "  18. Persian (Farsi)  🇮🇷")
        print(Fore.CYAN + "  19. Swahili          🇰🇪")
        print(Fore.CYAN + "  20. Dutch            🇳🇱")
        language_choice = input("Enter 1-20: ").strip()

        result = translate_text(user_text, language_choice)
        display_translation(result, user_name)

    # ── Invalid choice ────────────────────────────────────────────────────────
    else:
        print(Fore.RED + "❌ Invalid choice. Please enter 1-6.")