#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════╗
# ║        ✨  Vintage Photo Enhancer                    ║
# ║  No object detection. No boxes. No labels.          ║
# ║  Just: old photo in → beautiful photo out.          ║
# ║  Requires: pillow                                   ║
# ╚══════════════════════════════════════════════════════╝

import os, io
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ALLOWED = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
MAX_MB  = 8

# ────────────────────────────────────────────────────────
#  STEP 1 : ছবি বেছে নাও
# ────────────────────────────────────────────────────────
def ask_image():
    print("\n📂 তোমার পুরনো ছবির path দাও (JPG/PNG/WebP ≤ 8MB).")
    while True:
        p = input("Image path: ").strip().strip('"').strip("'")
        if not p or not os.path.isfile(p):
            print("⚠️  File পাওয়া যায়নি।"); continue
        if os.path.splitext(p)[1].lower() not in ALLOWED:
            print("⚠️  এই format support করে না।"); continue
        if os.path.getsize(p) / (1024 * 1024) > MAX_MB:
            print("⚠️  File অনেক বড় (> 8MB)।"); continue
        try:
            Image.open(p).verify()
        except Exception:
            print("⚠️  ছবিটা corrupted।"); continue
        return p

# ────────────────────────────────────────────────────────
#  STEP 2 : Enhance করো
# ────────────────────────────────────────────────────────
def enhance(img: Image.Image) -> Image.Image:
    print("\n🔧 Enhancing চলছে...")

    # ১. Auto contrast — exposure ঠিক করে
    img = ImageOps.autocontrast(img, cutoff=1)
    print("  ✅ Auto contrast done")

    # ২. Brightness একটু বাড়াও
    img = ImageEnhance.Brightness(img).enhance(1.15)
    print("  ✅ Brightness boost done")

    # ৩. Contrast আরো sharp করো
    img = ImageEnhance.Contrast(img).enhance(1.25)
    print("  ✅ Contrast boost done")

    # ৪. Color/Saturation vivid করো
    img = ImageEnhance.Color(img).enhance(1.3)
    print("  ✅ Color vivid done")

    # ৫. Sharpness বাড়াও
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    print("  ✅ Sharpness boost done")

    # ৬. Noise কমাও (median filter)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    print("  ✅ Noise reduction done")

    # ৭. Final unsharp mask — edges crisp করো
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=3))
    print("  ✅ Final sharpening done")

    return img

# ────────────────────────────────────────────────────────
#  STEP 3 : Before/After comparison save করো
# ────────────────────────────────────────────────────────
def save_comparison(original: Image.Image, enhanced: Image.Image, out_path: str):
    w, h = original.size

    # Dark background canvas
    canvas = Image.new("RGB", (w * 2 + 40, h + 80), (20, 20, 20))
    canvas.paste(original.convert("RGB"), (10, 50))
    canvas.paste(enhanced,               (w + 30, 50))

    from PIL import ImageDraw
    draw = ImageDraw.Draw(canvas)

    # Labels
    draw.rectangle([(10, 10), (w + 10, 45)],        fill=(180, 50, 50))
    draw.rectangle([(w + 30, 10), (w * 2 + 30, 45)], fill=(50, 160, 80))
    draw.text((w // 2 - 20, 18),         "BEFORE", fill=(255, 255, 255))
    draw.text((w + 30 + w // 2 - 20, 18), "AFTER", fill=(255, 255, 255))

    canvas.save(out_path)
    print(f"  ✅ Comparison image saved: {out_path}")

# ────────────────────────────────────────────────────────
#  MAIN
# ────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  ✨  Vintage Photo Enhancer")
    print("  কোনো box নেই। কোনো label নেই।")
    print("  শুধু সুন্দর ছবি! 🖼️")
    print("=" * 50)

    # ছবি লোড
    path     = ask_image()
    original = Image.open(path).convert("RGB")
    print(f"\n✅ Loaded: {os.path.basename(path)}  ({original.size[0]}×{original.size[1]} px)")

    # Custom settings (optional)
    print("\n⚙️  Custom settings (Enter চাপলে default use হবে):")

    brightness = input("  Brightness (default 1.15, range 0.5–2.0): ").strip()
    contrast   = input("  Contrast   (default 1.25, range 0.5–2.0): ").strip()
    color      = input("  Color      (default 1.30, range 0.5–2.0): ").strip()
    sharpness  = input("  Sharpness  (default 2.00, range 0.5–3.0): ").strip()

    # Apply custom values if given
    img = ImageOps.autocontrast(original, cutoff=1)
    img = ImageEnhance.Brightness(img).enhance(float(brightness) if brightness else 1.15)
    img = ImageEnhance.Contrast(img).enhance(float(contrast)   if contrast   else 1.25)
    img = ImageEnhance.Color(img).enhance(float(color)         if color      else 1.30)
    img = ImageEnhance.Sharpness(img).enhance(float(sharpness) if sharpness  else 2.00)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=3))

    print("\n✅ Enhancement সম্পন্ন!")

    # Save
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_img = f"enhanced_{ts}.png"
    out_cmp = f"comparison_{ts}.png"

    img.save(out_img)
    save_comparison(original, img, out_cmp)

    print(f"\n🎉 সব শেষ!")
    print(f"  📸 Enhanced ছবি  : {out_img}")
    print(f"  🔲 Comparison    : {out_cmp}")
    print(f"\n⚠️  Disclaimer: AI demo। ফলাফল ছবির উপর নির্ভর করে।")

if __name__ == "__main__":
    main()