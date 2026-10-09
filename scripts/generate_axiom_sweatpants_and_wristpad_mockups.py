import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
GAMING_DIR = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")
BRAIN_DIR = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7"

os.makedirs(PUB_PRODUCTS, exist_ok=True)

# Load Owl Logo
owl_path = os.path.join(GAMING_DIR, "axiom-owl-mascot.png")
owl_img = Image.open(owl_path).convert("RGBA") if os.path.exists(owl_path) else None

def get_font(name_list, size):
    for n in name_list:
        try:
            return ImageFont.truetype(n, size)
        except:
            pass
    return ImageFont.load_default()

font_title = get_font(["impact.ttf", "arialbd.ttf"], 36)
font_label = get_font(["arialbd.ttf", "arial.ttf"], 22)
font_sub = get_font(["arial.ttf"], 18)
font_micro = get_font(["arial.ttf"], 14)

def create_dark_studio_canvas(w=1024, h=1024, bg=(14, 15, 18), accent=(45, 20, 65)):
    canvas = Image.new("RGBA", (w, h), (bg[0], bg[1], bg[2], 255))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    cx, cy = w // 2, h // 2
    for r in range(int(w * 0.45), 0, -15):
        alpha = int(35 * (1.0 - r / (w * 0.45)))
        draw.ellipse([cx - r, cy - int(r * 0.8), cx + r, cy + int(r * 0.8)], fill=(accent[0], accent[1], accent[2], alpha))
    return Image.alpha_composite(canvas, glow)

