import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUBLIC_BRANDING_C = os.path.join(BASE_DIR, "public", "images", "branding", "construction")
PUBLIC_BRANDING_G = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")

def create_studio_canvas(w=1000, h=1000, bg=(14, 17, 22), accent=(35, 30, 25)):
    canvas = Image.new("RGBA", (w, h), (bg[0], bg[1], bg[2], 255))
    spotlight = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(spotlight)
    cx, cy = w // 2, h // 2
    for r in range(int(w * 0.45), 0, -10):
        alpha = int(25 * (1.0 - r / (w * 0.45)))
        draw.ellipse([cx - r, cy - int(r * 0.9), cx + r, cy + int(r * 0.9)], fill=(accent[0], accent[1], accent[2], alpha))
    return Image.alpha_composite(canvas, spotlight)

# 1. BUILT TO REIGN: Tan / Brown Richardson 112 with Genuine Stitched Leather Patch
def generate_tan_leather_patch_r112():
    print("Generating Richardson 112 Tan / Rustic Leather Patch Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(16, 18, 22), accent=(50, 40, 25))
    cx, cy = 500, 520

    # Contact shadow on workbench
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 280, cy + 220, cx + 280, cy + 310], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, shadow)

    draw = ImageDraw.Draw(canvas)

    # Dark Brown / Espresso Breathable Mesh Back panels
    draw.ellipse([cx - 240, cy - 200, cx + 240, cy + 120], fill=(32, 26, 22), outline=(48, 38, 32), width=2)
    # Mesh texture grid
    for y in range(cy - 180, cy + 100, 8):
        for x in range(cx - 220, cx + 220, 8):
            if (x < cx - 120 or x > cx + 120 or y < cy - 80):
                draw.point((x, y), fill=(18, 14, 12))

    # Khaki / Tan Cotton-Poly Front Crown Panels (Structured Mid-Profile)
    # Distinct Richardson 112 structured front
    front_poly = [
        (cx - 170, cy - 180),
        (cx + 170, cy - 180),
        (cx + 220, cy + 70),
        (cx - 220, cy + 70)
    ]
    draw.polygon(front_poly, fill=(215, 202, 178)) # Authentic Richardson Khaki
    # Subtle panel seam down center
    draw.line([(cx, cy - 180), (cx, cy + 70)], fill=(180, 168, 145), width=3)
    # Side panel seams
    draw.line([(cx - 85, cy - 180), (cx - 120, cy + 70)], fill=(190, 178, 155), width=2)
    draw.line([(cx + 85, cy - 180), (cx + 120, cy + 70)], fill=(190, 178, 155), width=2)

    # Pre-Curved Khaki Visor
    draw.ellipse([cx - 270, cy + 50, cx + 270, cy + 240], fill=(198, 185, 160), outline=(165, 152, 130), width=2)
    # Visor rows of contrast stitching
    for diff in [16, 32, 48, 64]:
        draw.arc([cx - 260 + diff, cy + 60 + diff // 2, cx + 260 - diff, cy + 230 - diff // 2], start=20, end=160, fill=(150, 138, 118), width=2)

    # Top eyelets and khaki button
    draw.ellipse([cx - 65, cy - 100, cx - 53, cy - 88], outline=(150, 138, 118), width=2)
    draw.ellipse([cx + 53, cy - 100, cx + 65, cy - 88], outline=(150, 138, 118), width=2)
    draw.ellipse([cx - 16, cy - 192, cx + 16, cy - 168], fill=(195, 182, 158), outline=(150, 138, 118), width=2)

    # Centered Laser-Engraved Rustic Leather Patch (Cognac / Caramel Leather)
    patch_w, patch_h = 240, 150
    px, py = cx - patch_w // 2, cy - 85
    # Leather drop shadow
    patch_shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    ps_draw = ImageDraw.Draw(patch_shadow)
    ps_draw.rounded_rectangle([px, py + 4, px + patch_w, py + patch_h + 4], radius=12, fill=(0, 0, 0, 120))
    patch_shadow = patch_shadow.filter(ImageFilter.GaussianBlur(6))
    canvas = Image.alpha_composite(canvas, patch_shadow)

    draw = ImageDraw.Draw(canvas)
    # Caramel/Cognac leather base
    draw.rounded_rectangle([px, py, px + patch_w, py + patch_h], radius=12, fill=(168, 102, 48), outline=(125, 72, 30), width=2)
    # Subtle leather grain highlight
    draw.rounded_rectangle([px + 3, py + 3, px + patch_w - 3, py + patch_h - 3], radius=10, outline=(195, 128, 68), width=1)
    
    # Perimeter Stitched Border (Thick industrial saddle thread)
    stitch_inset = 8
    draw.rounded_rectangle([px + stitch_inset, py + stitch_inset, px + patch_w - stitch_inset, py + patch_h - stitch_inset], radius=8, outline=(80, 45, 18), width=2)
    # Dashed thread stitches
    for x in range(px + stitch_inset + 6, px + patch_w - stitch_inset - 6, 8):
        draw.line([(x, py + stitch_inset), (x + 4, py + stitch_inset)], fill=(225, 205, 160), width=2)
        draw.line([(x, py + patch_h - stitch_inset), (x + 4, py + patch_h - stitch_inset)], fill=(225, 205, 160), width=2)
    for y in range(py + stitch_inset + 6, py + patch_h - stitch_inset - 6, 8):
        draw.line([(px + stitch_inset, y), (px + stitch_inset, y + 4)], fill=(225, 205, 160), width=2)
        draw.line([(px + patch_w - stitch_inset, y), (px + patch_w - stitch_inset, y + 4)], fill=(225, 205, 160), width=2)

    # Laser-Burned KrowN Construction Monogram Crest in Center
    kc_path = os.path.join(PUBLIC_BRANDING_C, "KC logo black and white.png")
    if os.path.exists(kc_path):
        kc = Image.open(kc_path).convert("RGBA")
        scale = 88 / max(kc.width, kc.height)
        kc_res = kc.resize((int(kc.width * scale), int(kc.height * scale)), Image.Resampling.LANCZOS)
        # Tint logo to dark burned-leather tone (#3D1E0B)
        arr = np.array(kc_res)
        mask = arr[:, :, 3] > 30
        arr[mask, 0] = 55
        arr[mask, 1] = 28
        arr[mask, 2] = 12
        burned_kc = Image.fromarray(arr)
        canvas.paste(burned_kc, (cx - burned_kc.width // 2, py + 16), burned_kc)

    # Laser-Engraved "BUILT TO REIGN" Text on Patch
    draw = ImageDraw.Draw(canvas)
    draw.text((cx, py + 116), "BUILT TO REIGN", fill=(55, 28, 12), anchor="mm")
    draw.text((cx, py + 132), "EST. 2026 // KROWN SUPPLY", fill=(95, 52, 25), anchor="mm")

    # Authentic Richardson 112 Visor Foil Sticker on left visor edge
    sticker_poly = [
        (cx - 190, cy + 120),
        (cx - 100, cy + 110),
        (cx - 110, cy + 155),
        (cx - 200, cy + 165)
    ]
    draw.polygon(sticker_poly, fill=(35, 35, 40), outline=(210, 210, 215), width=1)
    draw.text((cx - 150, cy + 136), "RICHARDSON 112", fill=(240, 240, 245), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-r112-leather-patch-tan.png")
    canvas.save(out_p, "PNG")
    print(f"Saved Tan Richardson 112 Leather Patch mockup: {out_p}")

# 2. DROP 001: The Original KrowN Black / 3D Royal Purple Embroidered Trucker
def generate_purple_puff_trucker():
    print("Generating KrowN Original Black / 3D Purple Puff Trucker Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(45, 20, 60))
    cx, cy = 500, 520

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 280, cy + 220, cx + 280, cy + 310], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, shadow)

    draw = ImageDraw.Draw(canvas)

    # Royal Purple Mesh Back
    draw.ellipse([cx - 240, cy - 200, cx + 240, cy + 120], fill=(42, 18, 65), outline=(65, 28, 98), width=2)
    for y in range(cy - 180, cy + 100, 8):
        for x in range(cx - 220, cx + 220, 8):
            if (x < cx - 120 or x > cx + 120 or y < cy - 80):
                draw.point((x, y), fill=(25, 10, 40))

    # Midnight Obsidian Black Front Panels
    front_poly = [
        (cx - 170, cy - 180),
        (cx + 170, cy - 180),
        (cx + 220, cy + 70),
        (cx - 220, cy + 70)
    ]
    draw.polygon(front_poly, fill=(22, 22, 25))
    draw.line([(cx, cy - 180), (cx, cy + 70)], fill=(35, 35, 40), width=3)

    # Curved Black Visor with Purple Underbill Accent
    draw.ellipse([cx - 270, cy + 50, cx + 270, cy + 240], fill=(18, 18, 20), outline=(35, 35, 40), width=2)
    for diff in [16, 32, 48, 64]:
        draw.arc([cx - 260 + diff, cy + 60 + diff // 2, cx + 260 - diff, cy + 230 - diff // 2], start=20, end=160, fill=(45, 20, 68), width=2)

    # 3D Raised Puff Embroidery: Royal Purple KrowN Emblem & Crown
    # We create high-contrast puff embroidery effect
    kc_path = os.path.join(PUBLIC_BRANDING_C, "KC logo black and white.png")
    if os.path.exists(kc_path):
        kc = Image.open(kc_path).convert("RGBA")
        scale = 135 / max(kc.width, kc.height)
        kc_res = kc.resize((int(kc.width * scale), int(kc.height * scale)), Image.Resampling.LANCZOS)
        
        # 3D puff drop shadow/bevel
        arr = np.array(kc_res)
        mask = arr[:, :, 3] > 30
        
        # Purple puff fill
        arr[mask, 0] = 168 # vibrant royal purple
        arr[mask, 1] = 85
        arr[mask, 2] = 247
        purple_kc = Image.fromarray(arr)

        # Puff shadow
        puff_sh = Image.new("RGBA", purple_kc.size, (0, 0, 0, 0))
        sh_m = Image.fromarray((mask.astype(np.uint8) * 160))
        sh_fill = Image.new("RGBA", purple_kc.size, (20, 5, 35, 255))
        puff_sh.paste(sh_fill, (0, 0), sh_m)
        puff_sh = puff_sh.filter(ImageFilter.GaussianBlur(5))

        canvas.paste(puff_sh, (cx - purple_kc.width // 2 + 3, cy - 90 + 5), puff_sh)
        canvas.paste(purple_kc, (cx - purple_kc.width // 2, cy - 90), purple_kc)

    # Metallic Silver / White Outline Stitching & "KROWN" Typography
    draw = ImageDraw.Draw(canvas)
    draw.text((cx, cy + 18), "KROWN", fill=(240, 240, 250), anchor="mm")
    draw.text((cx, cy + 38), "ORIGINALS // DROP 001", fill=(168, 85, 247), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-original-3d-puff-purple-trucker.png")
    canvas.save(out_p, "PNG")
    print(f"Saved 3D Purple Puff Trucker mockup: {out_p}")

def main():
    print("=== Generating Reference-Grade Benchmark Hat Mockups ===")
    generate_tan_leather_patch_r112()
    generate_purple_puff_trucker()
    print("=== Complete! ===")

if __name__ == "__main__":
    main()
