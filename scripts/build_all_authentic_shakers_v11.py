import os
import math
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
BRANDING_DIR = os.path.join(BASE_DIR, 'public', 'images', 'branding')

# Typography
try:
    font_brand = ImageFont.truetype('arialbd.ttf', 26)
    font_sub = ImageFont.truetype('arial.ttf', 13)
except:
    font_brand = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# -------------------------------------------------------------------------
# Step 1: Extract authentic KrowN Construction logo from Tumbler
# -------------------------------------------------------------------------
def get_authentic_kc_logo():
    tumbler = Image.open(os.path.join(PROD_DIR, 'krown-construction-jobsite-tumbler.jpg')).convert('RGB')
    logo_crop = tumbler.crop((330, 300, 690, 600))
    arr = np.array(logo_crop, dtype=np.float32)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # Gold detection with smooth alpha
    gold_val = np.maximum(0.0, np.minimum(r - b - 15.0, g - b - 8.0))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    alpha_raw = np.clip((gold_val / 24.0) * (lum / 55.0), 0.0, 1.0)

    # Bounding box of the logo
    mask = np.zeros_like(alpha_raw)
    mask[35:295, 40:325] = alpha_raw[35:295, 40:325]

    # Vibrant High-Vis Safety Gold / Rich Metallic Gold
    gold_rgba = np.zeros((300, 360, 4), dtype=np.uint8)
    gold_rgba[:, :, 0] = np.clip(r * 1.25 + 30, 0, 255).astype(np.uint8)
    gold_rgba[:, :, 1] = np.clip(g * 1.20 + 20, 0, 255).astype(np.uint8)
    gold_rgba[:, :, 2] = np.clip(b * 0.70, 0, 255).astype(np.uint8)
    gold_rgba[:, :, 3] = (mask * 255.0).astype(np.uint8)

    img_rgba = Image.fromarray(gold_rgba, mode='RGBA')
    bbox = img_rgba.getbbox()
    return img_rgba.crop(bbox)

# -------------------------------------------------------------------------
# Helper: Clean Shaker Body Chest on 1024x1024 genuine shaker images
# -------------------------------------------------------------------------
def clean_blackout_shaker(base_img):
    arr = np.array(base_img, dtype=np.float32)
    clean_arr = arr.copy()
    top_prof = np.mean(arr[455:470, :, :], axis=0)
    bot_prof = np.mean(arr[915:930, :, :], axis=0)

    np.random.seed(42)
    for y in range(465, 925):
        t = (y - 465) / (925 - 465)
        row_est = (1.0 - t) * top_prof + t * bot_prof
        noise = np.random.normal(0, 0.9, size=(1024, 3))
        clean_row = np.clip(row_est + noise, 0, 255)
        for x in range(375, 646):
            edge_dist = min(x - 375, 646 - x, y - 465, 925 - y)
            w_blend = min(1.0, edge_dist / 6.0)
            clean_arr[y, x] = (1.0 - w_blend) * clean_arr[y, x] + w_blend * clean_row[x]

    # Neutralize purple collar on cap (x: 380..635, y: 180..380)
    for y in range(180, 380):
        for x in range(380, 635):
            r, g, b = clean_arr[y, x]
            if b > g + 8 and b > 40:
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.88, lum * 0.88, lum * 0.92]

    return clean_arr

def clean_steel_shaker(base_img):
    arr = np.array(base_img, dtype=np.float32)
    clean_arr = arr.copy()
    top_prof = np.mean(arr[420:435, :, :], axis=0)
    bot_prof = np.mean(arr[885:900, :, :], axis=0)

    np.random.seed(42)
    for y in range(435, 895):
        t = (y - 435) / (895 - 435)
        row_est = (1.0 - t) * top_prof + t * bot_prof
        noise = np.random.normal(0, 1.4, size=(1024, 3))
        clean_row = np.clip(row_est + noise, 0, 255)
        for x in range(360, 640):
            edge_dist = min(x - 360, 640 - x, y - 435, 895 - y)
            w_blend = min(1.0, edge_dist / 7.0)
            clean_arr[y, x] = (1.0 - w_blend) * clean_arr[y, x] + w_blend * clean_row[x]

    # Desaturate green loop & purple collar on cap
    for y in range(160, 460):
        for x in range(295, 650):
            r, g, b = clean_arr[y, x]
            if g > 55 and g > r * 1.08 and g > b * 1.08:
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.42, lum * 0.42, lum * 0.45]
            elif y >= 220 and y <= 380 and (b > g + 10 or (b > 60 and r > 50 and g < 75)):
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.82, lum * 0.82, lum * 0.86]

    return clean_arr