# -------------------------------------------------------------
# 1. GENERATE STUDIO SWEATPANTS MOCKUP (PRO & CORE)
# -------------------------------------------------------------
def generate_sweatpants_mockup(is_pro=True):
    edition_name = "Pro Heavyweight 450 GSM" if is_pro else "Core Everyday Fleece"
    filename = "axiom-sweatpants-pro-heavyweight-studio.jpg" if is_pro else "axiom-sweatpants-core-everyday-studio.jpg"
    print(f"Generating Sweatpants Mockup: {edition_name}...")

    canvas = create_dark_studio_canvas(1024, 1024, bg=(12, 13, 16), accent=(50, 15, 75) if is_pro else (25, 45, 30))
    cx, cy = 512, 510

    # Draw soft garment floor shadow
    shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 260, cy + 390, cx + 260, cy + 440], fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)

    draw = ImageDraw.Draw(canvas)

    # Sweatpants Silhouette Coordinates
    # Waistband: y=130 to 180, width 380
    waist_left = cx - 180
    waist_right = cx + 180
    waist_top = 140
    waist_bot = 190

    # Outer hips down to ankle cuffs
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
        right_hip,
        right_knee,
        right_ankle_out,
        right_ankle_in,
        (cx + 60, 600),
        left_crotch,
        (cx - 60, 600),
        left_ankle_in,
        left_ankle_out,
        left_knee,
        left_hip,
    ]

    # Fill Matte Jet Black Fabric
    fabric_color = (20, 20, 22) if is_pro else (25, 25, 28)
    draw.polygon(pant_poly, fill=fabric_color)

    # Shading and Seams
    # Crotch inseam & leg creases
    draw.line([left_crotch, (cx, 320)], fill=(12, 12, 14), width=3)
    draw.line([left_crotch, (cx - 60, 600), left_ankle_in], fill=(12, 12, 14), width=2)
    draw.line([left_crotch, (cx + 60, 600), right_ankle_in], fill=(12, 12, 14), width=2)

    # Subtle fabric fold highlights
    for dy in range(250, 750, 60):
        draw.line([(cx - 140, dy), (cx - 40, dy + 25)], fill=(28, 28, 32), width=3)
        draw.line([(cx + 40, dy + 20), (cx + 140, dy)], fill=(28, 28, 32), width=3)

    # Ribbed Waistband
    draw.rectangle([waist_left - 10, waist_top, waist_right + 10, waist_bot], fill=(16, 16, 18), outline=(35, 35, 40), width=2)
    for wx in range(waist_left, waist_right, 8):
        draw.line([(wx, waist_top + 2), (wx, waist_bot - 2)], fill=(28, 28, 32), width=2)

    # Ribbed Ankle Cuffs
    # Left Cuff
    draw.rectangle([left_ankle_out[0], left_ankle_out[1], left_ankle_in[0], left_ankle_out[1] + 35], fill=(16, 16, 18), outline=(32, 32, 36), width=2)
    for cx_line in range(int(left_ankle_out[0] + 5), int(left_ankle_in[0]), 6):
        draw.line([(cx_line, left_ankle_out[1] + 2), (cx_line, left_ankle_out[1] + 33)], fill=(26, 26, 30), width=2)

    # Right Cuff
    draw.rectangle([right_ankle_in[0], right_ankle_out[1], right_ankle_out[0], right_ankle_out[1] + 35], fill=(16, 16, 18), outline=(32, 32, 36), width=2)
    for cx_line in range(int(right_ankle_in[0] + 5), int(right_ankle_out[0]), 6):
        draw.line([(cx_line, right_ankle_out[1] + 2), (cx_line, right_ankle_out[1] + 33)], fill=(26, 26, 30), width=2)

    # Side Pockets
    draw.line([(waist_left - 5, waist_bot + 10), (waist_left - 25, 340)], fill=(12, 12, 14), width=4)
    draw.line([(waist_right + 5, waist_bot + 10), (waist_right + 25, 340)], fill=(12, 12, 14), width=4)

    # DUAL-TONE PURPLE & NEON GREEN DRAWSTRINGS!
    # Left String = Royal Purple with Toxic Green dipped aglet
    draw.line([(cx - 20, waist_bot - 5), (cx - 28, waist_bot + 60), (cx - 24, waist_bot + 120)], fill=(138, 43, 226), width=6)
    draw.rectangle([cx - 27, waist_bot + 120, cx - 21, waist_bot + 140], fill=(57, 255, 20)) # Neon green aglet

    # Right String = Neon Toxic Green with Royal Purple dipped aglet
    draw.line([(cx + 20, waist_bot - 5), (cx + 26, waist_bot + 65), (cx + 20, waist_bot + 125)], fill=(57, 255, 20), width=6)
    draw.rectangle([cx + 17, waist_bot + 125, cx + 23, waist_bot + 145], fill=(138, 43, 226)) # Royal purple aglet

    # Waistband eyelets
    draw.ellipse([cx - 26, waist_bot - 10, cx - 14, waist_bot + 2], fill=(45, 45, 50), outline=(80, 80, 90), width=1)
    draw.ellipse([cx + 14, waist_bot - 10, cx + 26, waist_bot + 2], fill=(45, 45, 50), outline=(80, 80, 90), width=1)

    # RIGHT LEG (User's left): AXIOM OWL CREST
    if owl_img:
        owl_scale = 135 / max(owl_img.width, owl_img.height)
        owl_resized = owl_img.resize((int(owl_img.width * owl_scale), int(owl_img.height * owl_scale)), Image.Resampling.LANCZOS)
        # Position on right upper thigh
        canvas.paste(owl_resized, (cx + 60, 270), owl_resized)

    # LEFT LEG (User's right): VERTICAL ATHLETIC TEXT "AXIOM ALLEGIANCE"
    # Render clean athletic text vertically
    vert_text_img = Image.new("RGBA", (800, 140), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vert_text_img)
    v_font = get_font(["impact.ttf", "arialbd.ttf"], 54)

    # Clean athletic bold text: "AXIOM" in Neon Toxic Green, "ALLEGIANCE" in Royal Purple with clean bold LL
    v_draw.text((30, 30), "AXIOM  ", fill=(57, 255, 20), font=v_font)
    bbox = v_draw.textbbox((30, 30), "AXIOM  ", font=v_font)
    v_draw.text((bbox[2], 30), "ALLEGIANCE", fill=(175, 100, 255), font=v_font)

    # Rotate 90 degrees to run vertically down the pant leg
    vert_rotated = vert_text_img.rotate(270, expand=True, resample=Image.Resampling.BICUBIC)
    # Scale down slightly to fit leg nicely
    target_h = 440
    scale_v = target_h / vert_rotated.height
    vert_scaled = vert_rotated.resize((int(vert_rotated.width * scale_v), target_h), Image.Resampling.LANCZOS)

    # Paste along left pant leg
    canvas.paste(vert_scaled, (cx - 155, 310), vert_scaled)

    # Header / Spec Banner
    draw = ImageDraw.Draw(canvas)
    draw.text((cx, 55), "AXIOM ALLEGIANCE // OFFICIAL TEAM FLEECE", fill=(138, 43, 226), font=font_label, anchor="mm")
    draw.text((cx, 85), f"{edition_name.upper()} JOGGERS", fill=(57, 255, 20), font=font_title, anchor="mm")

    # Lower spec callouts
    draw.text((cx - 240, 960), "• DUAL PURPLE & GREEN DRAWSTRINGS", fill=(180, 180, 190), font=font_micro, anchor="mm")
    draw.text((cx, 960), "• VERTICAL 'AXIOM ALLEGIANCE' PRINT", fill=(180, 180, 190), font=font_micro, anchor="mm")
    draw.text((cx + 240, 960), "• EMBROIDERED TEAM OWL CREST", fill=(180, 180, 190), font=font_micro, anchor="mm")

    out_path = os.path.join(PUB_PRODUCTS, filename)
    canvas.convert("RGB").save(out_path, "JPEG", quality=92, progressive=True)
    print(f"Saved: {out_path} ({os.path.getsize(out_path)//1024} KB)")

