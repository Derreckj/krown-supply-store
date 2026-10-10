import os
import sys
import io
import shutil
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

base_dir = "etsy_store_assets"
branding_dir = os.path.join(base_dir, "01_STORE_BRANDING")
listing_dir = os.path.join(base_dir, "02_LISTING_PHOTO_PACKS")

os.makedirs(branding_dir, exist_ok=True)
os.makedirs(listing_dir, exist_ok=True)

# Move branding assets into 01_STORE_BRANDING
for f in os.listdir(base_dir):
    if f.startswith("0") and f.endswith(".jpg"):
        shutil.move(os.path.join(base_dir, f), os.path.join(branding_dir, f))

# 1. Hoodie Photos
hoodie_dir = os.path.join(listing_dir, "HOODIE_480GSM")
os.makedirs(hoodie_dir, exist_ok=True)
shutil.copy("public/images/products/krown-supply-premium-hoodie-front.jpg", os.path.join(hoodie_dir, "Photo_1_Front_Chest_Gold_Crest.jpg"))
shutil.copy("public/images/products/krown-heavyweight-hoodie-back-krown.jpg", os.path.join(hoodie_dir, "Photo_2_Back_Official_KrowN_Statement.jpg"))
if os.path.exists("public/images/products/krown-boxy-heavy-hoodie-mineral-wash.jpg"):
    shutil.copy("public/images/products/krown-boxy-heavy-hoodie-mineral-wash.jpg", os.path.join(hoodie_dir, "Photo_3_Mineral_Wash_Texture.jpg"))

# 2. Tumbler Photos
tumbler_dir = os.path.join(listing_dir, "TUMBLER_20OZ")
os.makedirs(tumbler_dir, exist_ok=True)
shutil.copy("public/images/products/krown-construction-jobsite-tumbler.jpg", os.path.join(tumbler_dir, "Photo_1_Front_Laser_Gold_Crest.jpg"))
if os.path.exists("public/images/products/krown-construction-jobsite-tumbler-32oz.jpg"):
    shutil.copy("public/images/products/krown-construction-jobsite-tumbler-32oz.jpg", os.path.join(tumbler_dir, "Photo_2_Alternative_Angle.jpg"))

# Generate Tumbler Infographic Slide (Photo 3)
info_im = Image.new("RGB", (1000, 1000), (14, 14, 18))
draw = ImageDraw.Draw(info_im)
draw.rectangle([20, 20, 980, 980], outline=(212, 175, 55), width=2)

try:
    font_h = ImageFont.truetype("arialbd.ttf", 40)
    font_sub = ImageFont.truetype("arial.ttf", 22)
    font_body = ImageFont.truetype("arialbd.ttf", 26)
except Exception:
    font_h = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_body = ImageFont.load_default()

draw.text((80, 60), "KROW'N CONSTRUCTION LLC", fill=(212, 175, 55), font=font_h)
draw.text((80, 115), "20oz VACUUM INSULATED JOBSITE TUMBLER SPECIFICATIONS", fill=(180, 185, 195), font=font_sub)

features = [
    ("❄️ 24 HOURS ICE COLD", "Double-wall vacuum insulation keeps ice frozen through grueling shifts."),
    ("🔥 8 HOURS PIPING HOT", "Maintains optimal drinking temperature for fresh morning coffee."),
    ("🛡️ 18/8 KITCHEN-GRADE STEEL", "Pure 304 food-grade stainless steel body that resists rust, dents, and punctures."),
    ("☕ SPLASH-RESISTANT LID", "Crystal-clear slider lid engineered for vehicle cup holders and glove operation."),
    ("✨ PRECISION LASER ETCHED", "Permanent gold metallic emblem that will never peel, fade, or wash off.")
]

y_pos = 200
for title, desc in features:
    draw.text((80, y_pos), title, fill=(245, 245, 250), font=font_body)
    draw.text((80, y_pos + 38), desc, fill=(160, 165, 175), font=font_sub)
    draw.line([(80, y_pos + 85), (920, y_pos + 85)], fill=(35, 35, 45), width=1)
    y_pos += 120

draw.text((80, 890), "BUILT TO REIGN  •  JOB-SITE TESTED  •  BPA FREE", fill=(212, 175, 55), font=font_sub)
info_im.save(os.path.join(tumbler_dir, "Photo_3_Jobsite_Specifications_Infographic.jpg"), quality=95)

# 3. Desk Mat Photos
desk_dir = os.path.join(listing_dir, "DESK_MAT_32x16")
os.makedirs(desk_dir, exist_ok=True)
shutil.copy("public/images/products/axiom-owl-desk-mat-photorealistic.jpg", os.path.join(desk_dir, "Photo_1_BattleStation_Perspective.jpg"))

# Generate Desk Mat Infographic Slide (Photo 2)
mat_info = Image.new("RGB", (1000, 1000), (12, 14, 20))
m_draw = ImageDraw.Draw(mat_info)
m_draw.rectangle([20, 20, 980, 980], outline=(0, 230, 255), width=2)

m_draw.text((80, 60), "AXIOM ALLEGIANCE // AXA", fill=(0, 230, 255), font=font_h)
m_draw.text((80, 115), "PANORAMIC GAMING DESK MAT (32\" x 16\") SPECIFICATIONS", fill=(180, 185, 195), font=font_sub)

mat_features = [
    ("⚡ EXTENDED 32\" x 16\" XL SIZE", "Generous footprint accommodates both full mechanical keyboard & gaming mouse."),
    ("🎯 MICRO-TEXTURED CLOTH SURFACE", "Engineered for optical tracking precision and frictionless mouse glides."),
    ("🔒 ANTI-FRAY PRECISION EDGES", "Tight perimeter stitching prevents edge fraying and surface peeling."),
    ("🛑 NON-SLIP NATURAL RUBBER BASE", "Heavy-grip herringbone rubber base stays rooted to glass, wood, and metal desks."),
    ("💦 WATER-RESISTANT COATING", "Hydrophobic surface repels accidental drink spills for effortless wipe-down.")
]

y_pos = 200
for title, desc in mat_features:
    m_draw.text((80, y_pos), title, fill=(245, 245, 250), font=font_body)
    m_draw.text((80, y_pos + 38), desc, fill=(160, 165, 175), font=font_sub)
    m_draw.line([(80, y_pos + 85), (920, y_pos + 85)], fill=(25, 35, 55), width=1)
    y_pos += 120

m_draw.text((80, 890), "PLAY TO REIGN  •  TOURNAMENT GRADE  •  PRO ESPORTS", fill=(0, 230, 255), font=font_sub)
mat_info.save(os.path.join(desk_dir, "Photo_2_Gaming_Specs_Infographic.jpg"), quality=95)

print("All listing photo packs and infographics organized successfully!")
