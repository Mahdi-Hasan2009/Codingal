"""
Simple Text-to-Image Generator
Uses Pollinations AI for image generation (free, no API key needed)
Uses HuggingFace for prompt enhancement only

INSTALLATION:
    pip install huggingface-hub pillow requests
"""
from huggingface_hub import InferenceClient
from datetime import datetime
from PIL import Image
from config import HF_API_KEY
import os
import requests
from io import BytesIO

# Style presets - name and keywords for each style
STYLES = {
    "1": ("Anime",          "anime style, studio ghibli, vibrant colors, cel shading, detailed linework, 2D illustration"),
    "2": ("Photorealistic",  "photorealistic, 4K, DSLR photography, sharp focus, natural lighting, hyperdetailed"),
    "3": ("Oil Painting",   "oil painting, classical art, brush strokes, textured canvas, renaissance style, rich colors"),
    "4": ("3D Render",      "3D render, octane render, Unreal Engine 5, ray tracing, subsurface scattering, 8K"),
    "5": ("Cyberpunk",      "cyberpunk, neon lights, futuristic city, dark atmosphere, rain reflections, blade runner style"),
    "6": ("Watercolor",     "watercolor painting, soft edges, pastel colors, wet on wet technique, artistic"),
    "7": ("No Style",       ""),
}

# Supported save formats - name, extension, and save options
FORMATS = {
    "1": ("PNG",  "png",  {}),
    "2": ("JPG",  "jpg",  {"quality": 95}),
    "3": ("WEBP", "webp", {"quality": 90}),
    "4": ("BMP",  "bmp",  {}),
}

def enhance_prompt(simple_prompt):
    # Send simple prompt to Qwen model and get a detailed midjourney-style prompt back
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[
            {
                "role": "system",
                "content": """You are an expert image prompt engineer.
Take the user's simple prompt and expand it into a highly detailed, 
midjourney-style image generation prompt.
Add: art style, lighting, camera angle, quality keywords, mood.
Return ONLY the enhanced prompt. No explanation. No extra text."""
            },
            {
                "role": "user",
                "content": simple_prompt
            }
        ],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

def show_style_menu():
    # Print all available style options
    print("\n🎨 Select Style:")
    for key, (name, _) in STYLES.items():
        print(f"  [{key}] {name}")

def get_style():
    # Keep asking until user enters a valid choice
    while True:
        choice = input("Enter choice (1-7): ").strip()
        if choice in STYLES:
            name, keywords = STYLES[choice]
            if keywords:
                print(f"✅ Style: {name}\n")
            else:
                print(f"✅ No style selected\n")
            return keywords
        else:
            print("⚠️ Invalid choice! Please enter 1-7")

def apply_style(prompt, style_keywords):
    # Append style keywords to the prompt if a style was selected
    if style_keywords:
        return f"{prompt}, {style_keywords}"
    return prompt

def get_image_path():
    # Ask user for an input image path, validate it, return None if skipped or invalid
    path = input("🖼️  Image path (Enter to skip): ").strip()

    # User pressed Enter to skip
    if not path:
        return None

    # Check if file exists on disk
    if not os.path.exists(path):
        print("⚠️ File not found! Skipping image input.")
        return None

    # Only allow image file types
    valid_extensions = [".png", ".jpg", ".jpeg", ".webp"]
    ext = os.path.splitext(path)[1].lower()
    if ext not in valid_extensions:
        print("⚠️ Invalid file type! Use PNG, JPG, or WEBP. Skipping.")
        return None

    print("✅ Image loaded!\n")
    return path

def show_format_menu():
    # Print all available save format options
    print("\n💾 Select Save Format:")
    for key, (name, ext, _) in FORMATS.items():
        print(f"  [{key}] {name} (.{ext})")

def get_format():
    # Keep asking until user enters a valid format choice
    while True:
        choice = input("Enter choice (1-4): ").strip()
        if choice in FORMATS:
            name, ext, options = FORMATS[choice]
            print(f"✅ Format: {name}\n")
            return ext, options
        else:
            print("⚠️ Invalid choice! Please enter 1-4")

def save_image(image, ext, options):
    # Generate a unique filename using timestamp and save the image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_{timestamp}.{ext}"

    # JPG, BMP and WEBP do not support RGBA, convert to RGB first
    if ext in ["jpg", "bmp", "webp"] and image.mode == "RGBA":
        image = image.convert("RGB")

    # Pillow uses JPEG not JPG
    fmt = ext.upper()
    if fmt == "JPG":
        fmt = "JPEG"

    image.save(filename, format=fmt, **options)
    return filename

def generate_image(enhanced, image_path):
    # Image-to-Image mode is not supported by Pollinations, use text-to-image only
    if image_path:
        print("⚠️  Image-to-Image not supported with Pollinations. Using text prompt only.")

    print("✏️  Mode: Text-to-Image (Pollinations AI)")

    try:
        #____________________________________________________________________________
        # Build Pollinations URL with encoded prompt
        encoded = requests.utils.quote(enhanced)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"

        print("⏳ Waiting for image... (may take 10-30 seconds)")
        response = requests.get(url, timeout=60)

        # Check if request was successful
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            print("✅ Image generated!")
            return image
        else:
            print(f"❌ Pollinations failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

# Initialize the HuggingFace client with API key (for enhancer only)
client = InferenceClient(api_key=HF_API_KEY)

print("🤖 Text-to-Image Generator")
print("✨ Enhancer : HuggingFace (Qwen)")
print("🎨 Generator: Pollinations AI (Free)")
print("Type 'quit' to exit\n")

while True:
    prompt = input("Enter prompt: ").strip()

    # Exit the loop if user types quit/exit/q
    if prompt.lower() in ["quit", "exit", "q"]:
        break

    # Skip empty input
    if not prompt:
        continue

    # Step 1: Show style menu and get user's style choice
    show_style_menu()
    style_keywords = get_style()
    styled_prompt = apply_style(prompt, style_keywords)

    # Step 2: Ask for optional input image path
    image_path = get_image_path()

    # Step 3: Ask for save format
    show_format_menu()
    ext, options = get_format()

    # Step 4: Enhance the prompt using AI
    print("🔮 Enhancing prompt...")
    try:
        enhanced = enhance_prompt(styled_prompt)
        print(f"✨ Enhanced: {enhanced}\n")
    except Exception as e:
        # If enhancer fails, fall back to the original styled prompt
        print(f"⚠️ Enhancer failed: {type(e).__name__}: {e}")
        print("Using original prompt...")
        enhanced = styled_prompt

    # Step 5: Generate the image
    print("🎨 Generating image...")
    image = generate_image(enhanced, image_path)

    # Step 6: Save and display the image
    if image:
        filename = save_image(image, ext, options)
        print(f"✓ Saved: {filename}")
        image.show()
        print()
    else:
        print("Error: Generation failed. Try again.\n")

print("Goodbye!")