def clean_tritan_shaker(base_img):
    arr = np.array(base_img, dtype=np.float32)
    clean_arr = arr.copy()
    top_prof = np.mean(arr[420:435, :, :], axis=0)
    bot_prof = np.mean(arr[890:905, :, :], axis=0)

    np.random.seed(42)
    for y in range(435, 895):
        t = (y - 435) / (895 - 435)
        row_est = (1.0 - t) * top_prof + t * bot_prof
        noise = np.random.normal(0, 1.1, size=(1024, 3))
        clean_row = np.clip(row_est + noise, 0, 255)
        for x in range(360, 638):
            edge_dist = min(x - 360, 638 - x, y - 435, 895 - y)
            w_blend = min(1.0, edge_dist / 7.0)
            clean_arr[y, x] = (1.0 - w_blend) * clean_arr[y, x] + w_blend * clean_row[x]

    return clean_arr

# -------------------------------------------------------------------------
# KC SHAKERS (kc-shaker-01)
# -------------------------------------------------------------------------
def build_kc_highvis(kc_logo):
    print("Building Authentic KC High-Vis Safety Gold & Matte Black Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-steel-clean.jpg')).convert('RGB')
    clean_arr = clean_blackout_shaker(base)

    # User Request: "make yellow or gold accents on the top cover/cap"
    for y in range(225, 290):
        for x in range(482, 538):
            r, g, b = clean_arr[y, x]
            lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
            edge_dist = min(x - 482, 538 - x, y - 225, 290 - y)
            alpha = min(1.0, edge_dist / 3.0)
            gold_r = np.clip(245 * lum + 35, 0, 255)
            gold_g = np.clip(195 * lum + 20, 0, 255)
            gold_b = np.clip(25 * lum + 5, 0, 255)
            clean_arr[y, x] = (1.0 - alpha * 0.85) * clean_arr[y, x] + (alpha * 0.85) * np.array([gold_r, gold_g, gold_b])

    # Subtle safety gold pinstripe accent on collar
    for y in range(358, 366):
        for x in range(395, 625):
            r, g, b = clean_arr[y, x]
            norm_x = (x - 395) / (625 - 395)
            cyl_shade = math.sin(norm_x * math.pi)
            clean_arr[y, x] = [
                int(np.clip(r * 0.3 + 220 * cyl_shade, 0, 255)),
                int(np.clip(g * 0.3 + 175 * cyl_shade, 0, 255)),
                int(np.clip(b * 0.3 + 20 * cyl_shade, 0, 255))
            ]

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    # Composite KC logo
    target_w = 185
    aspect = kc_logo.height / kc_logo.width
    target_h = int(target_w * aspect)
    logo_resized = kc_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)

    pos_x = 510 - target_w // 2
    pos_y = 520

    logo_np = np.array(logo_resized, dtype=np.float32)
    for x in range(target_w):
        norm_x = (x - target_w / 2.0) / (target_w / 2.0)
        shade = 0.90 + 0.22 * math.cos(norm_x * 0.8) - 0.05 * norm_x
        logo_np[:, x, :3] = np.clip(logo_np[:, x, :3] * shade, 0, 255)

    logo_styled = Image.fromarray(logo_np.astype(np.uint8), mode='RGBA')

    # Drop shadow
    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    logo_alpha = logo_styled.split()[3]
    shadow_mask = logo_alpha.filter(ImageFilter.GaussianBlur(radius=3.5))
    l_shadow = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 175))
    l_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(l_shadow, (pos_x + 1, pos_y + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(logo_styled, (pos_x, pos_y), mask=logo_alpha)

    return bottle.convert('RGB')

def build_kc_steelcore(kc_logo):
    print("Building Authentic KC Industrial Steel & Concrete Grey Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-signature-steel-clean.jpg')).convert('RGB')
    clean_arr = clean_steel_shaker(base)

    # Gold accent to the latch
    for y in range(220, 285):
        for x in range(470, 525):
            r, g, b = clean_arr[y, x]
            lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
            edge_dist = min(x - 470, 525 - x, y - 220, 285 - y)
            alpha = min(1.0, edge_dist / 3.0)
            gold_r = np.clip(240 * lum + 30, 0, 255)
            gold_g = np.clip(190 * lum + 15, 0, 255)
            gold_b = np.clip(25 * lum + 5, 0, 255)
            clean_arr[y, x] = (1.0 - alpha * 0.8) * clean_arr[y, x] + (alpha * 0.8) * np.array([gold_r, gold_g, gold_b])

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    target_w = 185
    aspect = kc_logo.height / kc_logo.width
    target_h = int(target_w * aspect)
    logo_resized = kc_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)

    pos_x = 495 - target_w // 2
    pos_y = 515

    logo_np = np.array(logo_resized, dtype=np.float32)
    for x in range(target_w):
        norm_x = (x - target_w / 2.0) / (target_w / 2.0)
        shade = 0.90 + 0.28 * math.cos(norm_x * 0.85) - 0.04 * norm_x
        logo_np[:, x, :3] = np.clip(logo_np[:, x, :3] * shade, 0, 255)

    logo_styled = Image.fromarray(logo_np.astype(np.uint8), mode='RGBA')

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    logo_alpha = logo_styled.split()[3]
    shadow_mask = logo_alpha.filter(ImageFilter.GaussianBlur(radius=3.0))
    l_shadow = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 160))
    l_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(l_shadow, (pos_x + 1, pos_y + 2), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(logo_styled, (pos_x, pos_y), mask=logo_alpha)

    return bottle.convert('RGB')

def build_kc_tradesman(kc_logo):
    print("Building Authentic KC Tradesman Heavy-Duty Obsidian Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-steel-clean.jpg')).convert('RGB')
    clean_arr = clean_blackout_shaker(base)

    # Antique bronze gold latch accent
    for y in range(225, 290):
        for x in range(482, 538):
            r, g, b = clean_arr[y, x]
            lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
            edge_dist = min(x - 482, 538 - x, y - 225, 290 - y)
            alpha = min(1.0, edge_dist / 3.0)
            bronze_r = np.clip(210 * lum + 25, 0, 255)
            bronze_g = np.clip(160 * lum + 15, 0, 255)
            bronze_b = np.clip(35 * lum + 5, 0, 255)
            clean_arr[y, x] = (1.0 - alpha * 0.75) * clean_arr[y, x] + (alpha * 0.75) * np.array([bronze_r, bronze_g, bronze_b])

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    target_w = 185
    aspect = kc_logo.height / kc_logo.width
    target_h = int(target_w * aspect)
    logo_resized = kc_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)

    pos_x = 510 - target_w // 2
    pos_y = 520

    logo_np = np.array(logo_resized, dtype=np.float32)
    for x in range(target_w):
        norm_x = (x - target_w / 2.0) / (target_w / 2.0)
        shade = 0.88 + 0.22 * math.cos(norm_x * 0.8) - 0.05 * norm_x
        logo_np[:, x, 0] = np.clip(logo_np[:, x, 0] * shade * 0.95, 0, 255)
        logo_np[:, x, 1] = np.clip(logo_np[:, x, 1] * shade * 0.88, 0, 255)
        logo_np[:, x, 2] = np.clip(logo_np[:, x, 2] * shade * 0.80, 0, 255)

    logo_styled = Image.fromarray(logo_np.astype(np.uint8), mode='RGBA')

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    logo_alpha = logo_styled.split()[3]
    shadow_mask = logo_alpha.filter(ImageFilter.GaussianBlur(radius=3.5))
    l_shadow = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 185))
    l_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(l_shadow, (pos_x + 1, pos_y + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(logo_styled, (pos_x, pos_y), mask=logo_alpha)

    return bottle.convert('RGB')

# -------------------------------------------------------------------------
# KROWNSUPPLY CO LUXURY SHAKERS (krown-shaker-01)
# -------------------------------------------------------------------------
crown_img = Image.open(os.path.join(BRANDING_DIR, 'krown_geometric_crown_transparent_alpha.png')).convert('RGBA')

def build_krown_obsidian():
    print("Building KrowN Supply Co. Luxury Matte Obsidian Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-steel-clean.jpg')).convert('RGB')
    clean_arr = clean_blackout_shaker(base)
    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    target_cw = 145
    target_ch = int(target_cw * crown_img.height / crown_img.width)
    crown_resized = crown_img.resize((target_cw, target_ch), Image.Resampling.LANCZOS)
    crown_x = 510 - target_cw // 2
    crown_y = 515

    crown_np = np.array(crown_resized, dtype=np.float32)
    for x in range(target_cw):
        norm_x = (x - target_cw / 2.0) / (target_cw / 2.0)
        shade = 0.88 + 0.24 * math.cos(norm_x * 0.8) - 0.06 * norm_x
        crown_np[:, x, :3] = np.clip(crown_np[:, x, :3] * shade, 0, 255)

    crown_styled = Image.fromarray(crown_np.astype(np.uint8), mode='RGBA')

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    crown_alpha = crown_styled.split()[3]
    shadow_mask = crown_alpha.filter(ImageFilter.GaussianBlur(radius=4.0))
    c_shadow = Image.new('RGBA', (target_cw, target_ch), (0, 0, 0, 150))
    c_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(c_shadow, (crown_x + 1, crown_y + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(crown_styled, (crown_x, crown_y), mask=crown_styled.split()[3])

    text_layer = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)
    text_brand = 'K  R  O  W  N'
    text_sub = 'S U P P L Y   C O .'

    bbox1 = draw.textbbox((0, 0), text_brand, font=font_brand)
    tw1 = bbox1[2] - bbox1[0]
    tx1 = 510 - tw1 // 2
    ty1 = crown_y + target_ch + 20

    draw.text((tx1 + 1, ty1 + 1), text_brand, fill=(5, 5, 5, 180), font=font_brand)
    draw.text((tx1, ty1), text_brand, fill=(218, 182, 60, 255), font=font_brand)
    draw.text((tx1, ty1 - 1), text_brand, fill=(245, 225, 140, 160), font=font_brand)

    bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = 510 - tw2 // 2
    ty2 = ty1 + 34

    draw.text((tx2 + 1, ty2 + 1), text_sub, fill=(5, 5, 5, 160), font=font_sub)
    draw.text((tx2, ty2), text_sub, fill=(205, 175, 80, 240), font=font_sub)

    return Image.alpha_composite(bottle, text_layer).convert('RGB')

def build_krown_smoke():
    print("Building KrowN Supply Co. Luxury Frosted Smoke Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-tritan-clean.jpg')).convert('RGB')
    clean_arr = clean_tritan_shaker(base)
    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    target_cw = 145
    target_ch = int(target_cw * crown_img.height / crown_img.width)
    crown_resized = crown_img.resize((target_cw, target_ch), Image.Resampling.LANCZOS)
    crown_x = 495 - target_cw // 2
    crown_y = 505

    crown_np = np.array(crown_resized, dtype=np.float32)
    for x in range(target_cw):
        norm_x = (x - target_cw / 2.0) / (target_cw / 2.0)
        shade = 0.86 + 0.25 * math.cos(norm_x * 0.8) - 0.05 * norm_x
        crown_np[:, x, :3] = np.clip(crown_np[:, x, :3] * shade, 0, 255)

    crown_styled = Image.fromarray(crown_np.astype(np.uint8), mode='RGBA')

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    crown_alpha = crown_styled.split()[3]
    shadow_mask = crown_alpha.filter(ImageFilter.GaussianBlur(radius=3.5))
    c_shadow = Image.new('RGBA', (target_cw, target_ch), (0, 0, 0, 130))
    c_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(c_shadow, (crown_x + 1, crown_y + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(crown_styled, (crown_x, crown_y), mask=crown_styled.split()[3])

    text_layer = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)
    text_brand = 'K  R  O  W  N'
    text_sub = 'S U P P L Y   C O .'

    bbox1 = draw.textbbox((0, 0), text_brand, font=font_brand)
    tw1 = bbox1[2] - bbox1[0]
    tx1 = 495 - tw1 // 2
    ty1 = crown_y + target_ch + 20

    draw.text((tx1 + 1, ty1 + 1), text_brand, fill=(5, 5, 5, 170), font=font_brand)
    draw.text((tx1, ty1), text_brand, fill=(218, 182, 60, 255), font=font_brand)
    draw.text((tx1, ty1 - 1), text_brand, fill=(245, 225, 140, 160), font=font_brand)

    bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = 495 - tw2 // 2
    ty2 = ty1 + 34

    draw.text((tx2 + 1, ty2 + 1), text_sub, fill=(5, 5, 5, 150), font=font_sub)
    draw.text((tx2, ty2), text_sub, fill=(205, 175, 80, 240), font=font_sub)

    return Image.alpha_composite(bottle, text_layer).convert('RGB')

def build_krown_brushed():
    print("Building KrowN Supply Co. Luxury Raw Brushed Steel Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-signature-steel-clean.jpg')).convert('RGB')
    clean_arr = clean_steel_shaker(base)
    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    target_cw = 145
    target_ch = int(target_cw * crown_img.height / crown_img.width)
    crown_resized = crown_img.resize((target_cw, target_ch), Image.Resampling.LANCZOS)
    crown_x = 495 - target_cw // 2
    crown_y = 510

    crown_np = np.array(crown_resized, dtype=np.float32)
    for x in range(target_cw):
        norm_x = (x - target_cw / 2.0) / (target_cw / 2.0)
        shade = 0.90 + 0.28 * math.cos(norm_x * 0.85) - 0.04 * norm_x
        crown_np[:, x, :3] = np.clip(crown_np[:, x, :3] * shade, 0, 255)

    crown_styled = Image.fromarray(crown_np.astype(np.uint8), mode='RGBA')

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    crown_alpha = crown_styled.split()[3]
    shadow_mask = crown_alpha.filter(ImageFilter.GaussianBlur(radius=3.0))
    c_shadow = Image.new('RGBA', (target_cw, target_ch), (0, 0, 0, 140))
    c_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(c_shadow, (crown_x + 1, crown_y + 2), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(crown_styled, (crown_x, crown_y), mask=crown_styled.split()[3])

    text_layer = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)
    text_brand = 'K  R  O  W  N'
    text_sub = 'S U P P L Y   C O .'

    bbox1 = draw.textbbox((0, 0), text_brand, font=font_brand)
    tw1 = bbox1[2] - bbox1[0]
    tx1 = 495 - tw1 // 2
    ty1 = crown_y + target_ch + 20

    draw.text((tx1 + 1, ty1 + 1), text_brand, fill=(10, 12, 16, 200), font=font_brand)
    draw.text((tx1, ty1), text_brand, fill=(220, 185, 65, 255), font=font_brand)
    draw.text((tx1, ty1 - 1), text_brand, fill=(250, 235, 160, 180), font=font_brand)

    bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = 495 - tw2 // 2
    ty2 = ty1 + 34

    draw.text((tx2 + 1, ty2 + 1), text_sub, fill=(10, 12, 16, 180), font=font_sub)
    draw.text((tx2, ty2), text_sub, fill=(210, 180, 85, 240), font=font_sub)

    return Image.alpha_composite(bottle, text_layer).convert('RGB')

# -------------------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------------------
if __name__ == '__main__':
    kc_logo = get_authentic_kc_logo()

    # Build KC Shakers (v11)
    kc_hv = build_kc_highvis(kc_logo)
    kc_sc = build_kc_steelcore(kc_logo)
    kc_tb = build_kc_tradesman(kc_logo)

    kc_hv.save(os.path.join(PROD_DIR, 'kc-shaker-photoreal-v11.jpg'), quality=96)
    kc_sc.save(os.path.join(PROD_DIR, 'kc-shaker-steelcore-v11.jpg'), quality=96)
    kc_tb.save(os.path.join(PROD_DIR, 'kc-shaker-tradesman-v11.jpg'), quality=96)

    # KC 3-bottle lineup
    kc_lineup = Image.new('RGB', (1600, 1000), (12, 14, 18))
    k1_sm = kc_hv.resize((620, 620), Image.Resampling.LANCZOS)
    k2_sm = kc_tb.resize((620, 620), Image.Resampling.LANCZOS)
    k3_sm = kc_sc.resize((620, 620), Image.Resampling.LANCZOS)
    kc_lineup.paste(k1_sm, (-30, 200))
    kc_lineup.paste(k2_sm, (490, 200))
    kc_lineup.paste(k3_sm, (1010, 200))
    kc_lineup.save(os.path.join(PROD_DIR, 'kc-shaker-bottles-3-editions-v11.jpg'), quality=96)

    print("SUCCESS: Generated KC Shakers (v11)!")

    # Build KrowN Supply Co. Luxury Shakers (v11)
    krown_obs = build_krown_obsidian()
    krown_smk = build_krown_smoke()
    krown_brs = build_krown_brushed()

    krown_obs.save(os.path.join(PROD_DIR, 'krown-shaker-photoreal-v11.jpg'), quality=96)
    krown_smk.save(os.path.join(PROD_DIR, 'krown-shaker-smoke-v11.jpg'), quality=96)
    krown_brs.save(os.path.join(PROD_DIR, 'krown-shaker-brushed-v11.jpg'), quality=96)

    # KrowN 3-bottle lineup
    krown_lineup = Image.new('RGB', (1600, 1000), (12, 14, 18))
    kr1_sm = krown_obs.resize((620, 620), Image.Resampling.LANCZOS)
    kr2_sm = krown_smk.resize((620, 620), Image.Resampling.LANCZOS)
    kr3_sm = krown_brs.resize((620, 620), Image.Resampling.LANCZOS)
    krown_lineup.paste(kr1_sm, (-30, 200))
    krown_lineup.paste(kr2_sm, (490, 200))
    krown_lineup.paste(kr3_sm, (1010, 200))
    krown_lineup.save(os.path.join(PROD_DIR, 'krown-shaker-bottles-3-editions-v11.jpg'), quality=96)

    print("SUCCESS: Generated KrowN Supply Co. Shakers (v11)!")
