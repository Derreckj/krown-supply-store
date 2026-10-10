import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUB_BRANDING = os.path.join(BASE_DIR, "public", "images", "branding")
CONST_DIR = os.path.join(PUB_BRANDING, "construction")

os.makedirs(PUB_PRODUCTS, exist_ok=True)

def get_font(name_list, size):
    for n in name_list:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()

font_heavy = get_font(["impact.ttf", "arialbd.ttf"], 32)
font_title = get_font(["arialbd.ttf", "arial.ttf"], 24)
font_sub = get_font(["arialbd.ttf", "arial.ttf"], 18)
font_micro = get_font(["arial.ttf"], 12)

# Load Construction logos
kc_candidates = [
    os.path.join(CONST_DIR, "KC logo black and gold.png"),
    os.path.join(CONST_DIR, "KC logo by itself.png"),
    os.path.join(CONST_DIR, "KC.png"),
    os.path.join(CONST_DIR, "KC.jpg"),
]
kc_logo_path = None
for c in kc_candidates:
    if os.path.exists(c):
        kc_logo_path = c
        break

# Load Supply Co logo
krown_crown_path = os.path.join(PUB_BRANDING, "krown-authentic-embroidered-gold-crown.png")
if not os.path.exists(krown_crown_path):
    krown_crown_path = os.path.join(PUB_BRANDING, "krown-definitive-logo.png")

# Use Axiom clean shaker photos as the photorealistic base geometry
base_tritan_src = os.path.join(PUB_PRODUCTS, "axiom-shaker-stealth-tritan-clean.jpg")
if not os.path.exists(base_tritan_src):
    base_tritan_src = os.path.join(PUB_PRODUCTS, "axiom-shaker-signature-tritan-clean.jpg")

base_steel_src = os.path.join(PUB_PRODUCTS, "axiom-shaker-stealth-steel-clean.jpg")
if not os.path.exists(base_steel_src):
    base_steel_src = os.path.join(PUB_PRODUCTS, "axiom-shaker-signature-steel-clean.jpg")

