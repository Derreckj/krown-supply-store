import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont, ImageFilter

output_dir = "etsy_store_assets"
os.makedirs(output_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. ETSY SHOP ICON (1000x1000 & 500x500)
# -------------------------------------------------------------
print("Generating Etsy Shop Icons...")
logo_src = "public/images/branding/krown-definitive-logo.png"
if not os.path.exists(logo_src):
    logo_src = "public/images/branding/krown-supply-co-icon-mark.jpg"

src_im = Image.open(logo_src).convert("RGBA")

# Create 1000x1000 canvas with premium matte black
icon_1000 = Image.new("RGBA", (1000, 1000), (12, 12, 14, 255))
draw_icon = ImageDraw.Draw(icon_1000)

# Subtle radial gradient / vignette
for r in range(500, 0, -5):
    alpha = int(25 * (1 - r / 500))
    draw_icon.ellipse([500 - r, 500 - r, 500 + r, 500 + r], fill=(22, 22, 26, 255))

# Resize source logo to 740x740 to ensure safe circular cropping for Etsy
logo_resized = src_im.resize((740, 740), Image.Resampling.LANCZOS)
icon_1000.paste(logo_resized, (130, 130), logo_resized if logo_resized.mode == 'RGBA' else None)

# Add subtle inner border
draw_icon.rectangle([0, 0, 999, 999], outline=(40, 40, 48), width=2)

icon_1000_rgb = icon_1000.convert("RGB")
icon_1000_path = os.path.join(output_dir, "01_ETSY_SHOP_ICON_1000x1000.jpg")
icon_1000_rgb.save(icon_1000_path, quality=98)

icon_500_path = os.path.join(output_dir, "01_ETSY_SHOP_ICON_500x500.jpg")
icon_1000_rgb.resize((500, 500), Image.Resampling.LANCZOS).save(icon_500_path, quality=98)
print(f"  ✓ Saved: {icon_500_path}")
print(f"  ✓ Saved: {icon_1000_path}")

# -------------------------------------------------------------
# 2. ETSY BIG COVER BANNER (1600x400 & 1200x300)
# -------------------------------------------------------------
print("\nGenerating Etsy Shop Cover Banners...")
banner_w, banner_h = 1600, 400
banner = Image.new("RGBA", (banner_w, banner_h), (10, 10, 12, 255))
b_draw = ImageDraw.Draw(banner)

# Add subtle industrial grid / gradient lines
for x in range(0, banner_w, 40):
    b_draw.line([(x, 0), (x, banner_h)], fill=(16, 16, 20), width=1)
for y in range(0, banner_h, 40):
    b_draw.line([(0, y), (banner_w, y)], fill=(16, 16, 20), width=1)

# Subtle center glow
for r in range(400, 0, -10):
    b_draw.ellipse([800 - r * 2, 200 - r, 800 + r * 2, 200 + r], fill=(22, 22, 28, 255))

# Paste KrowN gold crest in center
crest_size = 220
crest_im = src_im.resize((crest_size, crest_size), Image.Resampling.LANCZOS)
banner.paste(crest_im, (banner_w // 2 - crest_size // 2, 35), crest_im if crest_im.mode == 'RGBA' else None)

# Add typography via clean drawing
# Slogan & Brand Title
try:
    font_title = ImageFont.truetype("arialbd.ttf", 36)
    font_sub = ImageFont.truetype("arial.ttf", 16)
    font_tags = ImageFont.truetype("arialbd.ttf", 14)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_tags = ImageFont.load_default()

# Title text
title_text = "K R O W N   S U P P L Y   C O."
sub_text = "BUILT TO REIGN  •  EST. 2024"
tags_text = "TRADESMAN GEAR  |  LUXURY STREETWEAR  |  PRO ESPORTS APPAREL"

# Center title
bbox_t = b_draw.textbbox((0, 0), title_text, font=font_title)
tw = bbox_t[2] - bbox_t[0]
b_draw.text(((banner_w - tw) // 2, 265), title_text, fill=(245, 245, 248), font=font_title)

# Center sub
bbox_s = b_draw.textbbox((0, 0), sub_text, font=font_sub)
sw = bbox_s[2] - bbox_s[0]
b_draw.text(((banner_w - sw) // 2, 312), sub_text, fill=(212, 175, 55), font=font_sub)

# Center tags
bbox_tags = b_draw.textbbox((0, 0), tags_text, font=font_tags)
gw = bbox_tags[2] - bbox_tags[0]
b_draw.text(((banner_w - gw) // 2, 345), tags_text, fill=(150, 155, 165), font=font_tags)

banner_rgb = banner.convert("RGB")
banner_1600_path = os.path.join(output_dir, "02_ETSY_COVER_BANNER_1600x400.jpg")
banner_rgb.save(banner_1600_path, quality=98)

banner_1200_path = os.path.join(output_dir, "02_ETSY_COVER_BANNER_1200x300.jpg")
banner_rgb.resize((1200, 300), Image.Resampling.LANCZOS).save(banner_1200_path, quality=98)
print(f"  ✓ Saved: {banner_1600_path}")
print(f"  ✓ Saved: {banner_1200_path}")

# -------------------------------------------------------------
# 3. ETSY MINI BANNER (1200x160)
# -------------------------------------------------------------
mini_w, mini_h = 1200, 160
mini = Image.new("RGB", (mini_w, mini_h), (12, 12, 15))
m_draw = ImageDraw.Draw(mini)

mini_crest = src_im.resize((110, 110), Image.Resampling.LANCZOS)
mini.paste(mini_crest, (40, 25), mini_crest if mini_crest.mode == 'RGBA' else None)

try:
    f_mini_t = ImageFont.truetype("arialbd.ttf", 28)
    f_mini_s = ImageFont.truetype("arial.ttf", 15)
except Exception:
    f_mini_t = ImageFont.load_default()
    f_mini_s = ImageFont.load_default()

m_draw.text((170, 45), "KROW'N SUPPLY CO.", fill=(245, 245, 245), font=f_mini_t)
m_draw.text((170, 85), "BUILT TO REIGN  •  OFFICIAL ETSY FLAGSHIP STORE", fill=(212, 175, 55), font=f_mini_s)

mini_path = os.path.join(output_dir, "03_ETSY_MINI_BANNER_1200x160.jpg")
mini.save(mini_path, quality=98)
print(f"  ✓ Saved: {mini_path}")

print("\n=== ETSY BRANDING ASSETS READY ===")