# -------------------------------------------------------------
# 2. GENERATE CUSTOM KEYBOARD WRIST REST MOCKUPS (2 VERSIONS + 3 SIZES)
# -------------------------------------------------------------
def generate_wrist_rest_mockups():
    print("Generating Custom Keyboard Wrist Rest Mockups...")

    # VERSION 1: PRO TOURNAMENT TOXIC SHARDS EDITION (Hero + 3 Sizes Comparison)
    v1_canvas = create_dark_studio_canvas(1024, 1024, bg=(10, 12, 15), accent=(30, 60, 25))
    v1_draw = ImageDraw.Draw(v1_canvas)
    cx = 512

    # Title
    v1_draw.text((cx, 60), "AXIOM ALLEGIANCE // PRO ESPORTS HARDWARE", fill=(138, 43, 226), font=font_label, anchor="mm")
    v1_draw.text((cx, 95), "ERGONOMIC GAMING KEYBOARD WRIST REST", fill=(57, 255, 20), font=font_title, anchor="mm")
    v1_draw.text((cx, 130), "HIGH-DENSITY MEMORY FOAM • ANTI-SLIP BASE • 3 SIZES AVAILABLE", fill=(160, 160, 175), font=font_micro, anchor="mm")

    # Draw 3 Wrist Rest Sizes Stacked / Compared:
    sizes = [
        ("FULL-SIZE (100% / 104-KEY) — 17.3\" x 3.9\" (440 x 100 mm)", 780, 105, 230),
        ("TENKEYLESS (TKL 80% / 87-KEY) — 14.2\" x 3.9\" (360 x 100 mm)", 640, 100, 430),
        ("COMPACT (60% / 65% / 75-KEY) — 11.8\" x 3.9\" (300 x 100 mm)", 520, 95, 620),
    ]

    for label, pad_w, pad_h, pad_y in sizes:
        px1 = cx - pad_w // 2
        px2 = cx + pad_w // 2
        py1 = pad_y
        py2 = pad_y + pad_h

        # Label above each pad
        v1_draw.text((cx, py1 - 18), label, fill=(57, 255, 20), font=font_micro, anchor="mm")

        # Floor drop shadow for 3D cushion depth
        shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.rounded_rectangle([px1 - 8, py1 + 8, px2 + 8, py2 + 18], radius=14, fill=(0, 0, 0, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        v1_canvas = Image.alpha_composite(v1_canvas, shadow)
        v1_draw = ImageDraw.Draw(v1_canvas)

        # Base wrist rest body (Beveled Obsidian Black Ergonomic Foam)
        v1_draw.rounded_rectangle([px1, py1, px2, py2], radius=12, fill=(18, 19, 23), outline=(138, 43, 226), width=2)

        # Dynamic Toxic Lime & Royal Purple Speed Shards Pattern
        # Draw angular speed shards across the wrist rest surface
        shards_img = Image.new("RGBA", (pad_w, pad_h), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shards_img)
        # Green speed slice
        sh_draw.polygon([(pad_w - 240, 0), (pad_w - 120, 0), (pad_w - 180, pad_h), (pad_w - 300, pad_h)], fill=(57, 255, 20, 45))
        sh_draw.polygon([(pad_w - 140, 0), (pad_w - 60, 0), (pad_w - 110, pad_h), (pad_w - 190, pad_h)], fill=(138, 43, 226, 60))
        sh_draw.line([(0, pad_h - 4), (pad_w, pad_h - 4)], fill=(57, 255, 20, 180), width=2)
        v1_canvas.paste(shards_img, (px1, py1), shards_img)
        v1_draw = ImageDraw.Draw(v1_canvas)

        # Anti-fray perimeter stitching effect
        v1_draw.rounded_rectangle([px1 + 3, py1 + 3, px2 - 3, py2 - 3], radius=10, outline=(70, 30, 110), width=1)

        # Left typography: Clean athletic bold "AXIOM ALLEGIANCE"
        text_size = 22 if pad_w > 600 else 18
        w_font = get_font(["impact.ttf", "arialbd.ttf"], text_size)
        v1_draw.text((px1 + 35, py1 + pad_h // 2), "AXIOM ALLEGIANCE", fill=(240, 240, 255), font=w_font, anchor="lm")
        # Subtitle
        v1_draw.text((px1 + 35, py1 + pad_h // 2 + 20), "PRO TOURNAMENT SPEC", fill=(57, 255, 20), font=get_font(["arial.ttf"], 11), anchor="lm")

        # Right Mascot: Axiom Owl Crest
        if owl_img:
            owl_h = int(pad_h * 0.75)
            owl_scale = owl_h / owl_img.height
            owl_w = int(owl_img.width * owl_scale)
            owl_pad = owl_img.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
            v1_canvas.paste(owl_pad, (px2 - owl_w - 30, py1 + (pad_h - owl_h) // 2), owl_pad)
            v1_draw = ImageDraw.Draw(v1_canvas)

    # Footer callouts
    v1_draw.text((cx - 280, 940), "• ULTRA-DENSE MEMORY FOAM", fill=(170, 170, 185), font=font_micro, anchor="mm")
    v1_draw.text((cx, 940), "• SILKY LYCRA GLIDE SURFACE", fill=(170, 170, 185), font=font_micro, anchor="mm")
    v1_draw.text((cx + 280, 940), "• TEXTURED ANTI-SLIP RUBBER", fill=(170, 170, 185), font=font_micro, anchor="mm")

    out_v1 = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-tournament-edition.jpg")
    v1_canvas.convert("RGB").save(out_v1, "JPEG", quality=92, progressive=True)
    print(f"Saved: {out_v1} ({os.path.getsize(out_v1)//1024} KB)")

    # VERSION 2: AXIOM STEALTH MIDNIGHT PURPLE EDITION (Mechanical Keyboard Battlestation In-Use Setup)
    v2_canvas = create_dark_studio_canvas(1024, 1024, bg=(10, 10, 14), accent=(45, 15, 65))
    v2_draw = ImageDraw.Draw(v2_canvas)

    v2_draw.text((cx, 60), "AXIOM ALLEGIANCE // STEALTH BLACKOUT EDITION", fill=(138, 43, 226), font=font_label, anchor="mm")
    v2_draw.text((cx, 95), "TACTICAL MEMORY FOAM WRIST PAD", fill=(230, 230, 245), font=font_title, anchor="mm")

    # Draw mechanical keyboard silhouette above the wrist rest
    kb_w, kb_h = 740, 240
    kb_y = 220
    v2_draw.rounded_rectangle([cx - kb_w//2, kb_y, cx + kb_w//2, kb_y + kb_h], radius=10, fill=(20, 20, 24), outline=(40, 40, 48), width=2)
    # Keyboard RGB backlight underglow
    v2_draw.line([(cx - kb_w//2 + 20, kb_y + kb_h - 2), (cx + kb_w//2 - 20, kb_y + kb_h - 2)], fill=(138, 43, 226), width=3)
    # Keycaps pattern
    for r in range(5):
        ky = kb_y + 25 + r * 40
        for c in range(16):
            kx = cx - kb_w//2 + 35 + c * 42
            v2_draw.rounded_rectangle([kx, ky, kx + 36, ky + 34], radius=4, fill=(30, 31, 38), outline=(45, 46, 56), width=1)

    v2_draw.text((cx, kb_y + kb_h // 2), "[ MECHANICAL GAMING KEYBOARD SETUP ]", fill=(100, 105, 120), font=font_sub, anchor="mm")

    # Wrist Rest Positioned Directly Below Keyboard
    wr_w, wr_h = 740, 130
    wr_y = kb_y + kb_h + 30

    # Shadow
    w_shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    ws_draw = ImageDraw.Draw(w_shadow)
    ws_draw.rounded_rectangle([cx - wr_w//2 - 10, wr_y + 10, cx + wr_w//2 + 10, wr_y + wr_h + 20], radius=16, fill=(0, 0, 0, 180))
    w_shadow = w_shadow.filter(ImageFilter.GaussianBlur(12))
    v2_canvas = Image.alpha_composite(v2_canvas, w_shadow)
    v2_draw = ImageDraw.Draw(v2_canvas)

    # Stealth Pad Body
    v2_draw.rounded_rectangle([cx - wr_w//2, wr_y, cx + wr_w//2, wr_y + wr_h], radius=14, fill=(16, 16, 20), outline=(80, 40, 120), width=2)
    # Center metallic Owl emblem
    if owl_img:
        owl_h = int(wr_h * 0.75)
        owl_scale = owl_h / owl_img.height
        owl_w = int(owl_img.width * owl_scale)
        owl_stealth = owl_img.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
        v2_canvas.paste(owl_stealth, (cx - owl_w // 2, wr_y + (wr_h - owl_h) // 2), owl_stealth)
        v2_draw = ImageDraw.Draw(v2_canvas)

    # Clean Athletic Typography at Left & Creed Motto at Right
    v2_draw.text((cx - wr_w//2 + 40, wr_y + wr_h//2), "AXIOM ALLEGIANCE", fill=(175, 120, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 22), anchor="lm")
    v2_draw.text((cx + wr_w//2 - 40, wr_y + wr_h//2), "“PLAY TO REIGN”", fill=(57, 255, 20), font=get_font(["impact.ttf", "arialbd.ttf"], 18), anchor="rm")

    # Inset Details / Macro Callouts at bottom
    v2_draw.rounded_rectangle([cx - 380, 720, cx - 140, 890], radius=10, fill=(18, 19, 24), outline=(40, 40, 50), width=1)
    v2_draw.text((cx - 260, 750), "1. ERGONOMIC ANGLE", fill=(57, 255, 20), font=font_micro, anchor="mm")
    v2_draw.text((cx - 260, 810), "Neutral 15° wrist slope\nprevents carpal fatigue", fill=(160, 160, 175), font=get_font(["arial.ttf"], 12), anchor="mm")

    v2_draw.rounded_rectangle([cx - 120, 720, cx + 120, 890], radius=10, fill=(18, 19, 24), outline=(40, 40, 50), width=1)
    v2_draw.text((cx, 750), "2. MEMORY FOAM CORE", fill=(57, 255, 20), font=font_micro, anchor="mm")
    v2_draw.text((cx, 810), "Slow-rebound 45D poly\nwith cooling gel layer", fill=(160, 160, 175), font=get_font(["arial.ttf"], 12), anchor="mm")

    v2_draw.rounded_rectangle([cx + 140, 720, cx + 380, 890], radius=10, fill=(18, 19, 24), outline=(40, 40, 50), width=1)
    v2_draw.text((cx + 260, 750), "3. NON-SLIP RUBBER", fill=(57, 255, 20), font=font_micro, anchor="mm")
    v2_draw.text((cx + 260, 810), "Textured chevron grip\nstays locked on desk", fill=(160, 160, 175), font=get_font(["arial.ttf"], 12), anchor="mm")

    out_v2 = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-stealth-setup.jpg")
    v2_canvas.convert("RGB").save(out_v2, "JPEG", quality=92, progressive=True)
    print(f"Saved: {out_v2} ({os.path.getsize(out_v2)//1024} KB)")

if __name__ == "__main__":
    generate_sweatpants_mockup(is_pro=True)
    generate_sweatpants_mockup(is_pro=False)
    generate_wrist_rest_mockups()
