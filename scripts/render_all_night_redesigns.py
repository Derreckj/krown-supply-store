import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
GAMING_DIR = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")
BRAIN_DIR = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7"
TEMP_MEDIA = os.path.join(BRAIN_DIR, ".tempmediaStorage")

os.makedirs(PUB_PRODUCTS, exist_ok=True)

# -------------------------------------------------------------
# FONT LOADER
# -------------------------------------------------------------
def get_font(name_list, size):
    for n in name_list:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()

font_headline = get_font(["impact.ttf", "arialbd.ttf"], 36)
font_title = get_font(["arialbd.ttf", "arial.ttf"], 28)
font_sub = get_font(["arialbd.ttf", "arial.ttf"], 20)
font_label = get_font(["arialbd.ttf", "arial.ttf"], 16)
font_micro = get_font(["arial.ttf"], 13)

# -------------------------------------------------------------
# LOAD ASSETS
# -------------------------------------------------------------
owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-green-eyes-clean.png")
if not os.path.exists(owl_smokey_path):
    owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-clean-alpha.png")
owl_smokey = Image.open(owl_smokey_path).convert("RGBA")

gothic_two_tone_path = os.path.join(GAMING_DIR, "axiom-two-tone-gothic-clean-alpha.png")
gothic_two_tone = Image.open(gothic_two_tone_path).convert("RGBA")

owl_mascot_path = os.path.join(GAMING_DIR, "axiom-owl-mascot.png")
owl_mascot = Image.open(owl_mascot_path).convert("RGBA") if os.path.exists(owl_mascot_path) else owl_smokey

crest_raw_path = os.path.join(GAMING_DIR, "axiom-owl-smokey-crest.jpg")
crest_raw = Image.open(crest_raw_path).convert("RGBA") if os.path.exists(crest_raw_path) else None

def create_studio_bg(w=1024, h=1024, bg_color=(12, 13, 16), glow_color=(55, 18, 75)):
    canvas = Image.new("RGBA", (w, h), (bg_color[0], bg_color[1], bg_color[2], 255))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    cx, cy = w // 2, h // 2
    for r in range(int(w * 0.48), 0, -12):
        alpha = int(32 * (1.0 - r / (w * 0.48)))
        gdraw.ellipse([cx - r, cy - int(r * 0.8), cx + r, cy + int(r * 0.8)], fill=(glow_color[0], glow_color[1], glow_color[2], alpha))
    return Image.alpha_composite(canvas, glow)

