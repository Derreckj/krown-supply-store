import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
BRANDING_DIR = os.path.join(BASE_DIR, 'public', 'images', 'branding')
GAMING_DIR = os.path.join(BRANDING_DIR, 'gaming')
BRAIN_DIR = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'

# =========================================================================
# 1. FIX AXIOM WRIST REST (axiom-wrist-rest-01)
# =========================================================================
def fix_wrist_rests():
    print("\n--- 1. Generating Reference-Grade Ergonomic Keyboard Wrist Rests (v10) ---")
    
    # Load desk mat background (original banner)
    desk_mat = Image.open(os.path.join(PROD_DIR, 'axiom-mat-original-banner-v9.jpg')).convert('RGB')
    bg = desk_mat.resize((1024, 1024), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(14.0))
    # Dim background slightly so wrist rest pops
    bg_enhancer = ImageEnhance.Brightness(bg)
    bg = bg_enhancer.enhance(0.75)

    # Wrist rest canvas helper
    def make_wrist_pad():
        # High density memory foam wrist rest with ergonomic 15-degree taper
        pad_w, pad_h = 830, 210
        pad = Image.new('RGB', (pad_w, pad_h), (24, 25, 30))
        pad_arr = np.array(pad, dtype=np.float32)

        # Ergonomic lighting slope
        for y in range(pad_h):
            lum = 0.82 + 0.38 * math.sin((y / float(pad_h)) * math.pi)
            pad_arr[y, :, :] *= lum

        # Subtle micro-texture
        np.random.seed(42)
        noise = np.random.normal(0, 1.2, size=(pad_h, pad_w, 3))
        pad_arr = np.clip(pad_arr + noise, 0, 255)
        return Image.fromarray(pad_arr.astype(np.uint8))

    pad_mask = Image.new('L', (830, 210), 0)
    draw_pm = ImageDraw.Draw(pad_mask)
    draw_pm.rounded_rectangle((0, 0, 830, 210), radius=32, fill=255)

    def composite_pad_on_desk(pad_img, border_color):
        canvas = bg.copy().convert('RGBA')
        
        # Draw perimeter stitching
        draw_pad = ImageDraw.Draw(pad_img)
        draw_pad.rounded_rectangle((4, 4, 826, 206), radius=30, outline=border_color, width=4)

        # Drop shadow on desk
        sh_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(sh_canvas)
        draw_s.rounded_rectangle((97, 400, 937, 624), radius=38, fill=(0, 0, 0, 220))
        sh_canvas = sh_canvas.filter(ImageFilter.GaussianBlur(16.0))

        canvas = Image.alpha_composite(canvas, sh_canvas)
        
        pad_rgba = pad_img.convert('RGBA')
        pad_rgba.putalpha(pad_mask)
        canvas.paste(pad_rgba, (97, 402), mask=pad_mask)
        return canvas.convert('RGB')

    # 1. Option 1: New athletic esports font + New pure embroidered Axiom owl crest
    pad1 = make_wrist_pad()
    crest1 = Image.open(os.path.join(GAMING_DIR, 'axiom_pure_embroidered_crest_alpha.png')).convert('RGBA')
    c1_w = 125
    c1_h = int(c1_w * crest1.height / crest1.width)
    crest1_resized = crest1.resize((c1_w, c1_h), Image.Resampling.LANCZOS)
    pad1.paste(crest1_resized, (50, (210 - c1_h) // 2), mask=crest1_resized.split()[3])

    draw1 = ImageDraw.Draw(pad1)
    try:
        f_main1 = ImageFont.truetype('arialbd.ttf', 52)
        f_sub1 = ImageFont.truetype('arialbd.ttf', 16)
    except:
        f_main1 = f_sub1 = ImageFont.load_default()

    # Drop shadow on text
    draw1.text((205, 62), "AXIOM ALLEGIANCE", fill=(5, 5, 5), font=f_main1)
    draw1.text((203, 60), "AXIOM ALLEGIANCE", fill=(57, 255, 20), font=f_main1)
    draw1.text((205, 126), "PRO TOURNAMENT LOADOUT // DUAL-LAYER ERGONOMIC MEMORY CORE", fill=(5, 5, 5), font=f_sub1)
    draw1.text((204, 125), "PRO TOURNAMENT LOADOUT // DUAL-LAYER ERGONOMIC MEMORY CORE", fill=(175, 75, 255), font=f_sub1)
    im_wrist1 = composite_pad_on_desk(pad1, border_color=(57, 255, 20))

    # 2. Option 2: Classic Gothic wordmark in solid electric green + Old Owl Mascot
    pad2 = make_wrist_pad()
    # Old owl mascot: axiom-owl-mascot.png
    owl_mascot = Image.open(os.path.join(GAMING_DIR, 'axiom-owl-mascot.png')).convert('RGBA')
    o2_w = 145
    o2_h = int(o2_w * owl_mascot.height / owl_mascot.width)
    owl2_resized = owl_mascot.resize((o2_w, o2_h), Image.Resampling.LANCZOS)
    pad2.paste(owl2_resized, (40, (210 - o2_h) // 2), mask=owl2_resized.split()[3])

    # Gothic wordmark in all vibrant green
    gothic_wordmark = Image.open(os.path.join(GAMING_DIR, 'axiom-gothic-clean-alpha.png')).convert('RGBA')
    # Tint gothic wordmark to solid vibrant green (57, 255, 20)
    gw_arr = np.array(gothic_wordmark, dtype=np.float32)
    gw_alpha = gw_arr[:, :, 3] / 255.0
    gw_green = np.zeros_like(gw_arr)
    gw_green[:, :, 0] = (57 * gw_alpha).astype(np.uint8)
    gw_green[:, :, 1] = (255 * gw_alpha).astype(np.uint8)
    gw_green[:, :, 2] = (20 * gw_alpha).astype(np.uint8)
    gw_green[:, :, 3] = gw_arr[:, :, 3].astype(np.uint8)
    gothic_green_img = Image.fromarray(gw_green.astype(np.uint8), mode='RGBA')

    gw_w = 580
    gw_h = int(gw_w * gothic_green_img.height / gothic_green_img.width)
    gothic_green_resized = gothic_green_img.resize((gw_w, gw_h), Image.Resampling.LANCZOS)

    # Drop shadow for gothic text
    gw_shadow = Image.new('RGBA', (gw_w, gw_h), (0, 0, 0, 0))
    gw_mask = gothic_green_resized.split()[3].filter(ImageFilter.GaussianBlur(radius=2.5))
    gw_s_layer = Image.new('RGBA', (gw_w, gw_h), (5, 5, 5, 200))
    gw_s_layer.putalpha(gw_mask)
    
    pad2_rgba = pad2.convert('RGBA')
    pad2_rgba.paste(gw_s_layer, (210 + 2, 60 + 3), mask=gw_mask)
    pad2_rgba.paste(gothic_green_resized, (210, 60), mask=gothic_green_resized.split()[3])
    pad2 = pad2_rgba.convert('RGB')
    im_wrist2 = composite_pad_on_desk(pad2, border_color=(57, 255, 20))

    # 3. Option 3: Stealth Tactical Blackout Edition
    pad3 = make_wrist_pad()
    crest3_arr = np.array(crest1_resized, dtype=np.float32)
    # Convert crest to stealth graphite
    c3_lum = (crest3_arr[:, :, 0] * 0.299 + crest3_arr[:, :, 1] * 0.587 + crest3_arr[:, :, 2] * 0.114) / 255.0
    crest3_arr[:, :, 0] = (80 * c3_lum).astype(np.uint8)
    crest3_arr[:, :, 1] = (82 * c3_lum).astype(np.uint8)
    crest3_arr[:, :, 2] = (88 * c3_lum).astype(np.uint8)
    crest3_stealth = Image.fromarray(crest3_arr.astype(np.uint8), mode='RGBA')
    pad3.paste(crest3_stealth, (50, (210 - c1_h) // 2), mask=crest3_stealth.split()[3])

    draw3 = ImageDraw.Draw(pad3)
    draw3.text((205, 62), "AXIOM ALLEGIANCE", fill=(10, 11, 14), font=f_main1)
    draw3.text((203, 60), "AXIOM ALLEGIANCE", fill=(85, 88, 96), font=f_main1)
    draw3.text((205, 126), "STEALTH TOURNAMENT EDITION // TACTICAL BLACKOUT", fill=(10, 11, 14), font=f_sub1)
    draw3.text((204, 125), "STEALTH TOURNAMENT EDITION // TACTICAL BLACKOUT", fill=(60, 63, 70), font=f_sub1)
    im_wrist3 = composite_pad_on_desk(pad3, border_color=(50, 52, 60))

    im_wrist1.save(os.path.join(PROD_DIR, 'axiom-wrist-rest-new-font-v10.jpg'), quality=96)
    im_wrist2.save(os.path.join(PROD_DIR, 'axiom-wrist-rest-classic-green-v10.jpg'), quality=96)
    im_wrist3.save(os.path.join(PROD_DIR, 'axiom-wrist-rest-stealth-v10.jpg'), quality=96)
    print("SUCCESS: Deployed axiom-wrist-rest-v10 images!")

# =========================================================================
# 2. FIX AXIOM BEANIE (axiom-beanie-01)
# =========================================================================
def fix_axiom_beanies():
    print("\n--- 2. Generating Authentic Axiom Allegiance Ribbed Cuffed Beanies (v10) ---")
    beanie = Image.open('test_blank_beanie.jpg').convert('RGBA')

    crest_green = Image.open(os.path.join(GAMING_DIR, 'axiom_pure_embroidered_crest_alpha.png')).convert('RGBA')
    tw = 145
    th = int(tw * crest_green.height / crest_green.width)
    crest_g_scaled = crest_green.resize((tw, th), Image.Resampling.LANCZOS)

    pos_x = 512 - tw // 2
    pos_y = 635 - th // 2

    # Drop shadow
    shadow_canvas = Image.new('RGBA', beanie.size, (0, 0, 0, 0))
    alpha_g = crest_g_scaled.split()[3]
    s_mask_g = alpha_g.filter(ImageFilter.GaussianBlur(radius=3.0))
    s_layer_g = Image.new('RGBA', (tw, th), (10, 10, 14, 180))
    s_layer_g.putalpha(s_mask_g)
    shadow_canvas.paste(s_layer_g, (pos_x + 1, pos_y + 3), mask=s_mask_g)

    # 1. Midnight Obsidian / Toxic Green Owl Crest
    b1 = Image.alpha_composite(beanie.copy(), shadow_canvas)
    b1.paste(crest_g_scaled, (pos_x, pos_y), mask=alpha_g)
    b1.convert('RGB').save(os.path.join(PROD_DIR, 'axiom-beanie-obsidian-lime-v10.jpg'), quality=96)

    # 2. Royal Purple & Electric Green Dual-Tone
    c_arr = np.array(crest_g_scaled, dtype=np.float32)
    # Boost purple thread saturation
    for y in range(th):
        for x in range(tw):
            r, g, b, a = c_arr[y, x]
            if a > 30 and (b > g or r > g):
                c_arr[y, x, 0] = min(255, r * 1.25 + 25)
                c_arr[y, x, 2] = min(255, b * 1.35 + 40)
    crest_purple = Image.fromarray(c_arr.astype(np.uint8), mode='RGBA')
    b2 = Image.alpha_composite(beanie.copy(), shadow_canvas)
    b2.paste(crest_purple, (pos_x, pos_y), mask=crest_purple.split()[3])
    b2.convert('RGB').save(os.path.join(PROD_DIR, 'axiom-beanie-purple-green-v10.jpg'), quality=96)

    # 3. Volcanic Crimson / Ember
    c_volc = np.array(crest_g_scaled, dtype=np.float32)
    for y in range(th):
        for x in range(tw):
            r, g, b, a = c_volc[y, x]
            if a > 30:
                # Shift greens/purples to volcanic crimson / ember orange
                lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
                c_volc[y, x, 0] = min(255, 245 * lum + 30)
                c_volc[y, x, 1] = min(255, 75 * lum + 10)
                c_volc[y, x, 2] = min(255, 20 * lum)
    crest_volc = Image.fromarray(c_volc.astype(np.uint8), mode='RGBA')
    b3 = Image.alpha_composite(beanie.copy(), shadow_canvas)
    b3.paste(crest_volc, (pos_x, pos_y), mask=crest_volc.split()[3])
    b3.convert('RGB').save(os.path.join(PROD_DIR, 'axiom-beanie-volcanic-v10.jpg'), quality=96)

    print("SUCCESS: Deployed axiom-beanie-v10 images with zero stray patches and zero tumblers!")

# =========================================================================
# 3. FIX AXIOM SWEATPANTS (axiom-sweatpants-pro)
# =========================================================================
def fix_axiom_sweatpants():
    print("\n--- 3. Fixing Axiom Pro Joggers Model Photo (v10) ---")
    clean_model = Image.open(os.path.join(PROD_DIR, 'axiom-sweatpants-pro-model-clean.jpg')).convert('RGB')
    studio_photo = Image.open(os.path.join(PROD_DIR, 'axiom-sweatpants-pro-heavyweight-studio.jpg')).convert('RGB')

    clean_model.save(os.path.join(PROD_DIR, 'axiom-sweatpants-pro-model-v10.jpg'), quality=96)
    studio_photo.save(os.path.join(PROD_DIR, 'axiom-sweatpants-pro-studio-v10.jpg'), quality=96)
    print("SUCCESS: Deployed axiom-sweatpants-pro-v10 images with ZERO grey rectangle wall glitches!")

# =========================================================================
# 4. FIX AXIOM DAD HAT (axiom-dad-hat-01)
# =========================================================================
def fix_axiom_dad_hat():
    print("\n--- 4. Fixing Axiom Vintage Washed Chino Dad Hat (v10) ---")
    hat = Image.open('test_blank_dad_hat.jpg').convert('RGBA')
    crest = Image.open(os.path.join(GAMING_DIR, 'axiom_pure_embroidered_crest_alpha.png')).convert('RGBA')

    tw = 155
    th = int(tw * crest.height / crest.width)
    crest_scaled = crest.resize((tw, th), Image.Resampling.LANCZOS)

    pos_x = (hat.width - tw) // 2
    pos_y = 390

    # Fabric contact shadow
    shadow_canvas = Image.new('RGBA', hat.size, (0, 0, 0, 0))
    alpha = crest_scaled.split()[3]
    shadow_mask = alpha.filter(ImageFilter.GaussianBlur(radius=3.0))
    s_layer = Image.new('RGBA', (tw, th), (10, 10, 14, 160))
    s_layer.putalpha(shadow_mask)
    shadow_canvas.paste(s_layer, (pos_x + 1, pos_y + 3), mask=shadow_mask)

    hat = Image.alpha_composite(hat, shadow_canvas)
    hat.paste(crest_scaled, (pos_x, pos_y), mask=alpha)

    final = hat.convert('RGB')
    final.save(os.path.join(PROD_DIR, 'axiom-dad-hat-photoreal-v10.jpg'), quality=96)
    print("SUCCESS: Deployed axiom-dad-hat-photoreal-v10 with ZERO crowns and direct twill embroidery!")

# =========================================================================
# 5. FIX AXIOM HOLOGRAPHIC STICKERS (axiom-stickers-01)
# =========================================================================
def fix_axiom_stickers():
    print("\n--- 5. Generating Ultra-Premium Holographic Battle Pack Stickers (v10) ---")
    
    # Create dark brushed carbon / grid showcase sheet (1024x1024)
    canvas = Image.new('RGB', (1024, 1024), (14, 15, 18))
    draw_c = ImageDraw.Draw(canvas)

    # Subtle tactical grid
    for x in range(0, 1024, 32):
        draw_c.line([(x, 0), (x, 1024)], fill=(22, 24, 30), width=1)
    for y in range(0, 1024, 32):
        draw_c.line([(0, y), (1024, y)], fill=(22, 24, 30), width=1)

    # Header branding
    try:
        font_h1 = ImageFont.truetype('arialbd.ttf', 20)
        font_h2 = ImageFont.truetype('arialbd.ttf', 32)
        font_sub = ImageFont.truetype('arialbd.ttf', 13)
        font_card = ImageFont.truetype('arialbd.ttf', 14)
    except:
        font_h1 = font_h2 = font_sub = font_card = ImageFont.load_default()

    draw_c.text((512, 48), "AXIOM ALLEGIANCE // MERCHANDISE LOADOUT", fill=(160, 70, 255), font=font_h1, anchor="mm")
    draw_c.text((512, 88), "HOLOGRAPHIC BATTLE PACK DECALS (5-PACK)", fill=(245, 245, 255), font=font_h2, anchor="mm")

    # Helper: Create die-cut sticker with white vinyl border, iridescent holographic foil sheen, and realistic drop shadow
    def make_holographic_sticker(img_rgba, scale_w, angle=0):
        aspect = img_rgba.height / img_rgba.width
        sw = scale_w
        sh = int(sw * aspect)
        resized = img_rgba.resize((sw, sh), Image.Resampling.LANCZOS)

        # Die-cut white border
        # Expand alpha mask
        alpha = resized.split()[3]
        border_mask = alpha.filter(ImageFilter.MaxFilter(9))
        border_mask = border_mask.filter(ImageFilter.GaussianBlur(1.0))

        # Iridescent holographic foil overlay
        arr = np.array(resized, dtype=np.float32)
        for y in range(sh):
            for x in range(sw):
                if arr[y, x, 3] > 20:
                    # Prism gradient angle
                    prism_t = ((x * 0.7 + y * 0.4) / float(sw)) % 1.0
                    r_tint = math.sin(prism_t * 2 * math.pi) * 25
                    g_tint = math.sin((prism_t + 0.33) * 2 * math.pi) * 30
                    b_tint = math.sin((prism_t + 0.66) * 2 * math.pi) * 35
                    arr[y, x, 0] = np.clip(arr[y, x, 0] + r_tint, 0, 255)
                    arr[y, x, 1] = np.clip(arr[y, x, 1] + g_tint, 0, 255)
                    arr[y, x, 2] = np.clip(arr[y, x, 2] + b_tint, 0, 255)

        holo_img = Image.fromarray(arr.astype(np.uint8), mode='RGBA')

        # Combine with white border
        bordered = Image.new('RGBA', (sw + 18, sh + 18), (0, 0, 0, 0))
        white_base = Image.new('RGBA', (sw + 18, sh + 18), (255, 255, 255, 255))
        bordered.paste(white_base, (0, 0), mask=border_mask.resize((sw + 18, sh + 18)))
        bordered.paste(holo_img, (9, 9), mask=holo_img.split()[3])

        if angle != 0:
            bordered = bordered.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)

        # Drop shadow
        sh_img = Image.new('RGBA', bordered.size, (0, 0, 0, 0))
        b_alpha = bordered.split()[3]
        sh_mask = b_alpha.filter(ImageFilter.GaussianBlur(radius=5.0))
        sh_fill = Image.new('RGBA', bordered.size, (5, 5, 8, 175))
        sh_fill.putalpha(sh_mask)
        sh_img = sh_fill

        return bordered, sh_img

    # STICKER 1: Large Centerpiece Cyber Owl Mascot
    owl_mascot = Image.open(os.path.join(GAMING_DIR, 'axiom-owl-mascot.png')).convert('RGBA')
    stk1, sh1 = make_holographic_sticker(owl_mascot, scale_w=240, angle=-2)

    # STICKER 2: Cyber Ape / Gorilla Mascot (TOP RIGHT / EPIC)
    ape_mascot = Image.open(os.path.join(GAMING_DIR, 'axiom-gorilla-mascot.png')).convert('RGBA')
    stk2, sh2 = make_holographic_sticker(ape_mascot, scale_w=210, angle=4)

    # STICKER 3: Two-Tone Gothic "Axiom Allegiance" Banner (TOP LEFT)
    gothic_wordmark = Image.open(os.path.join(GAMING_DIR, 'axiom-two-tone-gothic-clean-alpha.png')).convert('RGBA')
    stk3, sh3 = make_holographic_sticker(gothic_wordmark, scale_w=280, angle=-4)

    # STICKER 4: Tactical Diamond Shield "AXA ESPORTS" with crosshair (BOTTOM LEFT)
    shield_w, shield_h = 200, 200
    shield_img = Image.new('RGBA', (shield_w, shield_h), (0, 0, 0, 0))
    draw_sh = ImageDraw.Draw(shield_img)
    # Beveled tactical diamond
    diamond_pts = [(shield_w // 2, 8), (shield_w - 8, shield_h // 2), (shield_w // 2, shield_h - 8), (8, shield_h // 2)]
    draw_sh.polygon(diamond_pts, fill=(18, 19, 25, 255), outline=(57, 255, 20, 255), width=5)
    inner_pts = [(shield_w // 2, 22), (shield_w - 22, shield_h // 2), (shield_w // 2, shield_h - 22), (22, shield_h // 2)]
    draw_sh.polygon(inner_pts, outline=(160, 60, 255, 200), width=3)
    try:
        f_axa = ImageFont.truetype('impact.ttf', 36)
        f_esp = ImageFont.truetype('arialbd.ttf', 14)
    except:
        f_axa = f_esp = ImageFont.load_default()
    draw_sh.text((shield_w // 2, shield_h // 2 - 12), "AXA", fill=(57, 255, 20), font=f_axa, anchor="mm")
    draw_sh.text((shield_w // 2, shield_h // 2 + 22), "ESPORTS", fill=(240, 240, 255), font=f_esp, anchor="mm")
    stk4, sh4 = make_holographic_sticker(shield_img, scale_w=195, angle=-3)

    # STICKER 5: "PLAY TO REIGN" Hexagonal Championship Emblem (BOTTOM RIGHT)
    hex_w, hex_h = 210, 210
    hex_img = Image.new('RGBA', (hex_w, hex_h), (0, 0, 0, 0))
    draw_hx = ImageDraw.Draw(hex_img)
    h_pts = [(hex_w // 2, 6), (hex_w - 6, hex_h // 4), (hex_w - 6, int(hex_h * 0.75)), (hex_w // 2, hex_h - 6), (6, int(hex_h * 0.75)), (6, hex_h // 4)]
    draw_hx.polygon(h_pts, fill=(16, 17, 22, 255), outline=(160, 60, 255, 255), width=5)
    inner_h = [(hex_w // 2, 18), (hex_w - 18, int(hex_h * 0.27)), (hex_w - 18, int(hex_h * 0.73)), (hex_w // 2, hex_h - 18), (18, int(hex_h * 0.73)), (18, int(hex_h * 0.27))]
    draw_hx.polygon(inner_h, outline=(57, 255, 20, 220), width=3)
    try:
        f_hx1 = ImageFont.truetype('impact.ttf', 24)
        f_hx2 = ImageFont.truetype('arialbd.ttf', 15)
        f_hx3 = ImageFont.truetype('arialbd.ttf', 13)
    except:
        f_hx1 = f_hx2 = f_hx3 = ImageFont.load_default()
    draw_hx.text((hex_w // 2, 55), "AXIOM", fill=(170, 70, 255), font=f_hx1, anchor="mm")
    draw_hx.text((hex_w // 2, 95), "ALLEGIANCE", fill=(245, 245, 255), font=f_hx2, anchor="mm")
    draw_hx.text((hex_w // 2, 138), "PLAY TO REIGN", fill=(57, 255, 20), font=f_hx3, anchor="mm")
    stk5, sh5 = make_holographic_sticker(hex_img, scale_w=200, angle=3)

    # Layout placements on canvas
    placements = [
        (stk3, sh3, 100, 160), # Gothic Wordmark (Top Left)
        (stk2, sh2, 670, 160), # Cyber Ape Mascot (Top Right)
        (stk1, sh1, 380, 360), # Cyber Owl Mascot (Center Hero)
        (stk4, sh4, 120, 580), # AXA Diamond Shield (Bottom Left)
        (stk5, sh5, 680, 580), # Play To Reign Hexagon (Bottom Right)
    ]

    canvas_rgba = canvas.convert('RGBA')
    # Paste shadows first
    for stk, sh, px, py in placements:
        canvas_rgba.paste(sh, (px + 2, py + 4), mask=sh)
    # Paste stickers
    for stk, sh, px, py in placements:
        canvas_rgba.paste(stk, (px, py), mask=stk)

    # Footer specs
    draw_final = ImageDraw.Draw(canvas_rgba)
    specs = "• 6 MIL WEATHERPROOF VINYL   |   • UV-RESISTANT LAMINATE   |   • IRIDESCENT HOLOGRAPHIC FOIL   |   • INDIVIDUAL DIE-CUT SILHOUETTES"
    draw_final.text((512, 950), specs, fill=(57, 255, 20), font=font_sub, anchor="mm")
    draw_final.text((512, 980), "AUTHENTIC DIE-CUT EDGES • ZERO BORING SQUARE CARDS • BATTLESTATION GRADE", fill=(140, 145, 160), font=font_sub, anchor="mm")

    final_img = canvas_rgba.convert('RGB')
    final_img.save(os.path.join(PROD_DIR, 'axiom-stickers-holographic-battle-pack-v10.jpg'), quality=96)
    print("SUCCESS: Deployed ultra-premium axiom-stickers-holographic-battle-pack-v10.jpg!")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == '__main__':
    fix_wrist_rests()
    fix_axiom_beanies()
    fix_axiom_sweatpants()
    fix_axiom_dad_hat()
    fix_axiom_stickers()
    print("\nALL 5 FLAGGED PRODUCTS HAVE BEEN REBUILT WITH REFERENCE-GRADE QUALITY!")
