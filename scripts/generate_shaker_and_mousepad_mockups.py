import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
GAMING_DIR = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")
BRAIN_DIR = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7"

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

def create_dark_canvas(w=1024, h=1024, bg=(12, 13, 16), accent=(40, 20, 60)):
    canvas = Image.new("RGBA", (w, h), (bg[0], bg[1], bg[2], 255))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    cx, cy = w // 2, h // 2
    for r in range(int(w * 0.45), 0, -15):
        alpha = int(35 * (1.0 - r / (w * 0.45)))
        draw.ellipse([cx - r, cy - int(r * 0.8), cx + r, cy + int(r * 0.8)], fill=(accent[0], accent[1], accent[2], alpha))
    return Image.alpha_composite(canvas, glow)

# -----------------------------------------------------------------
# 1. SHAKER BOTTLES: 3 REALISTIC OPTIONS MOCKUP
# -----------------------------------------------------------------
def generate_shaker_options_mockup():
    print("Generating Shaker Bottles 3-Option Comparison Mockup...")
    canvas = create_dark_canvas(1024, 1024, bg=(10, 11, 14), accent=(30, 45, 35))
    draw = ImageDraw.Draw(canvas)
    cx = 512

    draw.text((cx, 55), "AXIOM ALLEGIANCE // OFFICIAL REFUEL GEAR", fill=(138, 43, 226), font=font_label, anchor="mm")
    draw.text((cx, 90), "PRO LOADOUT GAMING SHAKER COLLECTION", fill=(57, 255, 20), font=font_title, anchor="mm")
    draw.text((cx, 125), "LEAK-PROOF LOCK • ERGONOMIC DRINK SPOUT • STAINLESS STEEL WHISK BALL", fill=(160, 160, 175), font=font_micro, anchor="mm")

    # 3 Shakers Side by Side
    shakers = [
        ("OPTION 1: TOXIC LIME & PURPLE", "24oz Frosted Smoke Body\nNeon Toxic Green Flip Cap\nPurple Ergonomic Band", cx - 310, 210, "toxic_lime"),
        ("OPTION 2: STEALTH BLACKOUT", "24oz Matte Obsidian Body\nDark Charcoal Grip Band\nTonal Purple Accent & Glow", cx, 210, "stealth_black"),
        ("OPTION 3: PRO INSULATED STEEL", "26oz Kitchen-Grade Steel\nVacuum Insulated Double-Wall\nLaser-Etched Metallic Owl", cx + 310, 210, "stainless_steel")
    ]

    for title, subtitle, sx, sy, style in shakers:
        # Floor shadow
        shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.ellipse([sx - 110, sy + 510, sx + 110, sy + 560], fill=(0, 0, 0, 170))
        shadow = shadow.filter(ImageFilter.GaussianBlur(14))
        canvas = Image.alpha_composite(canvas, shadow)
        draw = ImageDraw.Draw(canvas)

        # Draw Shaker Silhouette
        bw = 140
        bh = 460
        by = sy + 60

        # Colors based on style
        if style == "toxic_lime":
            body_fill = (25, 28, 32, 230)
            lid_fill = (45, 200, 20)
            cap_fill = (57, 255, 20)
            band_fill = (138, 43, 226)
            outline_col = (57, 255, 20)
        elif style == "stealth_black":
            body_fill = (16, 17, 20, 250)
            lid_fill = (28, 28, 34)
            cap_fill = (138, 43, 226)
            band_fill = (22, 22, 26)
            outline_col = (110, 50, 160)
        else: # Stainless steel
            body_fill = (28, 30, 35, 255)
            lid_fill = (35, 38, 44)
            cap_fill = (57, 255, 20)
            band_fill = (20, 22, 26)
            outline_col = (200, 205, 215)

        # Shaker Body (Tapered)
        body_poly = [
            (sx - bw//2, by + 100),
            (sx + bw//2, by + 100),
            (sx + bw//2 - 15, by + bh),
            (sx - bw//2 + 15, by + bh)
        ]
        draw.polygon(body_poly, fill=body_fill, outline=(40, 42, 50))

        # Silicone Grip Band in Middle
        band_y = by + 170
        draw.polygon([
            (sx - bw//2 + 5, band_y),
            (sx + bw//2 - 5, band_y),
            (sx + bw//2 - 8, band_y + 80),
            (sx - bw//2 + 8, band_y + 80)
        ], fill=band_fill, outline=outline_col)

        # Shaker Screw-on Lid
        draw.rounded_rectangle([sx - bw//2 - 12, by + 40, sx + bw//2 + 12, by + 100], radius=8, fill=lid_fill, outline=(30, 30, 35))

        # Flip Cap and Carry Loop
        draw.rounded_rectangle([sx - 25, by - 5, sx + 25, by + 45], radius=6, fill=cap_fill)
        # Carry loop on right
        draw.ellipse([sx + 35, by + 15, sx + 75, by + 55], outline=band_fill, width=8)

        # Owl Crest on Lower Body
        if owl_img:
            owl_scale = 80 / max(owl_img.width, owl_img.height)
            owl_w = int(owl_img.width * owl_scale)
            owl_h = int(owl_img.height * owl_scale)
            owl_shk = owl_img.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
            canvas.paste(owl_shk, (sx - owl_w//2, by + 280), owl_shk)

        draw = ImageDraw.Draw(canvas)
        draw.text((sx, by + 375), "POWERED BY KROWN", fill=(160, 160, 175), font=get_font(["arialbd.ttf"], 10), anchor="mm")

        # Labels & Specs Below
        draw.text((sx, sy + 580), title, fill=(57, 255, 20), font=get_font(["impact.ttf", "arialbd.ttf"], 16), anchor="mm")
        y_off = sy + 610
        for line in subtitle.split("\n"):
            draw.text((sx, y_off), line, fill=(180, 180, 195), font=font_micro, anchor="mm")
            y_off += 20

    out_shk = os.path.join(PUB_PRODUCTS, "axiom-shaker-bottles-3-editions.jpg")
    canvas.convert("RGB").save(out_shk, "JPEG", quality=92, progressive=True)
    print(f"Saved: {out_shk} ({os.path.getsize(out_shk)//1024} KB)")

# -----------------------------------------------------------------
# 2. REALISTIC OWL DESK MAT (INCORPORATING DELIBERATE A-X-A FACE GEOMETRY)
# -----------------------------------------------------------------
def generate_realistic_axa_face_desk_mat():
    print("Generating Realistic Owl Desk Mat with deliberate A-X-A facial geometry...")
    canvas = create_dark_canvas(1024, 1024, bg=(8, 10, 13), accent=(40, 15, 65))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 512, 480

    # Draw 3D Desk Mat in Perspective on Battlestation Desk
    # Desk mat bounds: 880 x 440
    mw = 880
    mh = 440
    mx1 = cx - mw // 2
    mx2 = cx + mw // 2
    my1 = 200
    my2 = my1 + mh

    # Drop shadow
    shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([mx1 - 10, my1 + 10, mx2 + 10, my2 + 25], radius=16, fill=(0, 0, 0, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)
    draw = ImageDraw.Draw(canvas)

    # Base Desk Mat: Obsidian Black textured cloth
    draw.rounded_rectangle([mx1, my1, mx2, my2], radius=12, fill=(15, 16, 20), outline=(57, 255, 20), width=3)
    # Stitched border in electric toxic green
    draw.rounded_rectangle([mx1 + 3, my1 + 3, mx2 - 3, my2 - 3], radius=10, outline=(138, 43, 226), width=2)

    # Center: Realistic Owl artwork with deliberate A-X-A facial structure
    # Left eye/brow = A, Center beak/forehead bridge = X, Right eye/brow = A
    if owl_img:
        owl_scale = 320 / max(owl_img.width, owl_img.height)
        owl_w = int(owl_img.width * owl_scale)
        owl_h = int(owl_img.height * owl_scale)
        owl_mat = owl_img.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
        # Paste prominent in center
        canvas.paste(owl_mat, (cx - owl_w//2, my1 + (mh - owl_h)//2 - 15), owl_mat)

    draw = ImageDraw.Draw(canvas)

    # Stylized Team Typography across left side
    draw.text((mx1 + 50, my2 - 60), "Aχισм Aℓℓєgιαηcє", fill=(255, 255, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 28), anchor="lm")
    draw.text((mx1 + 50, my2 - 30), "PRO ESPORTS BATTLESTATION DESK MAT", fill=(57, 255, 20), font=get_font(["arialbd.ttf"], 12), anchor="lm")

    # Team Motto across right bottom border
    draw.text((mx2 - 50, my2 - 40), "“YOU CANNOT BE TRULY HUMBLE, UNLESS YOU TRULY BELIEVE THAT LIFE CAN AND WILL GO ON WITHOUT YOU”", fill=(175, 175, 190), font=get_font(["arial.ttf"], 9), anchor="rm")

    # Callout: 5 Custom Sizes Available
    draw.text((cx, 80), "AXIOM ALLEGIANCE // BATTLESTATION DESK MATS", fill=(138, 43, 226), font=font_label, anchor="mm")
    draw.text((cx, 120), "5 CUSTOM ESPORTS SIZES AVAILABLE", fill=(57, 255, 20), font=font_title, anchor="mm")

    # Size Badges Pill Grid at Bottom
    sizes = [
        ("MEDIUM (M)", "14\" x 12\" (360x300mm)", "$19.99", cx - 340),
        ("LARGE (L)", "18\" x 16\" (450x400mm)", "$26.99", cx - 170),
        ("EXTENDED (XL)", "31.5\" x 12\" (800x300mm)", "$32.99", cx),
        ("PANORAMIC (2XL)", "35.4\" x 16\" (900x400mm)", "$39.99", cx + 170),
        ("COLOSSAL (3XL)", "47\" x 24\" (1200x600mm)", "$49.99", cx + 340),
    ]

    for s_name, s_dim, s_price, bx in sizes:
        draw.rounded_rectangle([bx - 75, 710, bx + 75, 830], radius=8, fill=(18, 20, 26), outline=(57, 255, 20), width=1)
        draw.text((bx, 735), s_name, fill=(57, 255, 20), font=get_font(["impact.ttf", "arialbd.ttf"], 14), anchor="mm")
        draw.text((bx, 765), s_dim, fill=(180, 180, 195), font=get_font(["arial.ttf"], 10), anchor="mm")
        draw.text((bx, 800), s_price, fill=(240, 240, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 18), anchor="mm")

    # Inset Callout about A-X-A Face Feathers
    draw.text((cx, 880), "AUTHENTIC A-X-A FACIAL GEOMETRY • ANTI-FRAY DUAL PURPLE/LIME STITCHED EDGES • NON-SLIP RUBBER", fill=(160, 160, 175), font=font_micro, anchor="mm")

    out_mat = os.path.join(PUB_PRODUCTS, "axiom-owl-realistic-axa-face-desk-mat.jpg")
    canvas.convert("RGB").save(out_mat, "JPEG", quality=92, progressive=True)
    print(f"Saved: {out_mat} ({os.path.getsize(out_mat)//1024} KB)")

if __name__ == "__main__":
    generate_shaker_options_mockup()
    generate_realistic_axa_face_desk_mat()