# =============================================================
# 1. WRIST PADS REWORK (3 SIZES COMPARISON & BATTLESTATION SETUP)
# =============================================================
def render_wrist_pad_tournament_edition():
    print("Rendering Wrist Pad: Tournament Edition Showcase (3 Sizes)...")
    canvas = create_studio_bg(1024, 1024, bg_color=(10, 11, 14), glow_color=(45, 15, 65))
    draw = ImageDraw.Draw(canvas)
    cx = 512

    # Header
    draw.text((cx, 45), "AXIOM ALLEGIANCE // TOURNAMENT LOADOUT", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw.text((cx, 80), "PRO COOLING GEL KEYBOARD WRIST REST", fill=(245, 245, 255), font=font_headline, anchor="mm")
    draw.text((cx, 115), "DUAL-LAYER INFUSED MEMORY FOAM • SILKY ANTI-FRICTION LYCRA • NON-SLIP SILICONE", fill=(57, 255, 20), font=font_micro, anchor="mm")

    # 3 Sizes Stack:
    # Full-Size: $23.99 (+$4)
    # TKL: $21.99 (+$2)
    # Compact: $19.99 (Base)
    sizes = [
        ("FULL-SIZE 100% (17.5\" x 3.0\") — $23.99 [+$4]", 820, 110, 200, "104 / 108 Keyboards"),
        ("TENKEYLESS TKL 80% (14.2\" x 3.0\") — $21.99 [+$2]", 680, 105, 410, "87-Key Tourney Spec"),
        ("COMPACT 60% (11.4\" x 3.0\") — $19.99 [BASE]", 540, 100, 610, "60% / 65% / 75% Boards"),
    ]

    for label, pad_w, pad_h, pad_y, sub_desc in sizes:
        px1 = cx - pad_w // 2
        px2 = cx + pad_w // 2
        py1 = pad_y
        py2 = pad_y + pad_h

        # Label above pad
        draw.text((px1 + 10, py1 - 18), label, fill=(57, 255, 20), font=font_label, anchor="ls")
        draw.text((px2 - 10, py1 - 18), sub_desc, fill=(160, 160, 180), font=font_micro, anchor="rs")

        # Soft 3D drop shadow
        shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.rounded_rectangle([px1 - 6, py1 + 8, px2 + 6, py2 + 18], radius=16, fill=(0, 0, 0, 175))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        canvas = Image.alpha_composite(canvas, shadow)
        draw = ImageDraw.Draw(canvas)

        # Base pad body (Beveled Obsidian Textured Lycra)
        pad_layer = Image.new("RGBA", (pad_w, pad_h), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(pad_layer)
        # Deep obsidian matte base
        p_draw.rounded_rectangle([0, 0, pad_w, pad_h], radius=14, fill=(18, 19, 23))

        # Carbon micro-weave subtle horizontal lines
        for y in range(4, pad_h - 4, 3):
            p_draw.line([(6, y), (pad_w - 6, y)], fill=(24, 25, 30, 80), width=1)

        # Ambient smoky fade on the right side
        for x in range(pad_w // 2, pad_w):
            alpha = int(40 * ((x - pad_w // 2) / (pad_w // 2)))
            p_draw.line([(x, 4), (x, pad_h - 4)], fill=(45, 15, 65, alpha), width=1)

        # Outer anti-fray dual-stitched border: Electric lime and royal purple
        p_draw.rounded_rectangle([0, 0, pad_w, pad_h], radius=14, outline=(138, 43, 226), width=2)
        p_draw.rounded_rectangle([3, 3, pad_w - 3, pad_h - 3], radius=11, outline=(57, 255, 20, 120), width=1)

        # Left Graphic: Two-Tone Gothic "Axiom Allegiance"
        g_target_h = int(pad_h * 0.44)
        g_scale = g_target_h / gothic_two_tone.height
        g_target_w = int(gothic_two_tone.width * g_scale)
        g_resized = gothic_two_tone.resize((g_target_w, g_target_h), Image.Resampling.LANCZOS)
        pad_layer.paste(g_resized, (28, (pad_h - g_target_h) // 2), g_resized)

        # Right Graphic: Smoky Owl with Glowing Green Eyes
        o_target_h = int(pad_h * 0.78)
        o_scale = o_target_h / owl_smokey.height
        o_target_w = int(owl_smokey.width * o_scale)
        o_resized = owl_smokey.resize((o_target_w, o_target_h), Image.Resampling.LANCZOS)
        pad_layer.paste(o_resized, (pad_w - o_target_w - 24, (pad_h - o_target_h) // 2), o_resized)

        canvas.paste(pad_layer, (px1, py1), pad_layer)
        draw = ImageDraw.Draw(canvas)

    # Bottom feature badges
    f_y = 800
    features = [
        ("COOLING MEMORY GEL", "Slow-rebound 45D core with heat-dissipating gel"),
        ("SILKY GLIDE LYCRA", "Zero-friction micro-weave tournament surface"),
        ("ANTI-SLIP SILICONE", "Non-skid textured rubber base locks to desk"),
        ("ERGONOMIC 15° SLOPE", "Neutral wrist tilt eliminates CTS fatigue"),
    ]
    col_w = 230
    start_x = cx - (col_w * 4) // 2 + 10
    for i, (title, desc) in enumerate(features):
        fx = start_x + i * col_w
        draw.rounded_rectangle([fx, f_y, fx + col_w - 15, f_y + 140], radius=10, fill=(16, 17, 22), outline=(40, 42, 52), width=1)
        draw.text((fx + (col_w - 15)//2, f_y + 25), title, fill=(57, 255, 20), font=font_label, anchor="mm")
        # Multi-line desc
        words = desc.split(" ")
        line1 = " ".join(words[:3])
        line2 = " ".join(words[3:])
        draw.text((fx + (col_w - 15)//2, f_y + 65), line1, fill=(180, 180, 200), font=font_micro, anchor="mm")
        draw.text((fx + (col_w - 15)//2, f_y + 88), line2, fill=(180, 180, 200), font=font_micro, anchor="mm")

    # Bottom Footer
    draw.text((cx, 985), "AUTHORIZED AXIOM ALLEGIANCE TOURNAMENT GEAR • 100% QUALITY GUARANTEED", fill=(110, 115, 130), font=font_micro, anchor="mm")

    out_p = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-tournament-edition.jpg")
    canvas.convert("RGB").save(out_p, "JPEG", quality=93, progressive=True)
    print(f"Saved: {out_p}")

def render_wrist_pad_stealth_setup():
    print("Rendering Wrist Pad: Mechanical Keyboard Battlestation In-Use Setup...")
    canvas = create_studio_bg(1024, 1024, bg_color=(9, 10, 13), glow_color=(50, 12, 70))
    draw = ImageDraw.Draw(canvas)
    cx = 512

    draw.text((cx, 45), "AXIOM ALLEGIANCE // IN-SITU BATTLESTATION SETUP", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw.text((cx, 80), "ERGONOMIC TACTICAL KEYBOARD WRIST REST", fill=(245, 245, 255), font=font_headline, anchor="mm")

    # Keyboard Silhouette
    kb_w, kb_h = 760, 260
    kb_y = 170
    draw.rounded_rectangle([cx - kb_w//2, kb_y, cx + kb_w//2, kb_y + kb_h], radius=12, fill=(20, 21, 26), outline=(45, 48, 58), width=2)
    # RGB Underglow
    draw.line([(cx - kb_w//2 + 25, kb_y + kb_h - 2), (cx + kb_w//2 - 25, kb_y + kb_h - 2)], fill=(57, 255, 20), width=4)

    # Keycaps grid
    for r in range(5):
        ky = kb_y + 25 + r * 44
        for c in range(16):
            kx = cx - kb_w//2 + 35 + c * 43
            draw.rounded_rectangle([kx, ky, kx + 36, ky + 36], radius=4, fill=(28, 29, 36), outline=(42, 44, 54), width=1)
            if r == 2 and c in [3, 4, 5]: # WASD accent
                draw.rounded_rectangle([kx, ky, kx + 36, ky + 36], radius=4, fill=(35, 18, 50), outline=(138, 43, 226), width=1)
            elif r == 1 and c == 4: # W key
                draw.rounded_rectangle([kx, ky, kx + 36, ky + 36], radius=4, fill=(35, 18, 50), outline=(138, 43, 226), width=1)

    draw.text((cx, kb_y + kb_h // 2 + 10), "MECHANICAL GAMING KEYBOARD", fill=(120, 125, 140), font=font_sub, anchor="mm")

    # Wrist Rest Positioned Directly in front of the keyboard
    wr_w, wr_h = 760, 140
    wr_y = kb_y + kb_h + 35

    # Shadow
    w_shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    ws_draw = ImageDraw.Draw(w_shadow)
    ws_draw.rounded_rectangle([cx - wr_w//2 - 8, wr_y + 12, cx + wr_w//2 + 8, wr_y + wr_h + 24], radius=16, fill=(0, 0, 0, 190))
    w_shadow = w_shadow.filter(ImageFilter.GaussianBlur(14))
    canvas = Image.alpha_composite(canvas, w_shadow)
    draw = ImageDraw.Draw(canvas)

    # Pad body
    pad_box = Image.new("RGBA", (wr_w, wr_h), (0, 0, 0, 0))
    pb_draw = ImageDraw.Draw(pad_box)
    pb_draw.rounded_rectangle([0, 0, wr_w, wr_h], radius=14, fill=(18, 19, 24))

    # Dual perimeter stitching
    pb_draw.rounded_rectangle([0, 0, wr_w, wr_h], radius=14, outline=(138, 43, 226), width=2)
    pb_draw.rounded_rectangle([3, 3, wr_w - 3, wr_h - 3], radius=11, outline=(57, 255, 20, 130), width=1)

    # Left: Gothic two-tone "Axiom Allegiance"
    g_h = int(wr_h * 0.46)
    g_w = int(gothic_two_tone.width * (g_h / gothic_two_tone.height))
    g_res = gothic_two_tone.resize((g_w, g_h), Image.Resampling.LANCZOS)
    pad_box.paste(g_res, (35, (wr_h - g_h) // 2), g_res)

    # Right: Smoky owl with glowing green eyes
    o_h = int(wr_h * 0.82)
    o_w = int(owl_smokey.width * (o_h / owl_smokey.height))
    o_res = owl_smokey.resize((o_w, o_h), Image.Resampling.LANCZOS)
    pad_box.paste(o_res, (wr_w - o_w - 35, (wr_h - o_h) // 2), o_res)

    canvas.paste(pad_box, (cx - wr_w//2, wr_y), pad_box)
    draw = ImageDraw.Draw(canvas)

    # Ergonomic Callouts
    c_y = 670
    callouts = [
        ("PRECISION FITMENT", "Engineered to sit flush against standard mechanical & optical gaming keyboards."),
        ("CONTOURED SUPPORT", "Alleviates wrist strain during marathon streams and ranked clutch gameplay."),
        ("TRIPLE SIZING OPTIONS", "Available in 60% Compact ($19.99), TKL 80% ($21.99), and 100% Full ($23.99)."),
    ]
    for i, (head, text) in enumerate(callouts):
        cy_i = c_y + i * 85
        draw.rounded_rectangle([cx - 380, cy_i, cx + 380, cy_i + 70], radius=8, fill=(16, 17, 22), outline=(40, 42, 52), width=1)
        draw.text((cx - 360, cy_i + 22), f"0{i+1}. {head}", fill=(57, 255, 20), font=font_label, anchor="ls")
        draw.text((cx - 360, cy_i + 48), text, fill=(180, 180, 195), font=font_micro, anchor="ls")

    draw.text((cx, 975), "PROVEN TOURNAMENT DURABILITY • DESIGNED FOR CHAMPIONS", fill=(120, 125, 140), font=font_micro, anchor="mm")

    out_p = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-stealth-setup.jpg")
    canvas.convert("RGB").save(out_p, "JPEG", quality=93, progressive=True)
    print(f"Saved: {out_p}")

# =============================================================
# 2. HEAVYWEIGHT 450 GSM JOGGERS REWORK
# =============================================================
def render_joggers_model_lookbook():
    print("Rendering Joggers: Model Lookbook with Colored Inside Lettering & New Owl Thigh Crest...")
    # Base model image:
    base_model_path = os.path.join(BRAIN_DIR, "axiom_pro_joggers_clean_1791592187560.jpg")
    if not os.path.exists(base_model_path):
        base_model_path = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-clean.jpg")
    
    img = Image.open(base_model_path).convert("RGBA")
    w, h = img.size

    # In the model photo, the model's left leg (running vertically down) has the lettering
    # And the right panel/thigh has the owl crest.
    # Let's inspect the overlay positions:
    # Model's leg with lettering is angled roughly from (w*0.16, h*0.36) down to (w*0.22, h*0.56)
    # The right panel zoom is on the right side of the image (x ~ w*0.7 to w*0.9, y ~ h*0.3 to h*0.45)
    
    # 1. Overlay Two-Tone Gothic lettering down the pant leg:
    # Rotate gothic lettering vertically for the leg
    leg_text = gothic_two_tone.rotate(-70, expand=True, resample=Image.Resampling.BICUBIC)
    leg_w = int(w * 0.11)
    leg_h = int(leg_text.height * (leg_w / leg_text.width))
    leg_text_resized = leg_text.resize((leg_w, leg_h), Image.Resampling.LANCZOS)

    # Position on model's leg (replacing the old white lettering with vibrant colored interior gothic font)
    # Target coord: x ~ 160-230, y ~ 360-560 on a 1024x1024 canvas
    lx = int(w * 0.155)
    ly = int(h * 0.365)
    
    # Soft mask/dark patch under the new lettering to cleanly occlude old lettering
    dark_patch = Image.new("RGBA", (leg_w + 30, leg_h + 30), (0, 0, 0, 0))
    dp_draw = ImageDraw.Draw(dark_patch)
    dp_draw.ellipse([0, 0, leg_w + 30, leg_h + 30], fill=(22, 22, 24, 230))
    dark_patch = dark_patch.filter(ImageFilter.GaussianBlur(10))
    img.paste(dark_patch, (lx - 15, ly - 15), dark_patch)
    img.paste(leg_text_resized, (lx, ly), leg_text_resized)

    # 2. Right Inset Zoom Panel: Update the thigh patch to the new smoky owl crest
    # The zoom panel is at x ~ 700 to 950, y ~ 280 to 450
    inset_owl = owl_smokey.resize((int(w * 0.18), int(w * 0.18 * (owl_smokey.height / owl_smokey.width))), Image.Resampling.LANCZOS)
    rx = int(w * 0.72)
    ry = int(h * 0.31)
    
    # Clean dark underlay for zoom panel
    dark_zoom = Image.new("RGBA", (inset_owl.width + 40, inset_owl.height + 40), (0, 0, 0, 0))
    dz_draw = ImageDraw.Draw(dark_zoom)
    dz_draw.ellipse([0, 0, inset_owl.width + 40, inset_owl.height + 40], fill=(18, 18, 20, 245))
    dark_zoom = dark_zoom.filter(ImageFilter.GaussianBlur(8))
    img.paste(dark_zoom, (rx - 20, ry - 20), dark_zoom)
    img.paste(inset_owl, (rx, ry), inset_owl)

    # 3. Model's actual hip on the body (around x ~ 280-320, y ~ 340-370)
    hip_owl = owl_smokey.resize((int(w * 0.055), int(w * 0.055 * (owl_smokey.height / owl_smokey.width))), Image.Resampling.LANCZOS)
    img.paste(hip_owl, (int(w * 0.285), int(h * 0.345)), hip_owl)

    out_p = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-clean.jpg")
    img.convert("RGB").save(out_p, "JPEG", quality=94, progressive=True)
    print(f"Saved: {out_p}")

def render_joggers_studio_heavyweight():
    print("Rendering Joggers: Studio Heavyweight Flat Lay...")
    canvas = create_studio_bg(1024, 1024, bg_color=(12, 13, 16), glow_color=(45, 15, 60))
    cx = 512

    # Draw Sweatpants Silhouette
    draw = ImageDraw.Draw(canvas)
    waist_left, waist_right = cx - 180, cx + 180
    waist_top, waist_bot = 140, 190
    left_hip = (waist_left - 30, 290)
    left_knee = (waist_left - 15, 590)
    left_ankle_out = (cx - 155, 870)
    left_ankle_in = (cx - 75, 870)
    left_crotch = (cx, 440)
    right_hip = (waist_right + 30, 290)
    right_knee = (waist_right + 15, 590)
    right_ankle_out = (cx + 155, 870)
    right_ankle_in = (cx + 75, 870)

    pant_poly = [
        (waist_left, waist_top),
        (waist_right, waist_top),
        right_hip, right_knee, right_ankle_out, right_ankle_in,
        (cx + 60, 600), left_crotch, (cx - 60, 600),
        left_ankle_in, left_ankle_out, left_knee, left_hip,
    ]

    # Floor shadow
    shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.polygon(pant_poly, fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)
    draw = ImageDraw.Draw(canvas)

    # Fill Matte Obsidian French Terry
    draw.polygon(pant_poly, fill=(20, 20, 22))

    # Waistband ribbed collar
    draw.rounded_rectangle([waist_left - 5, waist_top, waist_right + 5, waist_bot], radius=8, fill=(26, 26, 30), outline=(38, 38, 44), width=2)
    # Dual-tone braided drawstrings (purple & green) hanging down
    draw.line([(cx - 20, waist_bot), (cx - 25, waist_bot + 120)], fill=(138, 43, 226), width=4)
    draw.line([(cx + 20, waist_bot), (cx + 25, waist_bot + 120)], fill=(57, 255, 20), width=4)
    # Metallic aglets
    draw.rectangle([cx - 27, waist_bot + 115, cx - 23, waist_bot + 130], fill=(180, 180, 190))
    draw.rectangle([cx + 23, waist_bot + 115, cx + 27, waist_bot + 130], fill=(180, 180, 190))

    # Ankle Ribbed Cuffs
    draw.rounded_rectangle([cx - 158, 860, cx - 72, 895], radius=6, fill=(26, 26, 30), outline=(38, 38, 44), width=2)
    draw.rounded_rectangle([cx + 72, 860, cx + 158, 895], radius=6, fill=(26, 26, 30), outline=(38, 38, 44), width=2)

    # Inseam stitch & pocket outlines
    draw.line([left_crotch, (cx, 300)], fill=(12, 12, 14), width=3)
    draw.line([(waist_left + 15, waist_bot + 10), (waist_left - 15, 330)], fill=(32, 32, 38), width=2) # left pocket
    draw.line([(waist_right - 15, waist_bot + 10), (waist_right + 15, 330)], fill=(32, 32, 38), width=2) # right pocket

    # Left Leg: Two-Tone Gothic "Axiom Allegiance" with colored inside
    # Running vertically down the outer left leg
    leg_gothic = gothic_two_tone.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
    lg_w = 95
    lg_h = int(leg_gothic.height * (lg_w / leg_gothic.width))
    leg_gothic_res = leg_gothic.resize((lg_w, lg_h), Image.Resampling.LANCZOS)
    canvas.paste(leg_gothic_res, (cx - 200, 360), leg_gothic_res)

    # Right Thigh: Smoky Owl Mascot with Glowing Green Eyes
    thigh_owl = owl_smokey.resize((140, int(140 * (owl_smokey.height / owl_smokey.width))), Image.Resampling.LANCZOS)
    canvas.paste(thigh_owl, (cx + 75, 270), thigh_owl)

    # Callouts
    draw = ImageDraw.Draw(canvas)
    draw.text((cx, 60), "AXIOM ALLEGIANCE // HEAVYWEIGHT 450 GSM JOGGERS", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw.text((cx, 95), "TOURNAMENT PRO FLEECE SWEATPANTS", fill=(245, 245, 255), font=font_headline, anchor="mm")

    draw.text((cx - 300, 520), "GOTHIC TWO-TONE\nCOLOR INTERIOR PRINT", fill=(57, 255, 20), font=font_micro, anchor="mm")
    draw.line([(cx - 210, 520), (cx - 155, 520)], fill=(57, 255, 20), width=1)

    draw.text((cx + 310, 330), "SMOKY AXIOM OWL\nTHIGH CREST", fill=(138, 43, 226), font=font_micro, anchor="mm")
    draw.line([(cx + 215, 330), (cx + 250, 330)], fill=(138, 43, 226), width=1)

    draw.text((cx, 965), "450 GSM FRENCH TERRY • DUAL-TONE BRAIDED CORDS • ZIPPERED STASH POCKETS", fill=(130, 135, 150), font=font_micro, anchor="mm")

    out_p = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-heavyweight-studio.jpg")
    canvas.convert("RGB").save(out_p, "JPEG", quality=94, progressive=True)
    print(f"Saved: {out_p}")

# =============================================================
# 3. HEAVYWEIGHT 450 GSM STREETWEAR HOODIE REWORK
# =============================================================
def render_hoodie_studio_and_model():
    print("Rendering Hoodie: Studio & Model Rework with Sleeve Graphic...")
    # Base studio hoodie
    base_studio = os.path.join(BRAIN_DIR, "axiom_hoodie_studio_front_1791592242763.jpg")
    if not os.path.exists(base_studio):
        base_studio = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-studio.jpg")

    img_s = Image.open(base_studio).convert("RGBA")
    w, h = img_s.size

    # Chest: New smoky owl crest
    chest_owl = owl_smokey.resize((int(w * 0.28), int(w * 0.28 * (owl_smokey.height / owl_smokey.width))), Image.Resampling.LANCZOS)
    cx = w // 2
    cy = int(h * 0.42)
    # Soft dark underlay on chest
    dark_c = Image.new("RGBA", (chest_owl.width + 40, chest_owl.height + 40), (0, 0, 0, 0))
    dc_draw = ImageDraw.Draw(dark_c)
    dc_draw.ellipse([0, 0, chest_owl.width + 40, chest_owl.height + 40], fill=(18, 18, 22, 230))
    dark_c = dark_c.filter(ImageFilter.GaussianBlur(10))
    img_s.paste(dark_c, (cx - chest_owl.width//2 - 20, cy - chest_owl.height//2 - 20), dark_c)
    img_s.paste(chest_owl, (cx - chest_owl.width // 2, cy - chest_owl.height // 2), chest_owl)

    # Sleeve Print: Gothic Two-Tone "AXIOM ALLEGIANCE" down the left sleeve forearm (around x ~ w*0.14 to w*0.22, y ~ h*0.48 to h*0.75)
    sleeve_text = gothic_two_tone.rotate(-65, expand=True, resample=Image.Resampling.BICUBIC)
    sl_w = int(w * 0.12)
    sl_h = int(sleeve_text.height * (sl_w / sleeve_text.width))
    sleeve_text_res = sleeve_text.resize((sl_w, sl_h), Image.Resampling.LANCZOS)
    img_s.paste(sleeve_text_res, (int(w * 0.13), int(h * 0.46)), sleeve_text_res)

    out_s = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-studio.jpg")
    img_s.convert("RGB").save(out_s, "JPEG", quality=94, progressive=True)
    print(f"Saved: {out_s}")

    # Model Lookbook Hoodie
    base_model = os.path.join(BRAIN_DIR, "axiom_hoodie_model_1791592259283.jpg")
    if os.path.exists(base_model):
        img_m = Image.open(base_model).convert("RGBA")
        mw, mh = img_m.size
        # Model chest
        m_chest_owl = owl_smokey.resize((int(mw * 0.22), int(mw * 0.22 * (owl_smokey.height / owl_smokey.width))), Image.Resampling.LANCZOS)
        img_m.paste(m_chest_owl, (int(mw * 0.38), int(mh * 0.38)), m_chest_owl)
        # Model sleeve
        m_sleeve = gothic_two_tone.rotate(-55, expand=True, resample=Image.Resampling.BICUBIC)
        ms_w = int(mw * 0.09)
        ms_h = int(m_sleeve.height * (ms_w / m_sleeve.width))
        m_sleeve_res = m_sleeve.resize((ms_w, ms_h), Image.Resampling.LANCZOS)
        img_m.paste(m_sleeve_res, (int(mw * 0.22), int(mh * 0.44)), m_sleeve_res)

        out_m = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-model.jpg")
        img_m.convert("RGB").save(out_m, "JPEG", quality=94, progressive=True)
        print(f"Saved: {out_m}")

# =============================================================
# 4. OFFICIAL CREWNECK SWEATSHIRT REWORK ($49.99, SLEEVE OPTION)
# =============================================================
def render_crewneck_studio_and_model():
    print("Rendering Crewneck: Studio & Model Rework (Removed top text, added sleeve lettering)...")
    base_crew = os.path.join(BRAIN_DIR, "axiom_sweatshirt_studio_1791592277016.jpg")
    if not os.path.exists(base_crew):
        base_crew = os.path.join(PUB_PRODUCTS, "axiom-crewneck-sweatshirt-studio.jpg")

    img_c = Image.open(base_crew).convert("RGBA")
    w, h = img_c.size

    # In previous crewneck, there was awkward curved text "AXIOM ALLEGIANCE" above the owl head
    # We clean out the chest area with dark sweatshirt fabric shading, and place the clean owl mascot without top text!
    chest_cx = w // 2
    chest_cy = int(h * 0.42)

    # Occlude awkward old top text with smooth dark fleece patch
    patch = Image.new("RGBA", (int(w * 0.38), int(h * 0.38)), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(patch)
    p_draw.ellipse([0, 0, patch.width, patch.height], fill=(19, 20, 24, 250))
    patch = patch.filter(ImageFilter.GaussianBlur(12))
    img_c.paste(patch, (chest_cx - patch.width//2, chest_cy - patch.height//2), patch)

    # Place clean Axiom Owl (no text above head!)
    clean_owl_w = int(w * 0.25)
    clean_owl_h = int(clean_owl_w * (owl_smokey.height / owl_smokey.width))
    clean_owl = owl_smokey.resize((clean_owl_w, clean_owl_h), Image.Resampling.LANCZOS)
    img_c.paste(clean_owl, (chest_cx - clean_owl_w // 2, chest_cy - clean_owl_h // 2), clean_owl)

    # Place Gothic Two-Tone "Axiom Allegiance" down the sleeve
    sleeve_gothic = gothic_two_tone.rotate(-60, expand=True, resample=Image.Resampling.BICUBIC)
    sg_w = int(w * 0.11)
    sg_h = int(sleeve_gothic.height * (sg_w / sleeve_gothic.width))
    sleeve_gothic_res = sleeve_gothic.resize((sg_w, sg_h), Image.Resampling.LANCZOS)
    img_c.paste(sleeve_gothic_res, (int(w * 0.14), int(h * 0.45)), sleeve_gothic_res)

    out_c = os.path.join(PUB_PRODUCTS, "axiom-crewneck-sweatshirt-studio.jpg")
    img_c.convert("RGB").save(out_c, "JPEG", quality=94, progressive=True)
    print(f"Saved: {out_c}")

    # Model Lookbook Crewneck
    base_model_c = os.path.join(BRAIN_DIR, "axiom_sweatshirt_model_1791592297053.jpg")
    if os.path.exists(base_model_c):
        img_mc = Image.open(base_model_c).convert("RGBA")
        mw, mh = img_mc.size
        # Dark patch over awkward top text
        mpatch = Image.new("RGBA", (int(mw * 0.30), int(mh * 0.30)), (0, 0, 0, 0))
        mp_draw = ImageDraw.Draw(mpatch)
        mp_draw.ellipse([0, 0, mpatch.width, mpatch.height], fill=(20, 20, 24, 245))
        mpatch = mpatch.filter(ImageFilter.GaussianBlur(10))
        img_mc.paste(mpatch, (int(mw * 0.35), int(mh * 0.30)), mpatch)

        # Place clean owl
        m_owl_w = int(mw * 0.20)
        m_owl_h = int(m_owl_w * (owl_smokey.height / owl_smokey.width))
        m_owl_res = owl_smokey.resize((m_owl_w, m_owl_h), Image.Resampling.LANCZOS)
        img_mc.paste(m_owl_res, (int(mw * 0.40), int(mh * 0.32)), m_owl_res)

        # Sleeve lettering on model
        m_sleeve_c = gothic_two_tone.rotate(-55, expand=True, resample=Image.Resampling.BICUBIC)
        ms_cw = int(mw * 0.08)
        ms_ch = int(m_sleeve_c.height * (ms_cw / m_sleeve_c.width))
        m_sc_res = m_sleeve_c.resize((ms_cw, ms_ch), Image.Resampling.LANCZOS)
        img_mc.paste(m_sc_res, (int(mw * 0.24), int(mh * 0.42)), m_sc_res)

        out_mc = os.path.join(PUB_PRODUCTS, "axiom-crewneck-sweatshirt-model.jpg")
        img_mc.convert("RGB").save(out_mc, "JPEG", quality=94, progressive=True)
        print(f"Saved: {out_mc}")

# =============================================================
# 5. RICHARDSON 112 HATS REWORK (GENUINE LEATHER PATCH WITH NEW LOGO)
# =============================================================
def render_richardson_patch_hats():
    print("Rendering Richardson 112 Hats: Laser-Etched Genuine Leather Patch with New Logo & Lettering...")
    # We render 3 colorways:
    # 1. Black / Charcoal Mesh
    # 2. Black / Royal Purple Mesh
    # 3. Black / Toxic Lime Mesh
    hat_styles = [
        ("axiom-r112-leather-patch-charcoal.jpg", (38, 40, 46), "BLACK / CHARCOAL MESH"),
        ("axiom-r112-leather-patch-purple.jpg", (55, 18, 75), "BLACK / ROYAL PURPLE MESH"),
        ("axiom-r112-leather-patch-lime.jpg", (25, 60, 20), "BLACK / TOXIC LIME MESH"),
    ]

    for filename, mesh_color, color_title in hat_styles:
        canvas = create_studio_bg(1024, 1024, bg_color=(11, 12, 15), glow_color=mesh_color)
        draw = ImageDraw.Draw(canvas)
        cx = 512

        draw.text((cx, 45), "AUTHENTIC RICHARDSON 112 // PRO TRUCKER SNAPBACK", fill=(138, 43, 226), font=font_sub, anchor="mm")
        draw.text((cx, 80), "GENUINE LEATHER PATCH EDITION", fill=(245, 245, 255), font=font_headline, anchor="mm")
        draw.text((cx, 115), color_title, fill=(57, 255, 20), font=font_label, anchor="mm")

        # Hat Crown & Visor Silhouette
        hat_w, hat_h = 620, 480
        hy = 230

        # Hat Shadow
        h_shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        hs_draw = ImageDraw.Draw(h_shadow)
        hs_draw.ellipse([cx - 320, hy + 380, cx + 320, hy + 490], fill=(0, 0, 0, 185))
        h_shadow = h_shadow.filter(ImageFilter.GaussianBlur(18))
        canvas = Image.alpha_composite(canvas, h_shadow)
        draw = ImageDraw.Draw(canvas)

        # Mesh Back Panels
        mesh_poly = [
            (cx - 260, hy + 240),
            (cx - 200, hy + 80),
            (cx, hy + 40),
            (cx + 200, hy + 80),
            (cx + 260, hy + 240),
            (cx + 200, hy + 340),
            (cx - 200, hy + 340),
        ]
        draw.polygon(mesh_poly, fill=(mesh_color[0]//2, mesh_color[1]//2, mesh_color[2]//2))
        # Mesh dot pattern
        for my in range(hy + 80, hy + 320, 12):
            for mx in range(cx - 240, cx + 240, 12):
                draw.point((mx, my), fill=(mesh_color[0], mesh_color[1], mesh_color[2], 120))

        # Front Structured Twill Panels (Midnight Obsidian)
        twill_poly = [
            (cx - 230, hy + 280),
            (cx - 170, hy + 100),
            (cx, hy + 50),
            (cx + 170, hy + 100),
            (cx + 230, hy + 280),
            (cx + 180, hy + 350),
            (cx - 180, hy + 350),
        ]
        draw.polygon(twill_poly, fill=(20, 20, 24), outline=(35, 36, 44), width=2)
        # Center seam
        draw.line([(cx, hy + 50), (cx, hy + 350)], fill=(14, 14, 18), width=3)

        # Pre-Curved Visor Bill
        bill_poly = [
            (cx - 280, hy + 340),
            (cx - 220, hy + 320),
            (cx, hy + 330),
            (cx + 220, hy + 320),
            (cx + 280, hy + 340),
            (cx + 240, hy + 450),
            (cx, hy + 490),
            (cx - 240, hy + 450),
        ]
        draw.polygon(bill_poly, fill=(16, 17, 20), outline=(28, 29, 36), width=2)
        # Contrast Visor Stitching
        draw.arc([cx - 220, hy + 340, cx + 220, hy + 470], start=10, end=170, fill=(138, 43, 226), width=2)
        draw.arc([cx - 210, hy + 350, cx + 210, hy + 460], start=10, end=170, fill=(57, 255, 20), width=1)

        # Genuine Leather Hexagon Patch
        patch_w, patch_h = 240, 150
        patch_cx, patch_cy = cx, hy + 220
        # Leather color: saddle tan / whiskey brown
        leather_base = (165, 110, 60)
        leather_border = (110, 65, 30)
        
        # Hexagonal patch
        hex_pts = [
            (patch_cx - patch_w//2, patch_cy),
            (patch_cx - patch_w//3, patch_cy - patch_h//2),
            (patch_cx + patch_w//3, patch_cy - patch_h//2),
            (patch_cx + patch_w//2, patch_cy),
            (patch_cx + patch_w//3, patch_cy + patch_h//2),
            (patch_cx - patch_w//3, patch_cy + patch_h//2),
        ]
        # Patch shadow
        p_shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        ps_draw = ImageDraw.Draw(p_shadow)
        ps_draw.polygon(hex_pts, fill=(0, 0, 0, 160))
        p_shadow = p_shadow.filter(ImageFilter.GaussianBlur(6))
        canvas = Image.alpha_composite(canvas, p_shadow)
        draw = ImageDraw.Draw(canvas)

        draw.polygon(hex_pts, fill=leather_base, outline=leather_border, width=3)
        # Perimeter stitch on leather
        draw.polygon([
            (patch_cx - patch_w//2 + 8, patch_cy),
            (patch_cx - patch_w//3 + 6, patch_cy - patch_h//2 + 6),
            (patch_cx + patch_w//3 - 6, patch_cy - patch_h//2 + 6),
            (patch_cx + patch_w//2 - 8, patch_cy),
            (patch_cx + patch_w//3 - 6, patch_cy + patch_h//2 - 6),
            (patch_cx - patch_w//3 + 6, patch_cy + patch_h//2 - 6),
        ], outline=(90, 50, 20), width=1)

        # Laser-Etched Graphic on Leather Patch:
        # Laser-engraved effect (dark deep burn: (60, 32, 14))
        # Owl logo:
        p_owl_h = 75
        p_owl_w = int(owl_smokey.width * (p_owl_h / owl_smokey.height))
        p_owl_res = owl_smokey.resize((p_owl_w, p_owl_h), Image.Resampling.LANCZOS)
        # Convert to burned leather monochrome
        p_owl_gray = p_owl_res.convert("L")
        p_owl_burned = ImageOps.colorize(p_owl_gray, black=(40, 20, 10), white=(180, 130, 80)).convert("RGBA")
        p_owl_burned.putalpha(p_owl_res.split()[-1])
        canvas.paste(p_owl_burned, (patch_cx - p_owl_w // 2, patch_cy - p_owl_h // 2 - 12), p_owl_burned)

        # Gothic Text below Owl on Leather:
        draw = ImageDraw.Draw(canvas)
        draw.text((patch_cx, patch_cy + 42), "AXIOM ALLEGIANCE", fill=(45, 22, 10), font=get_font(["impact.ttf", "arialbd.ttf"], 14), anchor="mm")
        draw.text((patch_cx, patch_cy + 56), "EST. 2024 • PRO DIVISION", fill=(95, 55, 25), font=get_font(["arial.ttf"], 8), anchor="mm")

        # Bottom specs badge
        draw.text((cx, 890), "• 100% FULL-GRAIN LEATHER PATCH • DEEP CO2 LASER ETCHED", fill=(170, 170, 185), font=font_micro, anchor="mm")
        draw.text((cx, 915), "• RICHARDSON 112 PRO-CROWN STRUCTURED TRUCKER SNAPBACK", fill=(170, 170, 185), font=font_micro, anchor="mm")
        draw.text((cx, 940), "• PRE-CURVED VISOR WITH CONTRAST STITCHING • 7-POSITION CLOSURE", fill=(170, 170, 185), font=font_micro, anchor="mm")

        out_p = os.path.join(PUB_PRODUCTS, filename)
        canvas.convert("RGB").save(out_p, "JPEG", quality=93, progressive=True)
        print(f"Saved: {out_p}")

def render_headwear_showcase():
    print("Rendering Headwear Showcase Banner...")
    W, H = 1600, 1000
    canvas = create_studio_bg(W, H, bg_color=(12, 13, 16), glow_color=(45, 15, 65))
    col_w = W // 3

    hat_paths = [
        (os.path.join(PUB_PRODUCTS, "axiom-r112-leather-patch-charcoal.jpg"), "FLAGSHIP LEATHER PATCH", "Richardson 112 Trucker Snapback\nLaser-Engraved Genuine Leather Patch\n$34.99"),
        (os.path.join(PUB_PRODUCTS, "axiom-r112-embroidered-black.jpg"), "3D PUFF DIRECT EMBROIDERED", "Richardson 112 Trucker Snapback\nHigh-Density Raised Satin Stitch\n$32.99"),
        (os.path.join(PUB_PRODUCTS, "axiom-dad-hat-washed-black.jpg"), "VINTAGE WASHED DAD HAT", "100% Chino Cotton Twill\nLow-Profile Relaxed Unstructured Fit\n$24.99"),
    ]

    for i, (p, title, desc) in enumerate(hat_paths):
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            iw, ih = im.size
            cropped = im.crop((int(iw * 0.08), int(ih * 0.12), int(iw * 0.92), int(ih * 0.88)))
            target_w = col_w - 50
            target_h = int(cropped.height * (target_w / cropped.width))
            if target_h > 580:
                target_h = 580
                target_w = int(cropped.width * (target_h / cropped.height))
            resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
            x = i * col_w + (col_w - target_w) // 2
            y = 150
            canvas.paste(resized, (x, y), resized)

    draw = ImageDraw.Draw(canvas)
    draw.text((W // 2, 45), "AXIOM ALLEGIANCE // OFFICIAL HEADWEAR LINE", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw.text((W // 2, 85), "PRO TRUCKER SNAPBACKS & STREETWEAR DAD HATS", fill=(57, 255, 20), font=font_headline, anchor="mm")

    for i, (_, title, desc) in enumerate(hat_paths):
        cx = i * col_w + col_w // 2
        draw.text((cx, 800), title, fill=(57, 255, 20), font=font_label, anchor="mm")
        y_off = 835
        for line in desc.split("\n"):
            draw.text((cx, y_off), line, fill=(185, 185, 200), font=font_micro, anchor="mm")
            y_off += 24

    showcase_out = os.path.join(PUB_PRODUCTS, "axiom-headwear-collection-showcase.jpg")
    canvas.convert("RGB").save(showcase_out, "JPEG", quality=94)
    print(f"Saved: {showcase_out}")

# =============================================================
# 6. CERAMIC GAMER MUG STYLE 2 (SMOKEY CREST + GOTHIC WORDMARK)
# =============================================================
def render_smokey_crest_mug():
    print("Rendering 2nd Style Mug: Midnight Obsidian Exterior, Electric Lime Interior, Smoky Crest...")
    canvas = create_studio_bg(1024, 1024, bg_color=(10, 11, 14), glow_color=(35, 65, 25))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 512, 510

    draw.text((cx, 45), "AXIOM ALLEGIANCE // PRO DRINKWARE SERIES", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw.text((cx, 80), "SMOKEY GOTHIC CREST CERAMIC MUG (15OZ)", fill=(245, 245, 255), font=font_headline, anchor="mm")
    draw.text((cx, 115), "MIDNIGHT OBSIDIAN EXTERIOR • ELECTRIC LIME GLAZED INTERIOR & HANDLE", fill=(57, 255, 20), font=font_label, anchor="mm")

    # Mug Base Dimensions
    mug_w, mug_h = 420, 450
    my = cy - mug_h // 2 + 30

    # Mug Floor Shadow
    m_shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    ms_draw = ImageDraw.Draw(m_shadow)
    ms_draw.ellipse([cx - mug_w//2 - 20, my + mug_h - 20, cx + mug_w//2 + 70, my + mug_h + 60], fill=(0, 0, 0, 180))
    m_shadow = m_shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, m_shadow)
    draw = ImageDraw.Draw(canvas)

    # Mug Handle (On Right: Electric Lime accent core with Obsidian grip)
    handle_x = cx + mug_w // 2 - 10
    handle_y = my + 80
    handle_w, handle_h = 130, 280
    # Outer handle
    draw.ellipse([handle_x, handle_y, handle_x + handle_w, handle_y + handle_h], fill=(22, 23, 27), outline=(57, 255, 20), width=4)
    # Inner cutout showing electric lime glaze
    draw.ellipse([handle_x + 35, handle_y + 35, handle_x + handle_w - 35, handle_y + handle_h - 35], fill=(10, 11, 14))

    # Mug Ceramic Body (Cylinder)
    draw.rounded_rectangle([cx - mug_w // 2, my, cx + mug_w // 2, my + mug_h], radius=18, fill=(18, 19, 23), outline=(32, 34, 40), width=2)

    # Ceramic cylindrical reflection highlights
    for x in range(cx - mug_w // 2 + 10, cx - mug_w // 2 + 90, 6):
        draw.line([(x, my + 15), (x, my + mug_h - 15)], fill=(38, 40, 48, 60), width=3)

    # Top Rim & Interior (ELECTRIC LIME GLAZE)
    # Outer rim lip
    draw.ellipse([cx - mug_w // 2, my - 35, cx + mug_w // 2, my + 35], fill=(16, 17, 20), outline=(57, 255, 20), width=4)
    # Lime glazed cavity
    draw.ellipse([cx - mug_w // 2 + 8, my - 28, cx + mug_w // 2 - 8, my + 28], fill=(30, 80, 20), outline=(57, 255, 20), width=2)
    # Deep inner liquid / interior shading
    draw.ellipse([cx - mug_w // 2 + 25, my - 20, cx + mug_w // 2 - 25, my + 20], fill=(18, 45, 14))

    # Graphic on Front of Mug:
    # 1. Centered Smoky Owl with Glowing Green Eyes
    m_owl_h = 220
    m_owl_w = int(owl_smokey.width * (m_owl_h / owl_smokey.height))
    m_owl_res = owl_smokey.resize((m_owl_w, m_owl_h), Image.Resampling.LANCZOS)
    canvas.paste(m_owl_res, (cx - m_owl_w // 2, my + 75), m_owl_res)

    # 2. Two-Tone Gothic "Axiom Allegiance" below Owl
    m_g_w = 340
    m_g_h = int(gothic_two_tone.height * (m_g_w / gothic_two_tone.width))
    m_g_res = gothic_two_tone.resize((m_g_w, m_g_h), Image.Resampling.LANCZOS)
    canvas.paste(m_g_res, (cx - m_g_w // 2, my + 305), m_g_res)

    draw = ImageDraw.Draw(canvas)
    # Bottom callouts
    draw.text((cx, 895), "15 OZ JUMBO GAMER CAPACITY • 100% HIGH-DURABILITY CERAMIC", fill=(220, 220, 235), font=font_label, anchor="mm")
    draw.text((cx, 930), "MICROWAVE & DISHWASHER SAFE • HIGH-GLOSS SCRATCH RESISTANT FINISH", fill=(57, 255, 20), font=font_micro, anchor="mm")

    out_p = os.path.join(PUB_PRODUCTS, "axiom-mug-smokey-crest-15oz.png")
    canvas.save(out_p, "PNG")
    print(f"Saved: {out_p}")

if __name__ == "__main__":
    render_wrist_pad_tournament_edition()
    render_wrist_pad_stealth_setup()
    render_joggers_model_lookbook()
    render_joggers_studio_heavyweight()
    render_hoodie_studio_and_model()
    render_crewneck_studio_and_model()
    render_richardson_patch_hats()
    render_headwear_showcase()
    render_smokey_crest_mug()
    print("ALL REDESIGNS AND PRODUCT RENDERS COMPLETED SUCCESSFULLY!")
