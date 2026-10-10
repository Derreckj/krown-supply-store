import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')
BRANDING_DIR = os.path.join(BASE_DIR, 'public', 'images', 'branding')
CONST_DIR = os.path.join(BRANDING_DIR, 'construction')

os.makedirs(PROD_DIR, exist_ok=True)
os.makedirs(MASTERS_DIR, exist_ok=True)

# Typography
try:
    font_brand = ImageFont.truetype('arialbd.ttf', 26)
    font_sub = ImageFont.truetype('arial.ttf', 13)
    font_kc_main = ImageFont.truetype('impact.ttf', 30)
    font_kc_sub = ImageFont.truetype('arialbd.ttf', 14)
except:
    font_brand = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_kc_main = ImageFont.load_default()
    font_kc_sub = ImageFont.load_default()

crown_img = Image.open(os.path.join(BRANDING_DIR, 'krown_geometric_crown_transparent_alpha.png')).convert('RGBA')

# -------------------------------------------------------------------------
# 1. KROWNSUPPLY CO - MATTE OBSIDIAN BLACK SHAKER BOTTLE
# -------------------------------------------------------------------------
def build_krown_obsidian():
    print("Building KrowN Obsidian Shaker Bottle...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-steel-clean.jpg')).convert('RGB')
    arr = np.array(base, dtype=np.float32)

    # Inpaint body to remove owl completely
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

    # Desaturate purple collar on cap (only on bottle cap x: 380..635, y: 180..380)
    for y in range(180, 380):
        for x in range(380, 635):
            r, g, b = clean_arr[y, x]
            if b > g + 8 and b > 40:
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.88, lum * 0.88, lum * 0.92]

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    # 3D Gold Crown monogram
    target_cw = 145
    target_ch = int(target_cw * crown_img.height / crown_img.width)
    crown_resized = crown_img.resize((target_cw, target_ch), Image.Resampling.LANCZOS)

    crown_x = 510 - target_cw // 2
    crown_y = 515

    # Cylindrical lighting wrap
    crown_np = np.array(crown_resized, dtype=np.float32)
    for x in range(target_cw):
        norm_x = (x - target_cw / 2.0) / (target_cw / 2.0)
        shade = 0.88 + 0.24 * math.cos(norm_x * 0.8) - 0.06 * norm_x
        crown_np[:, x, :3] = np.clip(crown_np[:, x, :3] * shade, 0, 255)

    crown_styled = Image.fromarray(crown_np.astype(np.uint8), mode='RGBA')

    # Contact shadow
    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    crown_alpha = crown_styled.split()[3]
    shadow_mask = crown_alpha.filter(ImageFilter.GaussianBlur(radius=4.0))
    c_shadow = Image.new('RGBA', (target_cw, target_ch), (0, 0, 0, 150))
    c_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(c_shadow, (crown_x + 1, crown_y + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(crown_styled, (crown_x, crown_y), mask=crown_styled.split()[3])

    # Typography
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

# -------------------------------------------------------------------------
# 2. KROWNSUPPLY CO - FROSTED SMOKE TRITAN SHAKER BOTTLE
# -------------------------------------------------------------------------
def build_krown_smoke():
    print("Building KrowN Frosted Smoke Tritan Shaker Bottle...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-tritan-clean.jpg')).convert('RGB')
    arr = np.array(base, dtype=np.float32)

    clean_arr = arr.copy()
    top_prof = np.mean(arr[420:435, :, :], axis=0)
    bot_prof = np.mean(arr[890:905, :, :], axis=0)

    np.random.seed(42)
    # Clean entire owl including bottom tip
    for y in range(435, 895):
        t = (y - 435) / (895 - 435)
        row_est = (1.0 - t) * top_prof + t * bot_prof
        noise = np.random.normal(0, 1.1, size=(1024, 3))
        clean_row = np.clip(row_est + noise, 0, 255)
        # Protect measurement ticks on the right (x > 635)
        for x in range(360, 638):
            edge_dist = min(x - 360, 638 - x, y - 435, 895 - y)
            w_blend = min(1.0, edge_dist / 7.0)
            clean_arr[y, x] = (1.0 - w_blend) * clean_arr[y, x] + w_blend * clean_row[x]

    # Keep factory translucent smoke cap 100% pristine and smooth
    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    # Crown monogram
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

    # Drop shadow
    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    crown_alpha = crown_styled.split()[3]
    shadow_mask = crown_alpha.filter(ImageFilter.GaussianBlur(radius=3.5))
    c_shadow = Image.new('RGBA', (target_cw, target_ch), (0, 0, 0, 130))
    c_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(c_shadow, (crown_x + 1, crown_y + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(crown_styled, (crown_x, crown_y), mask=crown_styled.split()[3])

    # Typography
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

# -------------------------------------------------------------------------
# 3. KROWNSUPPLY CO - RAW BRUSHED STAINLESS STEEL SHAKER BOTTLE
# -------------------------------------------------------------------------
def build_krown_brushed():
    print("Building KrowN Raw Brushed Stainless Steel Shaker Bottle...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-signature-steel-clean.jpg')).convert('RGB')
    arr = np.array(base, dtype=np.float32)

    clean_arr = arr.copy()
    top_prof = np.mean(arr[420:435, :, :], axis=0)
    bot_prof = np.mean(arr[885:900, :, :], axis=0)

    np.random.seed(42)
    # Clean owl body entirely
    for y in range(435, 895):
        t = (y - 435) / (895 - 435)
        row_est = (1.0 - t) * top_prof + t * bot_prof
        noise = np.random.normal(0, 1.4, size=(1024, 3))
        clean_row = np.clip(row_est + noise, 0, 255)
        for x in range(360, 640):
            edge_dist = min(x - 360, 640 - x, y - 435, 895 - y)
            w_blend = min(1.0, edge_dist / 7.0)
            clean_arr[y, x] = (1.0 - w_blend) * clean_arr[y, x] + w_blend * clean_row[x]

    # Desaturate green loop & purple lid with precision color detection (0 background monitor change)
    for y in range(160, 460):
        for x in range(295, 650):
            r, g, b = clean_arr[y, x]
            # Green loop
            if g > 55 and g > r * 1.08 and g > b * 1.08:
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.42, lum * 0.42, lum * 0.45]
            # Purple collar
            elif y >= 220 and y <= 380 and (b > g + 10 or (b > 60 and r > 50 and g < 75)):
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.82, lum * 0.82, lum * 0.86]

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    # Laser-etched metallic monogram
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

    # Typography
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
# 4. KROWNS CONSTRUCTION SHAKERS (BUILT TO REIGN)
# -------------------------------------------------------------------------
def get_kc_gold_monogram():
    kc_img = Image.open(os.path.join(CONST_DIR, 'KC logo black and white.png')).convert('RGBA')
    w_kc, h_kc = kc_img.size
    kc_top = kc_img.crop((0, 0, w_kc, h_kc // 2))
    kc_np = np.array(kc_top, dtype=np.float32)
    mask = (kc_np[:, :, 0] > 100).astype(np.float32)
    
    kc_colored = np.zeros((kc_top.height, kc_top.width, 4), dtype=np.uint8)
    kc_colored[:, :, 0] = (240 * mask).astype(np.uint8)
    kc_colored[:, :, 1] = (195 * mask).astype(np.uint8)
    kc_colored[:, :, 2] = (30 * mask).astype(np.uint8)
    kc_colored[:, :, 3] = (255 * mask).astype(np.uint8)
    return Image.fromarray(kc_colored, mode='RGBA')

def build_kc_highvis():
    print("Building KrowN Construction High-Vis Safety Gold Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-steel-clean.jpg')).convert('RGB')
    arr = np.array(base, dtype=np.float32)

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

    # Desaturate purple collar on cap (x: 380..635, y: 180..380)
    for y in range(180, 380):
        for x in range(380, 635):
            r, g, b = clean_arr[y, x]
            if b > g + 8 and b > 40:
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.88, lum * 0.88, lum * 0.92]

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    kc_gold_img = get_kc_gold_monogram()
    target_kw = 125
    target_kh = int(target_kw * kc_gold_img.height / kc_gold_img.width)
    kc_resized = kc_gold_img.resize((target_kw, target_kh), Image.Resampling.LANCZOS)

    kx = 510 - target_kw // 2
    ky = 515

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    kc_alpha = kc_resized.split()[3]
    shadow_mask = kc_alpha.filter(ImageFilter.GaussianBlur(radius=3.5))
    k_shadow = Image.new('RGBA', (target_kw, target_kh), (0, 0, 0, 160))
    k_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(k_shadow, (kx + 1, ky + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(kc_resized, (kx, ky), mask=kc_alpha)

    # Typography
    text_layer = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)

    text_kc_title = 'KROWN CONSTRUCTION'
    text_kc_sub = 'BUILT TO REIGN'

    bbox1 = draw.textbbox((0, 0), text_kc_title, font=font_kc_main)
    tw1 = bbox1[2] - bbox1[0]
    tx1 = 510 - tw1 // 2
    ty1 = ky + target_kh + 18

    draw.text((tx1 + 1, ty1 + 1), text_kc_title, fill=(5, 5, 5, 180), font=font_kc_main)
    draw.text((tx1, ty1), text_kc_title, fill=(235, 190, 35, 255), font=font_kc_main)
    draw.text((tx1, ty1 - 1), text_kc_title, fill=(255, 225, 90, 180), font=font_kc_main)

    bbox2 = draw.textbbox((0, 0), text_kc_sub, font=font_kc_sub)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = 510 - tw2 // 2
    ty2 = ty1 + 36

    draw.text((tx2 + 1, ty2 + 1), text_kc_sub, fill=(5, 5, 5, 160), font=font_kc_sub)
    draw.text((tx2, ty2), text_kc_sub, fill=(210, 175, 45, 240), font=font_kc_sub)

    return Image.alpha_composite(bottle, text_layer).convert('RGB')

def build_kc_steelcore():
    print("Building KrowN Construction Industrial Steelcore Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-signature-steel-clean.jpg')).convert('RGB')
    arr = np.array(base, dtype=np.float32)

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

    # Precision lid desaturation
    for y in range(160, 460):
        for x in range(295, 650):
            r, g, b = clean_arr[y, x]
            if g > 55 and g > r * 1.08 and g > b * 1.08:
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.42, lum * 0.42, lum * 0.45]
            elif y >= 220 and y <= 380 and (b > g + 10 or (b > 60 and r > 50 and g < 75)):
                lum = r * 0.299 + g * 0.587 + b * 0.114
                clean_arr[y, x] = [lum * 0.82, lum * 0.82, lum * 0.86]

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    kc_gold_img = get_kc_gold_monogram()
    target_kw = 125
    target_kh = int(target_kw * kc_gold_img.height / kc_gold_img.width)
    kc_resized = kc_gold_img.resize((target_kw, target_kh), Image.Resampling.LANCZOS)

    kx = 495 - target_kw // 2
    ky = 510

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    kc_alpha = kc_resized.split()[3]
    shadow_mask = kc_alpha.filter(ImageFilter.GaussianBlur(radius=3.0))
    k_shadow = Image.new('RGBA', (target_kw, target_kh), (0, 0, 0, 150))
    k_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(k_shadow, (kx + 1, ky + 2), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(kc_resized, (kx, ky), mask=kc_alpha)

    # Typography
    text_layer = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)

    text_kc_title = 'KROWN CONSTRUCTION'
    text_kc_sub = 'BUILT TO REIGN'

    bbox1 = draw.textbbox((0, 0), text_kc_title, font=font_kc_main)
    tw1 = bbox1[2] - bbox1[0]
    tx1 = 495 - tw1 // 2
    ty1 = ky + target_kh + 18

    draw.text((tx1 + 1, ty1 + 1), text_kc_title, fill=(10, 12, 16, 200), font=font_kc_main)
    draw.text((tx1, ty1), text_kc_title, fill=(235, 190, 35, 255), font=font_kc_main)
    draw.text((tx1, ty1 - 1), text_kc_title, fill=(255, 225, 90, 180), font=font_kc_main)

    bbox2 = draw.textbbox((0, 0), text_kc_sub, font=font_kc_sub)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = 495 - tw2 // 2
    ty2 = ty1 + 36

    draw.text((tx2 + 1, ty2 + 1), text_kc_sub, fill=(10, 12, 16, 180), font=font_kc_sub)
    draw.text((tx2, ty2), text_kc_sub, fill=(210, 175, 45, 240), font=font_kc_sub)

    return Image.alpha_composite(bottle, text_layer).convert('RGB')

def build_kc_tradesman():
    print("Building KrowN Construction Tradesman Obsidian Shaker...")
    base = Image.open(os.path.join(PROD_DIR, 'axiom-shaker-stealth-tritan-clean.jpg')).convert('RGB')
    arr = np.array(base, dtype=np.float32)

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

    # Keep factory translucent smoke cap 100% pristine and smooth

    bottle = Image.fromarray(clean_arr.astype(np.uint8)).convert('RGBA')

    kc_gold_img = get_kc_gold_monogram()
    target_kw = 125
    target_kh = int(target_kw * kc_gold_img.height / kc_gold_img.width)
    kc_resized = kc_gold_img.resize((target_kw, target_kh), Image.Resampling.LANCZOS)

    kx = 495 - target_kw // 2
    ky = 505

    shadow_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    kc_alpha = kc_resized.split()[3]
    shadow_mask = kc_alpha.filter(ImageFilter.GaussianBlur(radius=3.5))
    k_shadow = Image.new('RGBA', (target_kw, target_kh), (0, 0, 0, 140))
    k_shadow.putalpha(shadow_mask)
    shadow_canvas.paste(k_shadow, (kx + 1, ky + 3), mask=shadow_mask)

    bottle = Image.alpha_composite(bottle, shadow_canvas)
    bottle.paste(kc_resized, (kx, ky), mask=kc_alpha)

    # Typography
    text_layer = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)

    text_kc_title = 'KROWN CONSTRUCTION'
    text_kc_sub = 'BUILT TO REIGN'

    bbox1 = draw.textbbox((0, 0), text_kc_title, font=font_kc_main)
    tw1 = bbox1[2] - bbox1[0]
    tx1 = 495 - tw1 // 2
    ty1 = ky + target_kh + 18

    draw.text((tx1 + 1, ty1 + 1), text_kc_title, fill=(5, 5, 5, 170), font=font_kc_main)
    draw.text((tx1, ty1), text_kc_title, fill=(235, 190, 35, 255), font=font_kc_main)
    draw.text((tx1, ty1 - 1), text_kc_title, fill=(255, 225, 90, 180), font=font_kc_main)

    bbox2 = draw.textbbox((0, 0), text_kc_sub, font=font_kc_sub)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = 495 - tw2 // 2
    ty2 = ty1 + 36

    draw.text((tx2 + 1, ty2 + 1), text_kc_sub, fill=(5, 5, 5, 150), font=font_kc_sub)
    draw.text((tx2, ty2), text_kc_sub, fill=(210, 175, 45, 240), font=font_kc_sub)

    return Image.alpha_composite(bottle, text_layer).convert('RGB')

# -------------------------------------------------------------------------
# EXECUTE ALL AND DEPLOY
# -------------------------------------------------------------------------
if __name__ == '__main__':
    # 1. KrowN Supply Co
    krown_obsidian = build_krown_obsidian()
    krown_smoke = build_krown_smoke()
    krown_brushed = build_krown_brushed()

    obsidian_targets = [
        'krown-shaker-photoreal-v6.jpg',
        'krown-shaker-obsidian-steel.jpg',
        'krown-shaker-obsidian-tritan.jpg',
        'krown-shaker-obsidian-steel-v2.jpg',
    ]
    for t in obsidian_targets:
        krown_obsidian.save(os.path.join(PROD_DIR, t), quality=96)
        krown_obsidian.save(os.path.join(MASTERS_DIR, t), quality=96)
        print(f"Deployed KrowN Obsidian: {t}")

    smoke_targets = [
        'krown-shaker-smoke-v6.jpg',
        'krown-shaker-smoke-steel.jpg',
        'krown-shaker-smoke-tritan.jpg',
    ]
    for t in smoke_targets:
        krown_smoke.save(os.path.join(PROD_DIR, t), quality=96)
        krown_smoke.save(os.path.join(MASTERS_DIR, t), quality=96)
        print(f"Deployed KrowN Smoke: {t}")

    brushed_targets = [
        'krown-shaker-brushed-v6.jpg',
        'krown-shaker-brushed-steel.jpg',
        'krown-shaker-brushed-tritan.jpg',
    ]
    for t in brushed_targets:
        krown_brushed.save(os.path.join(PROD_DIR, t), quality=96)
        krown_brushed.save(os.path.join(MASTERS_DIR, t), quality=96)
        print(f"Deployed KrowN Brushed: {t}")

    # 3-bottle lineup
    lineup_canvas = Image.new('RGB', (1600, 1000), (12, 14, 18))
    b1_small = krown_obsidian.resize((620, 620), Image.Resampling.LANCZOS)
    b2_small = krown_smoke.resize((620, 620), Image.Resampling.LANCZOS)
    b3_small = krown_brushed.resize((620, 620), Image.Resampling.LANCZOS)
    lineup_canvas.paste(b1_small, (-30, 200))
    lineup_canvas.paste(b2_small, (490, 200))
    lineup_canvas.paste(b3_small, (1010, 200))

    lineup_canvas.save(os.path.join(PROD_DIR, 'krown-shaker-bottles-3-editions.jpg'), quality=96)
    lineup_canvas.save(os.path.join(MASTERS_DIR, 'krown-shaker-bottles-3-editions.jpg'), quality=96)
    print("Deployed KrowN 3-bottle lineup!")

    # 2. KrowN Construction
    kc_highvis = build_kc_highvis()
    kc_steelcore = build_kc_steelcore()
    kc_tradesman = build_kc_tradesman()

    kc_hv_targets = [
        'kc-shaker-photoreal-v6.jpg',
        'kc-shaker-highvis-steel.jpg',
        'kc-shaker-highvis-steel-v2.jpg',
        'kc-shaker-highvis-tritan.jpg',
        'kc-shaker-highvis-tritan-v3.jpg',
        'kc-shaker-highvis-tritan-v4.jpg',
    ]
    for t in kc_hv_targets:
        kc_highvis.save(os.path.join(PROD_DIR, t), quality=96)
        kc_highvis.save(os.path.join(MASTERS_DIR, t), quality=96)
        print(f"Deployed KC High-Vis: {t}")

    kc_sc_targets = [
        'kc-shaker-steelcore-v6.jpg',
        'kc-shaker-steelcore-steel.jpg',
        'kc-shaker-steelcore-tritan.jpg',
    ]
    for t in kc_sc_targets:
        kc_steelcore.save(os.path.join(PROD_DIR, t), quality=96)
        kc_steelcore.save(os.path.join(MASTERS_DIR, t), quality=96)
        print(f"Deployed KC Steelcore: {t}")

    kc_tb_targets = [
        'kc-shaker-tradesman-v6.jpg',
        'kc-shaker-jobsite-steel.jpg',
        'kc-shaker-jobsite-tritan.jpg',
    ]
    for t in kc_tb_targets:
        kc_tradesman.save(os.path.join(PROD_DIR, t), quality=96)
        kc_tradesman.save(os.path.join(MASTERS_DIR, t), quality=96)
        print(f"Deployed KC Tradesman: {t}")

    # KC 3-bottle lineup
    kc_lineup = Image.new('RGB', (1600, 1000), (12, 14, 18))
    k1_small = kc_highvis.resize((620, 620), Image.Resampling.LANCZOS)
    k2_small = kc_tradesman.resize((620, 620), Image.Resampling.LANCZOS)
    k3_small = kc_steelcore.resize((620, 620), Image.Resampling.LANCZOS)
    kc_lineup.paste(k1_small, (-30, 200))
    kc_lineup.paste(k2_small, (490, 200))
    kc_lineup.paste(k3_small, (1010, 200))
    kc_lineup.save(os.path.join(PROD_DIR, 'kc-shaker-bottles-3-editions.jpg'), quality=96)
    kc_lineup.save(os.path.join(MASTERS_DIR, 'kc-shaker-bottles-3-editions.jpg'), quality=96)
    print("Deployed KC 3-bottle lineup!")

    print("ALL SHAKERS RENDERED, POLISHED, AND DEPLOYED!")