def render_bottle_variant(base_path, brand, design_name, is_steel, out_filename, primary_accent, secondary_accent, badge_type):
    print(f"Rendering shaker: {out_filename} ({brand} - {design_name} - {'Steel' if is_steel else 'Tritan'})...")
    
    # Load base bottle
    base_img = Image.open(base_path).convert("RGBA")
    w, h = base_img.size

    # Isolate bottle canvas
    canvas = base_img.copy()

    # The front bottle face roughly spans x: [w*0.30, w*0.70], y: [h*0.32, h*0.72]
    # Cap is roughly y: [h*0.08, h*0.30]
    # Let's clean the bottle center body where old logo was
    clean_box = (int(w * 0.32), int(h * 0.35), int(w * 0.68), int(h * 0.72))
    
    # Sample body background color
    if is_steel:
        if "obsidian" in design_name.lower() or "black" in design_name.lower():
            body_color = (20, 21, 23, 255)
        elif "steel" in design_name.lower() or "brushed" in design_name.lower() or "titanium" in design_name.lower():
            body_color = (65, 68, 74, 255)
        else:
            body_color = (30, 32, 36, 255)
    else:
        # Tritan frosted
        if "smoke" in design_name.lower() or "obsidian" in design_name.lower():
            body_color = (25, 27, 30, 245)
        elif "grey" in design_name.lower() or "concrete" in design_name.lower():
            body_color = (45, 48, 52, 240)
        else:
            body_color = (28, 30, 34, 240)

    # Clean the center bottle body with subtle vertical sheen
    body_overlay = Image.new("RGBA", (clean_box[2] - clean_box[0], clean_box[3] - clean_box[1]), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(body_overlay)
    bw, bh = body_overlay.size
    for x in range(bw):
        t = x / bw
        # subtle cylindrical gradient
        factor = 0.85 + 0.35 * math.sin(t * math.pi)
        col = tuple(int(min(255, c * factor)) for c in body_color[:3]) + (body_color[3],)
        b_draw.line([(x, 0), (x, bh)], fill=col)
    
    # Soft blend edges
    body_overlay = body_overlay.filter(ImageFilter.GaussianBlur(4))
    canvas.paste(body_overlay, (clean_box[0], clean_box[1]), body_overlay)

    # Color lid accents (cap loop / silicone band)
    lid_y1, lid_y2 = int(h * 0.18), int(h * 0.28)
    lid_band = Image.new("RGBA", (int(w * 0.36), lid_y2 - lid_y1), (0, 0, 0, 0))
    lb_draw = ImageDraw.Draw(lid_band)
    lb_w, lb_h = lid_band.size
    
    # Tint lid band with primary accent
    for y in range(lb_h):
        alpha = int(120 * math.sin((y / lb_h) * math.pi))
        lb_draw.line([(0, y), (lb_w, y)], fill=primary_accent + (alpha,))
    lid_band = lid_band.filter(ImageFilter.GaussianBlur(3))
    canvas.paste(lid_band, (int(w * 0.32), lid_y1), lid_band)

    # Now composite the brand badge onto the bottle center
    center_x = int(w * 0.50)
    center_y = int(h * 0.52)

    if brand == "KrowN Construction":
        # Draw Construction Badge
        # Outer industrial hexagon or shield seal
        badge_w = int(w * 0.28)
        badge_h = int(badge_w * 1.15)
        badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(badge)

        # Hexagon points
        cx, cy = badge_w / 2, badge_h / 2
        r = badge_w * 0.48
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            points.append((cx + r * math.cos(angle_rad), cy + r * math.sin(angle_rad)))
        
        # Hexagon fill & borders
        bg_draw.polygon(points, fill=(15, 16, 18, 230), outline=primary_accent + (255,), width=3)
        # Inner accent ring
        inner_r = r * 0.88
        inner_points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            inner_points.append((cx + inner_r * math.cos(angle_rad), cy + inner_r * math.sin(angle_rad)))
        bg_draw.polygon(inner_points, outline=secondary_accent + (200,), width=1)

        # Text: KC / KrowN Construction / BUILT TO REIGN
        f_kc = get_font(["impact.ttf", "arialbd.ttf"], int(badge_w * 0.32))
        f_sub = get_font(["arialbd.ttf"], int(badge_w * 0.085))
        f_slogan = get_font(["arialbd.ttf"], int(badge_w * 0.075))

        # KC Monogram
        bg_draw.text((cx, cy - badge_h * 0.16), "KC", font=f_kc, fill=primary_accent + (255,), anchor="mm")
        # Line
        bg_draw.line([(cx - badge_w * 0.32, cy - badge_h * 0.02), (cx + badge_w * 0.32, cy - badge_h * 0.02)], fill=secondary_accent + (220,), width=2)
        # KROWN CONSTRUCTION
        bg_draw.text((cx, cy + badge_h * 0.08), "KROWN", font=f_sub, fill=(245, 245, 245, 255), anchor="mm")
        bg_draw.text((cx, cy + badge_h * 0.17), "CONSTRUCTION", font=f_sub, fill=(200, 200, 200, 255), anchor="mm")
        # BUILT TO REIGN
        bg_draw.text((cx, cy + badge_h * 0.28), "BUILT TO REIGN", font=f_slogan, fill=primary_accent + (255,), anchor="mm")

        # Soft drop shadow for badge
        badge_shadow = Image.new("RGBA", (badge_w + 20, badge_h + 20), (0, 0, 0, 0))
        bs_draw = ImageDraw.Draw(badge_shadow)
        bs_points = [(p[0] + 10, p[1] + 12) for p in points]
        bs_draw.polygon(bs_points, fill=(0, 0, 0, 160))
        badge_shadow = badge_shadow.filter(ImageFilter.GaussianBlur(6))

        canvas.paste(badge_shadow, (center_x - badge_w // 2 - 10, center_y - badge_h // 2 - 8), badge_shadow)
        canvas.paste(badge, (center_x - badge_w // 2, center_y - badge_h // 2), badge)

    else:
        # KrowN Supply Co.
        # Luxury minimalist aesthetic: Gold crown monogram + WEAR THE KROWN + KrowN Supply Co.
        cw = int(w * 0.24)
        crown_im = Image.open(krown_crown_path).convert("RGBA")
        ch = int(crown_im.height * (cw / crown_im.width))
        crown_res = crown_im.resize((cw, ch), Image.Resampling.LANCZOS)

        # Crown drop shadow
        cs = Image.new("RGBA", (cw + 16, ch + 16), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(cs)
        cs_draw.ellipse([4, 6, cw + 12, ch + 12], fill=(0, 0, 0, 180))
        cs = cs.filter(ImageFilter.GaussianBlur(5))

        canvas.paste(cs, (center_x - cw // 2 - 4, center_y - ch // 2 - int(h * 0.05)), cs)
        canvas.paste(crown_res, (center_x - cw // 2, center_y - ch // 2 - int(h * 0.05)), crown_res)

        # Luxury Typography underneath
        txt_box = Image.new("RGBA", (int(w * 0.40), int(h * 0.16)), (0, 0, 0, 0))
        t_draw = ImageDraw.Draw(txt_box)
        tcx = txt_box.width // 2

        f_brand = get_font(["arialbd.ttf", "impact.ttf"], int(cw * 0.19))
        f_co = get_font(["arial.ttf"], int(cw * 0.13))
        f_slogan = get_font(["arialbd.ttf"], int(cw * 0.12))

        t_draw.text((tcx, int(txt_box.height * 0.22)), "K R O W N", font=f_brand, fill=primary_accent + (255,), anchor="mm")
        t_draw.text((tcx, int(txt_box.height * 0.46)), "SUPPLY CO.", font=f_co, fill=(235, 235, 235, 240), anchor="mm")
        # Line
        t_draw.line([(tcx - cw * 0.35, int(txt_box.height * 0.64)), (tcx + cw * 0.35, int(txt_box.height * 0.64))], fill=secondary_accent + (200,), width=1)
        t_draw.text((tcx, int(txt_box.height * 0.82)), "WEAR THE KROWN", font=f_slogan, fill=primary_accent + (255,), anchor="mm")

        canvas.paste(txt_box, (center_x - txt_box.width // 2, center_y + ch // 2 - int(h * 0.03)), txt_box)

    out_path = os.path.join(PUB_PRODUCTS, out_filename)
    canvas.convert("RGB").save(out_path, "JPEG", quality=95)
    print(f"-> Generated: {out_path}")

# Run generation for all 12 variants + 2 lineups
# 1. KrowN Construction Shakers
render_bottle_variant(base_tritan_src, "KrowN Construction", "High-Vis Gold & Black", False, "kc-shaker-highvis-tritan.jpg", (226, 179, 78), (255, 215, 0), "hex")
render_bottle_variant(base_steel_src, "KrowN Construction", "High-Vis Gold & Black", True, "kc-shaker-highvis-steel.jpg", (226, 179, 78), (255, 215, 0), "hex")

render_bottle_variant(base_tritan_src, "KrowN Construction", "Steel Core Titanium", False, "kc-shaker-steelcore-tritan.jpg", (195, 202, 212), (240, 240, 245), "hex")
render_bottle_variant(base_steel_src, "KrowN Construction", "Steel Core Titanium", True, "kc-shaker-steelcore-steel.jpg", (195, 202, 212), (240, 240, 245), "hex")

render_bottle_variant(base_tritan_src, "KrowN Construction", "Jobsite Lime & Purple", False, "kc-shaker-jobsite-tritan.jpg", (50, 205, 50), (147, 51, 234), "hex")
render_bottle_variant(base_steel_src, "KrowN Construction", "Jobsite Lime & Purple", True, "kc-shaker-jobsite-steel.jpg", (50, 205, 50), (147, 51, 234), "hex")

# 2. KrowN Supply Co. Shakers
render_bottle_variant(base_tritan_src, "KrowN Supply Co.", "Obsidian Black & Gold", False, "krown-shaker-obsidian-tritan.jpg", (212, 175, 55), (255, 223, 100), "crown")
render_bottle_variant(base_steel_src, "KrowN Supply Co.", "Obsidian Black & Gold", True, "krown-shaker-obsidian-steel.jpg", (212, 175, 55), (255, 223, 100), "crown")

render_bottle_variant(base_tritan_src, "KrowN Supply Co.", "Frosted Smoke & Polished Gold", False, "krown-shaker-smoke-tritan.jpg", (220, 185, 80), (255, 235, 140), "crown")
render_bottle_variant(base_steel_src, "KrowN Supply Co.", "Frosted Smoke & Polished Gold", True, "krown-shaker-smoke-steel.jpg", (220, 185, 80), (255, 235, 140), "crown")

render_bottle_variant(base_tritan_src, "KrowN Supply Co.", "Brushed Steel & Minimal Crown", False, "krown-shaker-brushed-tritan.jpg", (200, 205, 215), (230, 230, 240), "crown")
render_bottle_variant(base_steel_src, "KrowN Supply Co.", "Brushed Steel & Minimal Crown", True, "krown-shaker-brushed-steel.jpg", (200, 205, 215), (230, 230, 240), "crown")

# Lineup images
def create_lineup(items, out_name, title_text):
    imgs = [Image.open(os.path.join(PUB_PRODUCTS, fn)) for fn in items]
    w, h = imgs[0].size
    lineup = Image.new("RGB", (w * len(imgs), h), (18, 19, 21))
    for i, im in enumerate(imgs):
        lineup.paste(im, (i * w, 0))
    # resize down to standard product width 1200x1200 or 1400x1000
    target_w = 1200
    target_h = int(h * (target_w / lineup.width))
    lineup_res = lineup.resize((target_w, target_h), Image.Resampling.LANCZOS)
    out_p = os.path.join(PUB_PRODUCTS, out_name)
    lineup_res.save(out_p, "JPEG", quality=95)
    print(f"-> Created Lineup: {out_p}")

create_lineup(["kc-shaker-highvis-steel.jpg", "kc-shaker-steelcore-steel.jpg", "kc-shaker-jobsite-steel.jpg"], "kc-shaker-bottles-3-editions.jpg", "KrowN Construction Lineup")
create_lineup(["krown-shaker-obsidian-steel.jpg", "krown-shaker-smoke-tritan.jpg", "krown-shaker-brushed-steel.jpg"], "krown-shaker-bottles-3-editions.jpg", "KrowN Supply Co Lineup")

print("All shaker mockups successfully generated!")
