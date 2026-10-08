import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUBLIC_BRANDING_C = os.path.join(BASE_DIR, "public", "images", "branding", "construction")
PUBLIC_BRANDING_G = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")

def create_studio_canvas(w=1000, h=1000, bg=(14, 17, 22), accent=(30, 25, 45)):
    canvas = Image.new("RGBA", (w, h), (bg[0], bg[1], bg[2], 255))
    spotlight = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(spotlight)
    cx, cy = w // 2, h // 2
    for r in range(int(w * 0.45), 0, -10):
        alpha = int(25 * (1.0 - r / (w * 0.45)))
        draw.ellipse([cx - r, cy - int(r * 0.9), cx + r, cy + int(r * 0.9)], fill=(accent[0], accent[1], accent[2], alpha))
    return Image.alpha_composite(canvas, spotlight)

def generate_crewneck_mockup():
    print("Generating KrowN Heritage Heavy Crewneck Sweatshirt Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(40, 32, 20))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 500, 480

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 300, cy + 340, cx + 300, cy + 420], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, shadow)

    # Crewneck Sweatshirt silhouette (Thick, heavy fleece, ribbed cuffs)
    poly = [
        (cx - 80, cy - 290),
        (cx + 80, cy - 290),
        (cx + 260, cy - 230),
        (cx + 410, cy - 20),
        (cx + 340, cy + 30),
        (cx + 250, cy - 90),
        (cx + 220, cy + 320),
        (cx - 220, cy + 320),
        (cx - 250, cy - 90),
        (cx - 340, cy + 30),
        (cx - 410, cy - 20),
        (cx - 260, cy - 230),
    ]
    draw = ImageDraw.Draw(canvas)
    draw.polygon(poly, fill=(28, 27, 31))

    # Ribbed collar
    draw.ellipse([cx - 85, cy - 305, cx + 85, cy - 270], outline=(42, 40, 46), width=7)
    draw.ellipse([cx - 80, cy - 305, cx + 80, cy - 280], fill=(18, 17, 20))

    # Ribbed bottom hem
    draw.rectangle([cx - 220, cy + 300, cx + 220, cy + 335], fill=(32, 30, 35), outline=(44, 42, 48), width=2)
    # Sleeve cuffs
    draw.rectangle([cx + 330, cy + 10, cx + 380, cy + 45], fill=(32, 30, 35))
    draw.rectangle([cx - 380, cy + 10, cx - 330, cy + 45], fill=(32, 30, 35))

    # Front Embroidered Gold Crown & "KROWN"
    draw.text((cx, cy - 70), "KROWN", fill=(212, 175, 55), anchor="mm")
    draw.text((cx, cy - 40), "SUPPLY CO. // HEAVY FLEECE", fill=(160, 140, 75), anchor="mm")

    kc_path = os.path.join(PUBLIC_BRANDING_C, "KC logo black and white.png")
    if os.path.exists(kc_path):
        kc = Image.open(kc_path).convert("RGBA")
        scale = 130 / max(kc.width, kc.height)
        kc_res = kc.resize((int(kc.width * scale), int(kc.height * scale)), Image.Resampling.LANCZOS)
        arr = np.array(kc_res)
        mask = arr[:, :, 3] > 30
        arr[mask, 0] = 225
        arr[mask, 1] = 185
        arr[mask, 2] = 75
        gold_crown = Image.fromarray(arr)
        canvas.paste(gold_crown, (cx - gold_crown.width // 2, cy + 20), gold_crown)

    draw.text((cx, cy + 190), "10 OZ LUXURY THREE-END COTTON FLEECE", fill=(100, 105, 115), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-supply-crewneck-sweatshirt.png")
    canvas.save(out_p, "PNG")
    print(f"Saved crewneck mockup: {out_p}")

def generate_dadhat_mockup():
    print("Generating KrowN Vintage Washed Cotton Dad Hat Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(40, 35, 20))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 500, 500

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 260, cy + 240, cx + 260, cy + 320], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, shadow)

    # Curved Brim / Visor
    draw = ImageDraw.Draw(canvas)
    draw.ellipse([cx - 250, cy + 60, cx + 250, cy + 240], fill=(22, 22, 25), outline=(40, 40, 44), width=2)
    # Brim stitch arcs
    for r_diff in [15, 30, 45]:
        draw.arc([cx - 240 + r_diff, cy + 70 + r_diff // 2, cx + 240 - r_diff, cy + 230 - r_diff // 2], start=20, end=160, fill=(38, 38, 42), width=2)

    # Unstructured Crown (relaxed low profile dome)
    draw.ellipse([cx - 200, cy - 200, cx + 200, cy + 120], fill=(26, 26, 30), outline=(42, 42, 48), width=2)
    # Center seam
    draw.line([(cx, cy - 200), (cx, cy + 100)], fill=(36, 36, 40), width=3)
    # Eyelets (breathable embroidered holes)
    draw.ellipse([cx - 80, cy - 100, cx - 66, cy - 86], outline=(50, 50, 55), width=2)
    draw.ellipse([cx + 66, cy - 100, cx + 80, cy - 86], outline=(50, 50, 55), width=2)

    # Top button
    draw.ellipse([cx - 16, cy - 212, cx + 16, cy - 188], fill=(20, 20, 22), outline=(45, 45, 50), width=2)

    # Front 3D Metallic Gold Embroidered Insignia
    kc_path = os.path.join(PUBLIC_BRANDING_C, "KC logo black and white.png")
    if os.path.exists(kc_path):
        kc = Image.open(kc_path).convert("RGBA")
        scale = 100 / max(kc.width, kc.height)
        kc_res = kc.resize((int(kc.width * scale), int(kc.height * scale)), Image.Resampling.LANCZOS)
        arr = np.array(kc_res)
        mask = arr[:, :, 3] > 30
        arr[mask, 0] = 225
        arr[mask, 1] = 185
        arr[mask, 2] = 75
        gold_kc = Image.fromarray(arr)
        canvas.paste(gold_kc, (cx - gold_kc.width // 2, cy - 60), gold_kc)

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-vintage-washed-dad-hat.png")
    canvas.save(out_p, "PNG")
    print(f"Saved dad hat mockup: {out_p}")

def generate_streetwear_shorts_mockup():
    print("Generating KrowN French Terry Streetwear Shorts Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(35, 30, 25))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 500, 500

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 260, cy + 300, cx + 260, cy + 370], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)

    # Elastic Ribbed Waistband with Gold Tips
    draw = ImageDraw.Draw(canvas)
    wb_y = cy - 220
    draw.rounded_rectangle([cx - 240, wb_y, cx + 240, wb_y + 60], radius=8, fill=(30, 29, 33), outline=(45, 43, 50), width=2)
    # Heavy cotton drawstrings
    draw.line([(cx - 20, wb_y + 35), (cx - 25, wb_y + 120)], fill=(210, 210, 215), width=6)
    draw.line([(cx + 20, wb_y + 35), (cx + 25, wb_y + 120)], fill=(210, 210, 215), width=6)
    # Gold aglets
    draw.rectangle([cx - 28, wb_y + 115, cx - 22, wb_y + 128], fill=(212, 175, 55))
    draw.rectangle([cx + 22, wb_y + 115, cx + 28, wb_y + 128], fill=(212, 175, 55))

    # Left & Right Legs (Heavy French Terry cotton)
    left_poly = [(cx - 240, wb_y + 55), (cx - 10, wb_y + 55), (cx - 15, cy + 120), (cx - 30, cy + 280), (cx - 260, cy + 280)]
    right_poly = [(cx + 10, wb_y + 55), (cx + 240, wb_y + 55), (cx + 260, cy + 280), (cx + 30, cy + 280), (cx + 15, cy + 120)]
    
    draw.polygon(left_poly, fill=(26, 25, 29))
    draw.polygon(right_poly, fill=(26, 25, 29))

    # Raw cut hem
    draw.line([(cx - 260, cy + 280), (cx - 30, cy + 280)], fill=(40, 38, 44), width=4)
    draw.line([(cx + 30, cy + 280), (cx + 260, cy + 280)], fill=(40, 38, 44), width=4)

    # Gold Embroidered Crown on Left Thigh
    kc_path = os.path.join(PUBLIC_BRANDING_C, "KC logo black and white.png")
    if os.path.exists(kc_path):
        kc = Image.open(kc_path).convert("RGBA")
        scale = 100 / max(kc.width, kc.height)
        kc_res = kc.resize((int(kc.width * scale), int(kc.height * scale)), Image.Resampling.LANCZOS)
        arr = np.array(kc_res)
        mask = arr[:, :, 3] > 30
        arr[mask, 0] = 225
        arr[mask, 1] = 185
        arr[mask, 2] = 75
        gold_kc = Image.fromarray(arr)
        canvas.paste(gold_kc, (cx - 190, cy + 120), gold_kc)

    draw.text((cx + 140, cy + 180), "WEAR THE KROWN", fill=(212, 175, 55), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-french-terry-streetwear-shorts.png")
    canvas.save(out_p, "PNG")
    print(f"Saved french terry shorts mockup: {out_p}")

def main():
    print("=== Generating Remaining Division Products ===")
    generate_crewneck_mockup()
    generate_dadhat_mockup()
    generate_streetwear_shorts_mockup()
    print("=== Done! ===")

if __name__ == "__main__":
    main()
