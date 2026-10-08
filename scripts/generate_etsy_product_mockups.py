import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUBLIC_BRANDING_C = os.path.join(BASE_DIR, "public", "images", "branding", "construction")
PUBLIC_BRANDING_G = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")

os.makedirs(PUBLIC_PRODUCTS, exist_ok=True)

def create_studio_canvas(w=1000, h=1000, bg=(14, 17, 22), accent=(30, 25, 45)):
    canvas = Image.new("RGBA", (w, h), (bg[0], bg[1], bg[2], 255))
    spotlight = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(spotlight)
    cx, cy = w // 2, h // 2
    for r in range(int(w * 0.45), 0, -10):
        alpha = int(25 * (1.0 - r / (w * 0.45)))
        draw.ellipse([cx - r, cy - int(r * 0.9), cx + r, cy + int(r * 0.9)], fill=(accent[0], accent[1], accent[2], alpha))
    return Image.alpha_composite(canvas, spotlight)

def generate_tumbler_mockup():
    print("Generating KrowN 20oz Jobsite Tumbler...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(45, 38, 20))
    draw = ImageDraw.Draw(canvas)
    
    # Draw 20oz stainless steel tumbler body (matte black taper)
    # Tapered cylinder
    top_w, bot_w = 340, 260
    h_tumbler = 640
    cx, top_y = 500, 180
    
    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 160, top_y + h_tumbler - 10, cx + 160, top_y + h_tumbler + 35], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    canvas = Image.alpha_composite(canvas, shadow)
    
    # Tumbler layers
    # Main body
    poly = [
        (cx - top_w // 2, top_y + 40),
        (cx + top_w // 2, top_y + 40),
        (cx + bot_w // 2, top_y + h_tumbler),
        (cx - bot_w // 2, top_y + h_tumbler)
    ]
    draw = ImageDraw.Draw(canvas)
    draw.polygon(poly, fill=(28, 30, 34))
    
    # Subtle matte cylindrical gradient/sheen
    for x_offset in range(-top_w // 2, top_w // 2, 8):
        factor = abs(x_offset) / (top_w / 2)
        sheen_poly = [
            (cx + x_offset, top_y + 40),
            (cx + x_offset + 8, top_y + 40),
            (cx + int(x_offset * (bot_w / top_w)) + 8, top_y + h_tumbler),
            (cx + int(x_offset * (bot_w / top_w)), top_y + h_tumbler)
        ]
        # Highlight along 35% left side
        if -80 < x_offset < -20:
            val = int(55 + 25 * (1.0 - abs(x_offset + 50) / 40.0))
            draw.polygon(sheen_poly, fill=(val, val + 2, val + 4))
        else:
            val = int(22 + 15 * (1.0 - factor))
            draw.polygon(sheen_poly, fill=(val, val + 1, val + 2))

    # Tumbler stainless steel rim & clear lid
    draw.ellipse([cx - top_w // 2, top_y + 20, cx + top_w // 2, top_y + 55], fill=(70, 75, 82), outline=(130, 135, 145), width=2)
    # Clear acrylic lid
    draw.ellipse([cx - top_w // 2 + 10, top_y + 5, cx + top_w // 2 - 10, top_y + 35], fill=(50, 58, 68), outline=(100, 115, 130), width=2)
    # Sip opening
    draw.rectangle([cx - 30, top_y + 12, cx + 30, top_y + 24], fill=(20, 22, 25))

    # Bottom steel base ring
    draw.ellipse([cx - bot_w // 2, top_y + h_tumbler - 18, cx + bot_w // 2, top_y + h_tumbler + 15], fill=(55, 60, 68), outline=(90, 95, 105), width=2)

    # Laser-Engraved Metallic Gold Logo on Front
    logo_path = os.path.join(PUBLIC_BRANDING_C, "KrownConstruction PNG white.PNG")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_w = 210
        scale = logo_w / logo.width
        logo_h = int(logo.height * scale)
        logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        
        # Colorize logo to metallic gold (#D4AF37 / #E5C158)
        arr = np.array(logo_resized)
        mask = arr[:, :, 3] > 30
        arr[mask, 0] = 225
        arr[mask, 1] = 185
        arr[mask, 2] = 75
        gold_logo = Image.fromarray(arr)
        
        canvas.paste(gold_logo, (cx - logo_w // 2, top_y + 230), gold_logo)

    # Inscribe "BUILT TO REIGN" below logo
    draw.text((cx, top_y + 460), "BUILT TO REIGN", fill=(212, 175, 55), anchor="mm")
    draw.text((cx, top_y + 485), "20 OZ VACUUM INSULATED • STAINLESS STEEL", fill=(120, 125, 135), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-construction-jobsite-tumbler.png")
    canvas.save(out_p, "PNG")
    print(f"Saved tumbler mockup: {out_p}")

def generate_beanie_mockup():
    print("Generating KrowN Jobsite Cuffed Beanie...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(40, 35, 25))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 500, 500

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 240, cy + 260, cx + 240, cy + 340], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, shadow)

    # Ribbed Knit Crown (Dome)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse([cx - 220, cy - 250, cx + 220, cy + 120], fill=(35, 37, 42))
    
    # Knit texture ribs (vertical lines)
    for x in range(cx - 200, cx + 200, 8):
        rib_alpha = 15 if (x // 8) % 2 == 0 else 30
        draw.line([(x, cy - 180), (x, cy + 100)], fill=(rib_alpha + 25, rib_alpha + 25, rib_alpha + 30), width=3)

    # Folded Beanie Cuff
    cuff_y = cy + 40
    draw.rounded_rectangle([cx - 235, cuff_y, cx + 235, cuff_y + 190], radius=18, fill=(30, 32, 36), outline=(45, 48, 54), width=2)
    # Cuff ribbing
    for x in range(cx - 225, cx + 225, 7):
        shade = 42 if (x // 7) % 2 == 0 else 24
        draw.line([(x, cuff_y + 4), (x, cuff_y + 186)], fill=(shade, shade + 2, shade + 4), width=3)

    # Center Embroidered Laser Patch (Faux-leather / Gold thread patch)
    patch_w, patch_h = 160, 95
    patch_x = cx - patch_w // 2
    patch_y = cuff_y + 45
    draw.rounded_rectangle([patch_x, patch_y, patch_x + patch_w, patch_y + patch_h], radius=10, fill=(20, 20, 22), outline=(212, 175, 55), width=2)
    # Stitch line
    draw.rounded_rectangle([patch_x + 4, patch_y + 4, patch_x + patch_w - 4, patch_y + patch_h - 4], radius=8, outline=(160, 130, 40), width=1)

    # KC Logo on patch
    kc_path = os.path.join(PUBLIC_BRANDING_C, "KC logo black and white.png")
    if os.path.exists(kc_path):
        kc = Image.open(kc_path).convert("RGBA")
        scale = 75 / max(kc.width, kc.height)
        kc_res = kc.resize((int(kc.width * scale), int(kc.height * scale)), Image.Resampling.LANCZOS)
        arr = np.array(kc_res)
        mask = arr[:, :, 3] > 30
        arr[mask, 0] = 225
        arr[mask, 1] = 185
        arr[mask, 2] = 75
        gold_kc = Image.fromarray(arr)
        canvas.paste(gold_kc, (cx - gold_kc.width // 2, patch_y + 10), gold_kc)

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-construction-cuffed-beanie.png")
    canvas.save(out_p, "PNG")
    print(f"Saved beanie mockup: {out_p}")

def generate_hard_hat_sticker_pack():
    print("Generating KrowN Hardhat Sticker Pack Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(35, 45, 30))
    draw = ImageDraw.Draw(canvas)

    # Header / Pack Label
    draw.text((500, 80), "KROWN TRADESMAN DECAL PACK", fill=(212, 175, 55), anchor="mm")
    draw.text((500, 115), "HEAVYWEIGHT 6 MIL WEATHERPROOF & SOLVENT-PROOF VINYL", fill=(148, 163, 184), anchor="mm")

    # Display 5 dynamic overlapping die-cut stickers with drop shadows
    sticker_configs = [
        # (Image path, pos_x, pos_y, angle, size)
        (os.path.join(PUBLIC_BRANDING_C, "KC logo black and white.png"), 280, 320, -8, 240),
        (os.path.join(PUBLIC_BRANDING_C, "Krown Construction.png"), 700, 340, 10, 260),
        (os.path.join(PUBLIC_BRANDING_C, "Krown ConstructionPNG Black.PNG"), 480, 520, 0, 320),
        (os.path.join(PUBLIC_BRANDING_C, "KC.jpg"), 290, 720, 6, 230),
        (os.path.join(PUBLIC_BRANDING_C, "KrownConstruction PNG white.PNG"), 710, 720, -5, 240)
    ]

    for p, sx, sy, ang, sz in sticker_configs:
        if os.path.exists(p):
            stk = Image.open(p).convert("RGBA")
            scale = sz / max(stk.width, stk.height)
            stk_w = int(stk.width * scale)
            stk_h = int(stk.height * scale)
            stk_res = stk.resize((stk_w, stk_h), Image.Resampling.LANCZOS)

            # Die-cut white border
            pad = 24
            bordered = Image.new("RGBA", (stk_w + pad, stk_h + pad), (0, 0, 0, 0))
            # Create border mask on matching canvas
            stk_alpha = Image.new("L", (stk_w + pad, stk_h + pad), 0)
            raw_alpha = stk_res.split()[-1] if len(stk_res.split()) == 4 else Image.new("L", (stk_w, stk_h), 255)
            stk_alpha.paste(raw_alpha, (pad // 2, pad // 2))
            
            mask_thick = stk_alpha.filter(ImageFilter.MaxFilter(9))
            b_white = Image.new("RGBA", (stk_w + pad, stk_h + pad), (245, 245, 248, 255))
            bordered.paste(b_white, (0, 0), mask_thick)
            bordered.paste(stk_res, (pad // 2, pad // 2), stk_res)

            # Rotate
            rotated = bordered.rotate(ang, expand=True, resample=Image.Resampling.BICUBIC)

            # Drop shadow
            sh = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
            sh_mask = Image.fromarray((np.array(rotated)[:, :, 3] > 10).astype(np.uint8) * 130)
            sh_paste = Image.new("RGBA", rotated.size, (0, 0, 0, 255))
            sh.paste(sh_paste, (0, 0), sh_mask)
            sh = sh.filter(ImageFilter.GaussianBlur(10))

            canvas.paste(sh, (sx - rotated.width // 2, sy - rotated.height // 2 + 12), sh)
            canvas.paste(rotated, (sx - rotated.width // 2, sy - rotated.height // 2), rotated)

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-construction-stickers-pack.png")
    canvas.save(out_p, "PNG")
    print(f"Saved sticker pack mockup: {out_p}")

def generate_axiom_mug_mockup():
    print("Generating Axiom Owl Two-Tone Gaming Mug Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(50, 20, 65))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 480, 520

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 220, cy + 220, cx + 220, cy + 310], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)

    # Mug Handle (Purple / Obsidian with Lime inner rim)
    handle_x = cx + 200
    h_outer = [handle_x - 30, cy - 140, handle_x + 130, cy + 140]
    draw = ImageDraw.Draw(canvas)
    draw.ellipse(h_outer, fill=(28, 22, 38), outline=(50, 40, 65), width=3)
    # Inner cutout of handle
    draw.ellipse([handle_x + 5, cy - 85, handle_x + 85, cy + 85], fill=(14, 17, 22), outline=(57, 255, 20), width=2)

    # Mug Body (Cylinder, 15oz)
    mug_w, mug_h = 390, 420
    draw.rounded_rectangle([cx - mug_w // 2, cy - mug_h // 2, cx + mug_w // 2, cy + mug_h // 2], radius=16, fill=(24, 25, 29), outline=(40, 42, 48), width=2)
    # Cylindrical lighting on mug
    for x in range(cx - mug_w // 2, cx + mug_w // 2, 8):
        offset = x - (cx - mug_w // 2)
        if 40 < offset < 100:
            draw.line([(x, cy - mug_h // 2 + 5), (x, cy + mug_h // 2 - 5)], fill=(48, 50, 58), width=4)

    # Mug Top Rim (Two-Tone: Electric Lime / Royal Purple Interior)
    draw.ellipse([cx - mug_w // 2, cy - mug_h // 2 - 30, cx + mug_w // 2, cy - mug_h // 2 + 30], fill=(18, 14, 26), outline=(57, 255, 20), width=4)
    # Inner cavity reflection
    draw.ellipse([cx - mug_w // 2 + 8, cy - mug_h // 2 - 24, cx + mug_w // 2 - 8, cy - mug_h // 2 + 24], fill=(25, 18, 35))

    # Mug Graphic: Axiom Owl Crest + Motto
    owl_p = os.path.join(PUBLIC_BRANDING_G, "axiom-owl-mascot.png")
    if os.path.exists(owl_p):
        owl = Image.open(owl_p).convert("RGBA")
        scale = 220 / max(owl.width, owl.height)
        owl_res = owl.resize((int(owl.width * scale), int(owl.height * scale)), Image.Resampling.LANCZOS)
        canvas.paste(owl_res, (cx - owl_res.width // 2 - 20, cy - 90), owl_res)

    draw.text((cx - 20, cy + 95), "AXIOM ALLEGIANCE", fill=(168, 85, 247), anchor="mm")
    draw.text((cx - 20, cy + 120), "PLAY TO REIGN • POWERED BY KROWN", fill=(57, 255, 20), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "axiom-owl-gamer-mug-15oz.png")
    canvas.save(out_p, "PNG")
    print(f"Saved mug mockup: {out_p}")

def generate_cc1717_tee_mockup():
    print("Generating Comfort Colors 1717 Heavyweight Vintage Tee Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(30, 25, 35))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 500, 500

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 300, cy + 340, cx + 300, cy + 420], fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, shadow)

    # Boxy Relaxed Vintage Tee Silhouette (Pepper / Washed Vintage Black)
    tee_poly = [
        # Neckline
        (cx - 90, cy - 320),
        (cx + 90, cy - 320),
        # Right shoulder
        (cx + 280, cy - 250),
        # Right sleeve
        (cx + 380, cy - 100),
        (cx + 300, cy - 40),
        (cx + 250, cy - 130),
        # Right torso
        (cx + 230, cy + 330),
        # Bottom hem
        (cx - 230, cy + 330),
        # Left torso
        (cx - 250, cy - 130),
        # Left sleeve
        (cx - 300, cy - 40),
        (cx - 380, cy - 100),
        # Left shoulder
        (cx - 280, cy - 250),
    ]
    draw = ImageDraw.Draw(canvas)
    # Garment-dyed pepper black (#242327)
    draw.polygon(tee_poly, fill=(36, 35, 39))

    # Ribbed collar
    draw.ellipse([cx - 95, cy - 335, cx + 95, cy - 295], outline=(48, 47, 52), width=6)
    draw.ellipse([cx - 90, cy - 335, cx + 90, cy - 305], fill=(22, 21, 24))

    # Subtle fabric fold shading
    for y in range(cy - 200, cy + 280, 50):
        draw.line([(cx - 180, y), (cx - 70, y + 25)], fill=(30, 29, 33), width=4)
        draw.line([(cx + 80, y + 10), (cx + 190, y + 35)], fill=(30, 29, 33), width=4)

    # Distressed Gold Chest Graphic: "WEAR THE KROWN" + Insignia
    draw.text((cx, cy - 80), "WEAR THE KROWN", fill=(212, 175, 55), anchor="mm")
    draw.text((cx, cy - 50), "SUPPLY CO. // EST. 2026", fill=(160, 140, 75), anchor="mm")
    
    # Crown logo
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
        canvas.paste(gold_crown, (cx - gold_crown.width // 2, cy + 10), gold_crown)

    draw.text((cx, cy + 170), "AUTHENTIC COMFORT COLORS 1717", fill=(100, 105, 115), anchor="mm")
    draw.text((cx, cy + 195), "6.1 OZ 100% RING-SPUN VINTAGE GARMENT-DYED COTTON", fill=(80, 85, 95), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "krown-supply-comfort-colors-1717-tee.png")
    canvas.save(out_p, "PNG")
    print(f"Saved CC1717 tee mockup: {out_p}")

def generate_mesh_shorts_mockup():
    print("Generating Axiom Allegiance Gaming Mesh Shorts Mockup...")
    canvas = create_studio_canvas(1000, 1000, bg=(14, 17, 22), accent=(45, 20, 55))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 500, 500

    # Shadow
    shadow = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([cx - 260, cy + 300, cx + 260, cy + 370], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)

    # Elastic Ribbed Waistband with Lime Drawstrings
    draw = ImageDraw.Draw(canvas)
    wb_y = cy - 220
    draw.rounded_rectangle([cx - 240, wb_y, cx + 240, wb_y + 60], radius=8, fill=(28, 22, 38), outline=(57, 255, 20), width=2)
    # Drawstring aglets
    draw.line([(cx - 20, wb_y + 35), (cx - 30, wb_y + 110)], fill=(57, 255, 20), width=5)
    draw.line([(cx + 20, wb_y + 35), (cx + 30, wb_y + 110)], fill=(57, 255, 20), width=5)
    # Metallic aglet tips
    draw.rectangle([cx - 33, wb_y + 105, cx - 27, wb_y + 118], fill=(212, 175, 55))
    draw.rectangle([cx + 27, wb_y + 105, cx + 33, wb_y + 118], fill=(212, 175, 55))

    # Left & Right Legs
    # Left leg poly
    left_poly = [(cx - 240, wb_y + 55), (cx - 10, wb_y + 55), (cx - 15, cy + 120), (cx - 30, cy + 280), (cx - 260, cy + 280)]
    right_poly = [(cx + 10, wb_y + 55), (cx + 240, wb_y + 55), (cx + 260, cy + 280), (cx + 30, cy + 280), (cx + 15, cy + 120)]
    
    draw.polygon(left_poly, fill=(24, 18, 32))
    draw.polygon(right_poly, fill=(24, 18, 32))

    # Lime side piping on outer seams
    draw.line([(cx - 240, wb_y + 55), (cx - 260, cy + 280)], fill=(57, 255, 20), width=6)
    draw.line([(cx + 240, wb_y + 55), (cx + 260, cy + 280)], fill=(57, 255, 20), width=6)

    # Mesh pinhole texture
    for y in range(wb_y + 70, cy + 270, 16):
        for x in range(cx - 240, cx + 240, 16):
            if (x < cx - 40 or x > cx + 40):
                draw.point((x, y), fill=(35, 26, 48))

    # Axiom Owl Crest on Left Leg
    owl_p = os.path.join(PUBLIC_BRANDING_G, "axiom-owl-mascot.png")
    if os.path.exists(owl_p):
        owl = Image.open(owl_p).convert("RGBA")
        scale = 140 / max(owl.width, owl.height)
        owl_res = owl.resize((int(owl.width * scale), int(owl.height * scale)), Image.Resampling.LANCZOS)
        canvas.paste(owl_res, (cx - 210, cy + 90), owl_res)

    # "AXIOM" vertical text on Right Leg
    draw.text((cx + 140, cy + 140), "AXIOM", fill=(168, 85, 247), anchor="mm")
    draw.text((cx + 140, cy + 180), "ALLEGIANCE", fill=(57, 255, 20), anchor="mm")

    out_p = os.path.join(PUBLIC_PRODUCTS, "axiom-allegiance-gaming-mesh-shorts.png")
    canvas.save(out_p, "PNG")
    print(f"Saved shorts mockup: {out_p}")

def main():
    print("=== Generating High-Converting Etsy & Printify Mockups ===")
    generate_tumbler_mockup()
    generate_beanie_mockup()
    generate_hard_hat_sticker_pack()
    generate_axiom_mug_mockup()
    generate_cc1717_tee_mockup()
    generate_mesh_shorts_mockup()
    print("=== All New Mockups Successfully Generated! ===")

if __name__ == "__main__":
    main()
