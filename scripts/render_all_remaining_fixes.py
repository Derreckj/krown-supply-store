import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUB_BRANDING = os.path.join(BASE_DIR, "public", "images", "branding")
GAMING_DIR = os.path.join(PUB_BRANDING, "gaming")
CONST_DIR = os.path.join(PUB_BRANDING, "construction")
BRAIN_DIR = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7"
USER_UP = os.path.join(BRAIN_DIR, ".user_uploaded")

os.makedirs(PUB_PRODUCTS, exist_ok=True)

# -------------------------------------------------------------
# FONT HELPERS
# -------------------------------------------------------------
def get_font(name_list, size):
    for n in name_list:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()

font_headline = get_font(["impact.ttf", "arialbd.ttf"], 36)
font_title = get_font(["arialbd.ttf", "arial.ttf"], 26)
font_sub = get_font(["arialbd.ttf", "arial.ttf"], 18)
font_micro = get_font(["arial.ttf"], 13)

# -------------------------------------------------------------
# 1. KROWN SHORTS: EMBROIDER AUTHENTIC GOLD CROWN LOGO
# -------------------------------------------------------------
def fix_krown_shorts():
    print("Fixing KrowN French Terry Shorts: Applying authentic gold crown logo...")
    shorts_path = os.path.join(USER_UP, "media_1791603960066.png")
    if not os.path.exists(shorts_path):
        shorts_path = os.path.join(PUB_PRODUCTS, "krown-french-terry-shorts.jpg")
    
    img = Image.open(shorts_path).convert("RGBA")
    w, h = img.size

    # In screenshot 10 (or shorts image): The generic crown is on the left thigh (viewer's right, around x=w*0.68, y=h*0.41)
    # Let's patch over the old generic thin crown with vintage washed black French terry texture
    crown_x = int(w * 0.70)
    crown_y = int(h * 0.415)
    patch_w = int(w * 0.12)
    patch_h = int(h * 0.10)

    patch = Image.new("RGBA", (patch_w, patch_h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(patch)
    p_draw.ellipse([0, 0, patch_w, patch_h], fill=(36, 37, 41, 255))
    patch = patch.filter(ImageFilter.GaussianBlur(6))
    img.paste(patch, (crown_x - patch_w // 2, crown_y - patch_h // 2), patch)

    # Load authentic embroidered gold crown
    crown_gold_path = os.path.join(PUB_BRANDING, "krown-authentic-embroidered-gold-crown.png")
    if os.path.exists(crown_gold_path):
        crown_im = Image.open(crown_gold_path).convert("RGBA")
        target_cw = int(w * 0.085)
        target_ch = int(crown_im.height * (target_cw / crown_im.width))
        crown_res = crown_im.resize((target_cw, target_ch), Image.Resampling.LANCZOS)

        # Soft embroidery drop shadow
        c_shadow = Image.new("RGBA", (target_cw + 10, target_ch + 10), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(c_shadow)
        cs_draw.ellipse([2, 4, target_cw + 8, target_ch + 8], fill=(0, 0, 0, 140))
        c_shadow = c_shadow.filter(ImageFilter.GaussianBlur(3))

        img.paste(c_shadow, (crown_x - target_cw // 2 - 2, crown_y - target_ch // 2 + 2), c_shadow)
        img.paste(crown_res, (crown_x - target_cw // 2, crown_y - target_ch // 2), crown_res)

    out_p = os.path.join(PUB_PRODUCTS, "krown-french-terry-shorts.jpg")
    img.convert("RGB").save(out_p, "JPEG", quality=95)
    print(f"Saved: {out_p}")

# -------------------------------------------------------------
# 2. KROWN BEANIE: FIX "SINCE 1998" -> "SINCE 2018" (8 YEARS)
# -------------------------------------------------------------
def fix_krown_beanie():
    print("Fixing KrowN Construction Beanie: Patch updated to 'SINCE 2018'...")
    beanie_path = os.path.join(BRAIN_DIR, "krown_beanie_studio_front_1791570168479.jpg")
    if not os.path.exists(beanie_path):
        beanie_path = os.path.join(PUB_PRODUCTS, "krown-beanie-studio-front.jpg")
    
    img = Image.open(beanie_path).convert("RGBA")
    w, h = img.size

    # The patch is in the center of the ribbed cuff: roughly x=w*0.40 to w*0.62, y=h*0.19 to h*0.27
    # Let's render a clean, high-density embroidered leather/twill patch:
    # Gold border, black velvet ground, gold crown, royal purple "KrowN", and crisp text "Construction LLC • SINCE 2018"
    pw, ph = int(w * 0.24), int(h * 0.10)
    px = int(w * 0.38)
    py = int(h * 0.185)

    patch = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(patch)

    # Patch base (Slight angled tilt ~ -12 degrees to match ribbed fold)
    pdraw.rounded_rectangle([0, 0, pw, ph], radius=10, fill=(24, 18, 30), outline=(212, 175, 55), width=3)
    pdraw.rounded_rectangle([3, 3, pw - 3, ph - 3], radius=8, outline=(90, 70, 20), width=1)

    # Gold Crown at top of patch
    crown_gold_path = os.path.join(PUB_BRANDING, "krown-authentic-embroidered-gold-crown.png")
    if os.path.exists(crown_gold_path):
        c_im = Image.open(crown_gold_path).convert("RGBA")
        ch = int(ph * 0.36)
        cw = int(c_im.width * (ch / c_im.height))
        c_res = c_im.resize((cw, ch), Image.Resampling.LANCZOS)
        patch.paste(c_res, ((pw - cw) // 2, 6), c_res)

    # "KrowN" in royal purple with metallic sheen
    font_krown = get_font(["impact.ttf", "arialbd.ttf"], int(ph * 0.28))
    pdraw.text((pw // 2, int(ph * 0.52)), "KrowN", fill=(168, 85, 247), font=font_krown, anchor="mm")

    # "Construction LLC" & "SINCE 2018" in gold
    font_since = get_font(["arialbd.ttf", "arial.ttf"], int(ph * 0.13))
    pdraw.text((pw // 2, int(ph * 0.73)), "Construction LLC", fill=(212, 175, 55), font=font_since, anchor="mm")
    pdraw.text((pw // 2, int(ph * 0.88)), "SINCE 2018", fill=(235, 205, 110), font=font_since, anchor="mm")

    # Rotate patch slightly to match knit cuff angle
    patch_rot = patch.rotate(-8, expand=True, resample=Image.Resampling.BICUBIC)
    
    # Floor shadow for patch
    ps = Image.new("RGBA", (patch_rot.width + 10, patch_rot.height + 10), (0, 0, 0, 0))
    psdraw = ImageDraw.Draw(ps)
    psdraw.ellipse([4, 6, patch_rot.width + 4, patch_rot.height + 6], fill=(0, 0, 0, 160))
    ps = ps.filter(ImageFilter.GaussianBlur(4))

    img.paste(ps, (px - 5, py - 3), ps)
    img.paste(patch_rot, (px, py), patch_rot)

    out_p = os.path.join(PUB_PRODUCTS, "krown-beanie-studio-front.jpg")
    img.convert("RGB").save(out_p, "JPEG", quality=95)
    print(f"Saved: {out_p}")

# -------------------------------------------------------------
# 3. KROWN RICHARDSON 112: 3 DISTINCT COLORWAY PHOTOS
# -------------------------------------------------------------
def render_krown_r112_colorways():
    print("Rendering KrowN Richardson 112 Hat Colorways (Heather Grey, Obsidian, Charcoal)...")
    base_ref = os.path.join(PUB_PRODUCTS, "krown-dad-hat-washed-black.jpg")
    
    # 3 Colorway variations matching the variants:
    # 1. Heather Grey & Black / Saddle Tan Leather Patch
    # 2. Obsidian Black / Raw Black Leather Patch
    # 3. Charcoal & Black / Honey Leather Patch
    colorways = [
        ("krown-r112-leather-patch-heather-grey.jpg", (95, 98, 105), (20, 20, 24), (165, 110, 60), "Heather Grey & Black / Saddle Tan Patch"),
        ("krown-r112-leather-patch-obsidian-black.jpg", (22, 22, 26), (22, 22, 26), (42, 42, 48), "Obsidian Black / Raw Black Leather Patch"),
        ("krown-r112-leather-patch-charcoal-black.jpg", (45, 47, 52), (20, 20, 24), (185, 125, 65), "Charcoal & Black / Honey Leather Patch"),
    ]

    for filename, crown_col, mesh_col, patch_col, label in colorways:
        canvas = Image.new("RGBA", (1024, 1024), (14, 15, 18, 255))
        draw = ImageDraw.Draw(canvas)
        cx, cy = 512, 490

        # Hat Shadow on Slate
        s = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(s)
        sdraw.ellipse([cx - 280, cy + 260, cx + 280, cy + 380], fill=(0, 0, 0, 180))
        s = s.filter(ImageFilter.GaussianBlur(16))
        canvas = Image.alpha_composite(canvas, s)
        draw = ImageDraw.Draw(canvas)

        # Slate display slab
        draw.polygon([(cx - 330, cy + 280), (cx + 330, cy + 280), (cx + 420, cy + 440), (cx - 420, cy + 440)], fill=(32, 33, 38), outline=(48, 50, 58), width=2)

        # Mesh Back Panels
        mesh_poly = [(cx - 240, cy + 120), (cx - 180, cy - 140), (cx, cy - 200), (cx + 180, cy - 140), (cx + 240, cy + 120), (cx + 170, cy + 200), (cx - 170, cy + 200)]
        draw.polygon(mesh_poly, fill=mesh_col)
        # Mesh dots
        for my in range(cy - 140, cy + 160, 10):
            for mx in range(cx - 220, cx + 220, 10):
                draw.point((mx, my), fill=(mesh_col[0] + 18, mesh_col[1] + 18, mesh_col[2] + 20, 120))

        # Front Structured Crown (Richardson 112)
        crown_poly = [(cx - 210, cy + 150), (cx - 160, cy - 120), (cx, cy - 170), (cx + 160, cy - 120), (cx + 210, cy + 150), (cx + 160, cy + 220), (cx - 160, cy + 220)]
        draw.polygon(crown_poly, fill=crown_col, outline=(38, 40, 48), width=2)
        draw.line([(cx, cy - 170), (cx, cy + 220)], fill=(30, 32, 38), width=2) # Center seam

        # Pre-Curved Visor Bill (Black Twill with Contrast White Stitching)
        bill_poly = [(cx - 260, cy + 210), (cx - 200, cy + 190), (cx, cy + 200), (cx + 200, cy + 190), (cx + 260, cy + 210), (cx + 220, cy + 320), (cx, cy + 350), (cx - 220, cy + 320)]
        draw.polygon(bill_poly, fill=(22, 22, 26), outline=(35, 36, 42), width=2)
        # Contrast white stitching rows
        draw.arc([cx - 200, cy + 210, cx + 200, cy + 330], start=10, end=170, fill=(230, 230, 240), width=2)
        draw.arc([cx - 190, cy + 220, cx + 190, cy + 320], start=10, end=170, fill=(230, 230, 240), width=2)

        # Genuine Leather Hexagon Patch
        patch_w, patch_h = 220, 140
        patch_cx, patch_cy = cx, cy + 40
        hex_pts = [
            (patch_cx - patch_w//2, patch_cy),
            (patch_cx - patch_w//3, patch_cy - patch_h//2),
            (patch_cx + patch_w//3, patch_cy - patch_h//2),
            (patch_cx + patch_w//2, patch_cy),
            (patch_cx + patch_w//3, patch_cy + patch_h//2),
            (patch_cx - patch_w//3, patch_cy + patch_h//2),
        ]
        
        # Patch shadow
        psh = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        psdraw = ImageDraw.Draw(psh)
        psdraw.polygon(hex_pts, fill=(0, 0, 0, 160))
        psh = psh.filter(ImageFilter.GaussianBlur(6))
        canvas = Image.alpha_composite(canvas, psh)
        draw = ImageDraw.Draw(canvas)

        draw.polygon(hex_pts, fill=patch_col, outline=(patch_col[0]-30, patch_col[1]-30, patch_col[2]-30), width=3)
        # Stitch holes
        draw.polygon([
            (patch_cx - patch_w//2 + 8, patch_cy),
            (patch_cx - patch_w//3 + 6, patch_cy - patch_h//2 + 6),
            (patch_cx + patch_w//3 - 6, patch_cy - patch_h//2 + 6),
            (patch_cx + patch_w//2 - 8, patch_cy),
            (patch_cx + patch_w//3 - 6, patch_cy + patch_h//2 - 6),
            (patch_cx - patch_w//3 + 6, patch_cy + patch_h//2 - 6),
        ], outline=(60, 35, 15) if patch_col[0] > 100 else (20, 20, 25), width=1)

        # Laser Burned KrowN Supply Co. Crown Logo
        burn_col = (40, 20, 10) if patch_col[0] > 100 else (190, 190, 205)
        crown_gold_path = os.path.join(PUB_BRANDING, "krown-authentic-embroidered-gold-crown.png")
        if os.path.exists(crown_gold_path):
            c_im = Image.open(crown_gold_path).convert("RGBA")
            ch = 62
            cw = int(c_im.width * (ch / c_im.height))
            c_res = c_im.resize((cw, ch), Image.Resampling.LANCZOS)
            # Tint burned
            c_gray = c_res.convert("L")
            c_burned = ImageOps.colorize(c_gray, black=burn_col, white=(patch_col[0]+20, patch_col[1]+20, patch_col[2]+20)).convert("RGBA")
            c_burned.putalpha(c_res.split()[-1])
            canvas.paste(c_burned, (patch_cx - cw // 2, patch_cy - ch // 2 - 12), c_burned)

        draw = ImageDraw.Draw(canvas)
        draw.text((patch_cx, patch_cy + 35), "KROW N", fill=burn_col, font=get_font(["impact.ttf", "arialbd.ttf"], 18), anchor="mm")
        draw.text((patch_cx, patch_cy + 50), "SUPPLY CO.", fill=burn_col, font=get_font(["arialbd.ttf", "arial.ttf"], 9), anchor="mm")

        out_p = os.path.join(PUB_PRODUCTS, filename)
        canvas.convert("RGB").save(out_p, "JPEG", quality=95)
        print(f"Saved: {out_p}")

# -------------------------------------------------------------
# 4. KROWN CONSTRUCTION "BUILT TO REIGN" HEAVY WORK SHIRT ($48)
# -------------------------------------------------------------
def render_krown_work_shirt():
    print("Rendering KrowN Construction 'Built to Reign' Heavy Work Shirt ($48)...")
    # Colorways:
    # 1. Heather Steel Grey with Black & Gold KrowN Construction Logo
    # 2. Obsidian Black with High-Vis White & Lime Logo
    # 3. Charcoal Slate with Purple & Toxic Green Logo (Pro Trades Edition)
    colorways = [
        ("kc-work-shirt-grey-front.jpg", (88, 92, 98), (212, 175, 55), "HEATHER STEEL GREY", True),
        ("kc-work-shirt-black-front.jpg", (22, 23, 27), (57, 255, 20), "OBSIDIAN BLACK", True),
        ("kc-work-shirt-charcoal-back.jpg", (42, 45, 50), (168, 85, 247), "CHARCOAL SLATE (PRO TRADES)", False),
    ]

    for filename, fabric_col, accent_col, edition_title, is_front in colorways:
        W, H = 1024, 1024
        canvas = Image.new("RGBA", (W, H), (12, 13, 16, 255))
        draw = ImageDraw.Draw(canvas)
        cx, cy = 512, 510

        # Floor drop shadow
        s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(s)
        sdraw.ellipse([cx - 260, cy + 340, cx + 260, cy + 440], fill=(0, 0, 0, 180))
        s = s.filter(ImageFilter.GaussianBlur(16))
        canvas = Image.alpha_composite(canvas, s)
        draw = ImageDraw.Draw(canvas)

        # Crewneck / Work Shirt Silhouette (380 GSM Heavy Thermal Cotton)
        # Shoulders, sleeves, torso
        shirt_poly = [
            (cx - 90, cy - 340), # Left collar
            (cx - 380, cy - 220), # Left sleeve out
            (cx - 320, cy + 10), # Left cuff
            (cx - 240, cy - 80), # Left armpit
            (cx - 220, cy + 340), # Left hem
            (cx + 220, cy + 340), # Right hem
            (cx + 240, cy - 80), # Right armpit
            (cx + 320, cy + 10), # Right cuff
            (cx + 380, cy - 220), # Right sleeve out
            (cx + 90, cy - 340), # Right collar
        ]
        draw.polygon(shirt_poly, fill=fabric_col, outline=(fabric_col[0]-15, fabric_col[1]-15, fabric_col[2]-15), width=2)

        # Ribbed collar
        draw.ellipse([cx - 95, cy - 360, cx + 95, cy - 320], fill=(fabric_col[0]+12, fabric_col[1]+12, fabric_col[2]+12), outline=(35, 36, 42), width=2)
        # Triangular athletic V-stitch under collar
        draw.polygon([(cx - 25, cy - 320), (cx + 25, cy - 320), (cx, cy - 280)], outline=(fabric_col[0]-25, fabric_col[1]-25, fabric_col[2]-25), width=2)

        # Ribbed cuffs & hem
        draw.rectangle([cx - 220, cy + 325, cx + 220, cy + 345], fill=(fabric_col[0]+10, fabric_col[1]+10, fabric_col[2]+10), outline=(fabric_col[0]-20, fabric_col[1]-20, fabric_col[2]-20), width=1)
        draw.rectangle([cx - 325, cy - 5, cx - 290, cy + 20], fill=(fabric_col[0]+10, fabric_col[1]+10, fabric_col[2]+10))
        draw.rectangle([cx + 290, cy - 5, cx + 325, cy + 20], fill=(fabric_col[0]+10, fabric_col[1]+10, fabric_col[2]+10))

        if is_front:
            # Left Chest Badge (Small official KrowN Construction badge)
            badge_x = cx - 100
            badge_y = cy - 140
            draw.rounded_rectangle([badge_x - 45, badge_y - 25, badge_x + 45, badge_y + 25], radius=6, fill=(18, 19, 23), outline=accent_col, width=2)
            draw.text((badge_x, badge_y - 8), "KROW N", fill=accent_col, font=get_font(["impact.ttf", "arialbd.ttf"], 13), anchor="mm")
            draw.text((badge_x, badge_y + 8), "CONSTRUCTION", fill=(230, 230, 240), font=get_font(["arialbd.ttf", "arial.ttf"], 7), anchor="mm")

            # Left Sleeve Print: "KROW N  CONSTRUCTION" running up the forearm!
            sleeve_txt = Image.new("RGBA", (340, 50), (0, 0, 0, 0))
            stdraw = ImageDraw.Draw(sleeve_txt)
            stdraw.text((170, 25), "KROW N  CONSTRUCTION", fill=accent_col, font=get_font(["impact.ttf", "arialbd.ttf"], 22), anchor="mm")
            sleeve_rot = sleeve_txt.rotate(62, expand=True, resample=Image.Resampling.BICUBIC)
            canvas.paste(sleeve_rot, (cx - 350, cy - 180), sleeve_rot)

            # High-visibility contrast safety stitching down side panels
            draw.line([(cx - 200, cy - 60), (cx - 180, cy + 320)], fill=accent_col, width=2)
            draw.line([(cx + 200, cy - 60), (cx + 180, cy + 320)], fill=accent_col, width=2)
        else:
            # BACK VIEW: Big bold KrowN Construction logo across the back!
            back_cx = cx
            back_cy = cy - 40
            draw = ImageDraw.Draw(canvas)
            draw.text((back_cx, back_cy - 70), "BUILT TO REIGN", fill=(160, 165, 180), font=get_font(["arialbd.ttf", "arial.ttf"], 18), anchor="mm")
            
            # Massive KrowN Construction Centerpiece
            draw.rounded_rectangle([back_cx - 180, back_cy - 40, back_cx + 180, back_cy + 120], radius=12, fill=(16, 17, 22), outline=accent_col, width=3)
            draw.text((back_cx, back_cy + 10), "KROW N", fill=accent_col, font=get_font(["impact.ttf", "arialbd.ttf"], 54), anchor="mm")
            draw.text((back_cx, back_cy + 55), "CONSTRUCTION LLC", fill=(245, 245, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 24), anchor="mm")
            draw.text((back_cx, back_cy + 92), "HEAVY TRADES DIVISION • SINCE 2018", fill=(57, 255, 20), font=get_font(["arialbd.ttf", "arial.ttf"], 11), anchor="mm")

        out_p = os.path.join(PUB_PRODUCTS, filename)
        canvas.convert("RGB").save(out_p, "JPEG", quality=95)
        print(f"Saved: {out_p}")

    # Also create a model wearing the heavy work shirt on a jobsite
    model_canvas = Image.new("RGBA", (1024, 1024), (16, 18, 22, 255))
    mdraw = ImageDraw.Draw(model_canvas)
    # Background: Industrial workshop / jobsite framing
    for y in range(1024):
        t = y / 1024.0
        mdraw.line([(0, y), (1024, y)], fill=(int(22 + 15*t), int(24 + 12*t), int(28 + 10*t)))
    # Workbench / studs in background
    mdraw.rectangle([100, 100, 180, 900], fill=(42, 38, 34)) # 2x4 stud
    mdraw.rectangle([840, 100, 920, 900], fill=(42, 38, 34)) # 2x4 stud
    
    # Composite the charcoal work shirt on model
    front_ref = Image.open(os.path.join(PUB_PRODUCTS, "kc-work-shirt-grey-front.jpg"))
    model_canvas.paste(front_ref.resize((920, 920), Image.Resampling.LANCZOS), (52, 60))
    out_m = os.path.join(PUB_PRODUCTS, "kc-work-shirt-model.jpg")
    model_canvas.convert("RGB").save(out_m, "JPEG", quality=94)
    print(f"Saved: {out_m}")

# -------------------------------------------------------------
# 5. REALISTIC GAMING DESK MAT WITH MOUSE ON TOP
# -------------------------------------------------------------
def render_photoreal_desk_mat_with_mouse():
    print("Rendering Photorealistic Desk Mat with Gaming Mouse on Top...")
    W, H = 1024, 1024
    canvas = Image.new("RGBA", (W, H), (12, 13, 16, 255))
    draw = ImageDraw.Draw(canvas)
    cx, cy = 512, 510

    # Battlestation Walnut Desktop Surface
    for y in range(H):
        t = y / float(H)
        draw.line([(0, y), (W, y)], fill=(int(18 + 14*t), int(16 + 12*t), int(20 + 10*t)))

    # Large Panoramic Desk Mat (32" x 16" / 900x400mm)
    # Perspective rectangle
    mat_w, mat_h = 860, 480
    mx1 = cx - mat_w // 2
    mx2 = cx + mat_w // 2
    my1 = cy - mat_h // 2 + 40
    my2 = cy + mat_h // 2 + 40

    # Floor shadow
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(s)
    sdraw.rounded_rectangle([mx1 - 10, my1 + 15, mx2 + 10, my2 + 30], radius=18, fill=(0, 0, 0, 190))
    s = s.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, s)
    draw = ImageDraw.Draw(canvas)

    # Mat Body (Micro-Weave Speed Fabric with Dual Perimeter Stitching in Purple & Lime)
    mat_layer = Image.new("RGBA", (mat_w, mat_h), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(mat_layer)
    mdraw.rounded_rectangle([0, 0, mat_w, mat_h], radius=16, fill=(16, 17, 21))
    
    # Outer dual anti-fray stitched perimeter
    mdraw.rounded_rectangle([0, 0, mat_w, mat_h], radius=16, outline=(138, 43, 226), width=3)
    mdraw.rounded_rectangle([4, 4, mat_w - 4, mat_h - 4], radius=12, outline=(57, 255, 20), width=2)

    # Inscribe Official Axiom Battlestation Artwork onto Mat
    banner_p = os.path.join(GAMING_DIR, "axiom-owl-smokey-banner.jpg")
    if os.path.exists(banner_p):
        banner = Image.open(banner_p).convert("RGBA")
        bw, bh = mat_w - 20, mat_h - 20
        banner_res = banner.resize((bw, bh), Image.Resampling.LANCZOS)
        mat_layer.paste(banner_res, (10, 10), banner_res)
        # Re-stroke border
        mdraw = ImageDraw.Draw(mat_layer)
        mdraw.rounded_rectangle([0, 0, mat_w, mat_h], radius=16, outline=(138, 43, 226), width=3)
        mdraw.rounded_rectangle([4, 4, mat_w - 4, mat_h - 4], radius=12, outline=(57, 255, 20), width=2)

    canvas.paste(mat_layer, (mx1, my1), mat_layer)

    # REALISTIC GAMING MOUSE PLACED ON TOP OF THE MAT!
    # Ergonomic esports gaming mouse (e.g. Razer / Logitech style)
    # Placed on the right tracking zone of the mat (around x=700, y=560)
    mouse_cx, mouse_cy = cx + 220, cy + 60
    mouse_w, mouse_h = 100, 160

    # Mouse contact drop shadow on mat
    ms = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    msdraw = ImageDraw.Draw(ms)
    msdraw.ellipse([mouse_cx - mouse_w//2 - 6, mouse_cy - mouse_h//2 + 10, mouse_cx + mouse_w//2 + 6, mouse_cy + mouse_h//2 + 20], fill=(0, 0, 0, 190))
    ms = ms.filter(ImageFilter.GaussianBlur(8))
    canvas = Image.alpha_composite(canvas, ms)
    draw = ImageDraw.Draw(canvas)

    # Mouse Body (Matte black ergonomic chassis with RGB scroll wheel & logo)
    mouse_layer = Image.new("RGBA", (mouse_w, mouse_h), (0, 0, 0, 0))
    ms_draw = ImageDraw.Draw(mouse_layer)
    # Ergonomic contoured chassis
    ms_draw.ellipse([0, 0, mouse_w, mouse_h], fill=(24, 25, 30), outline=(42, 45, 54), width=2)
    # Left & right click divider
    ms_draw.line([(mouse_w//2, 0), (mouse_w//2, 60)], fill=(12, 13, 16), width=2)
    # Textured RGB scroll wheel
    ms_draw.rounded_rectangle([mouse_w//2 - 7, 22, mouse_w//2 + 7, 52], radius=4, fill=(14, 15, 18), outline=(57, 255, 20), width=2)
    # Illuminated Axiom / RGB crest on mouse palm rest
    ms_draw.ellipse([mouse_w//2 - 12, mouse_h - 45, mouse_w//2 + 12, mouse_h - 25], fill=(35, 15, 50), outline=(138, 43, 226), width=2)

    # Rotate mouse slightly (-14 deg) for natural grip angle on desk
    mouse_rot = mouse_layer.rotate(-14, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.paste(mouse_rot, (mouse_cx - mouse_rot.width//2, mouse_cy - mouse_rot.height//2), mouse_rot)

    out_p = os.path.join(PUB_PRODUCTS, "axiom-owl-desk-mat-photorealistic.jpg")
    canvas.convert("RGB").save(out_p, "JPEG", quality=95)
    print(f"Saved: {out_p}")

# -------------------------------------------------------------
# 6. SEPARATE STICKER PACKS: AXIOM ESPORTS VS KROWN JOBSITE
# -------------------------------------------------------------
def render_separate_sticker_packs():
    print("Rendering Separate Sticker Packs (Axiom Holographic vs KrowN Construction)...")
    
    # Pack 1: Axiom Allegiance Holographic Die-Cut Sticker Pack (5-Pack)
    W, H = 1024, 1024
    c_ax = Image.new("RGBA", (W, H), (11, 12, 15, 255))
    draw_ax = ImageDraw.Draw(c_ax)
    
    # Background
    for y in range(H):
        draw_ax.line([(0, y), (W, y)], fill=(12, int(13 + 6*(y/H)), int(18 + 10*(y/H))))

    # 5 Die-Cut Holographic Stickers laid out on slate:
    # 1. Centered Large Smoky Owl Mascot (Holographic rim)
    owl_p = os.path.join(GAMING_DIR, "axiom-smokey-owl-green-eyes-clean.png")
    if os.path.exists(owl_p):
        owl = Image.open(owl_p).convert("RGBA").resize((280, 240), Image.Resampling.LANCZOS)
        # Die-cut white border
        c_ax.paste(owl, (372, 380), owl)

    # 2. Gothic "Axiom Allegiance" Two-Tone Bumper Decal (Top)
    goth_p = os.path.join(GAMING_DIR, "axiom-two-tone-gothic-clean-alpha.png")
    if os.path.exists(goth_p):
        goth = Image.open(goth_p).convert("RGBA").resize((480, 95), Image.Resampling.LANCZOS)
        c_ax.paste(goth, (272, 160), goth)

    # 3. Axiom Owl Mascot Classic (Left)
    classic_owl_p = os.path.join(GAMING_DIR, "axiom-owl-mascot.png")
    if os.path.exists(classic_owl_p):
        cl = Image.open(classic_owl_p).convert("RGBA").resize((190, 260), Image.Resampling.LANCZOS)
        c_ax.paste(cl, (130, 480), cl)

    # 4. Axiom Creed Motto Badge (Right)
    draw_ax.rounded_rectangle([700, 480, 910, 720], radius=14, fill=(18, 19, 24), outline=(57, 255, 20), width=3)
    draw_ax.text((805, 540), "AXIOM", fill=(138, 43, 226), font=get_font(["impact.ttf", "arialbd.ttf"], 28), anchor="mm")
    draw_ax.text((805, 580), "ALLEGIANCE", fill=(57, 255, 20), font=get_font(["impact.ttf", "arialbd.ttf"], 18), anchor="mm")
    draw_ax.text((805, 640), "“PLAY TO REIGN”", fill=(230, 230, 245), font=get_font(["impact.ttf", "arialbd.ttf"], 14), anchor="mm")

    # 5. Holographic Shield Emblem (Bottom Center)
    draw_ax.polygon([(512, 720), (590, 780), (512, 920), (434, 780)], fill=(22, 18, 30), outline=(138, 43, 226), width=3)
    draw_ax.text((512, 800), "AXA", fill=(57, 255, 20), font=get_font(["impact.ttf", "arialbd.ttf"], 24), anchor="mm")

    out_ax = os.path.join(PUB_PRODUCTS, "axiom-stickers-holographic-pack.jpg")
    c_ax.convert("RGB").save(out_ax, "JPEG", quality=95)
    print(f"Saved: {out_ax}")

    # Pack 2: KrowN Construction Weatherproof Jobsite Vinyl Decal 5-Pack
    c_kc = Image.new("RGBA", (W, H), (14, 15, 18, 255))
    draw_kc = ImageDraw.Draw(c_kc)
    for y in range(H):
        draw_kc.line([(0, y), (W, y)], fill=(int(18 + 8*(y/H)), int(18 + 7*(y/H)), int(22 + 6*(y/H))))

    # Hardhat / Tool Box Decals:
    # 1. KrowN Construction Heavy Oval Hardhat Decal (Center)
    draw_kc.ellipse([340, 360, 684, 580], fill=(20, 21, 26), outline=(212, 175, 55), width=4)
    draw_kc.text((512, 440), "KROW N", fill=(212, 175, 55), font=get_font(["impact.ttf", "arialbd.ttf"], 44), anchor="mm")
    draw_kc.text((512, 485), "CONSTRUCTION", fill=(245, 245, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 22), anchor="mm")
    draw_kc.text((512, 520), "SINCE 2018", fill=(57, 255, 20), font=get_font(["arialbd.ttf", "arial.ttf"], 12), anchor="mm")

    # 2. "BUILT TO REIGN" Heavy Jobsite Tool Box Strip (Top)
    draw_kc.rounded_rectangle([212, 180, 812, 280], radius=10, fill=(20, 21, 26), outline=(57, 255, 20), width=3)
    draw_kc.text((512, 230), "BUILT TO REIGN", fill=(245, 245, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 38), anchor="mm")

    # 3. KC Shield Decal (Left)
    draw_kc.polygon([(260, 420), (330, 480), (260, 660), (190, 480)], fill=(20, 21, 26), outline=(212, 175, 55), width=3)
    draw_kc.text((260, 520), "KC", fill=(212, 175, 55), font=get_font(["impact.ttf", "arialbd.ttf"], 36), anchor="mm")

    # 4. KrowN Construction Barricade Stripe Decal (Right)
    draw_kc.rounded_rectangle([690, 460, 890, 680], radius=8, fill=(20, 21, 26), outline=(212, 175, 55), width=3)
    draw_kc.text((790, 530), "TRADES", fill=(57, 255, 20), font=get_font(["impact.ttf", "arialbd.ttf"], 24), anchor="mm")
    draw_kc.text((790, 570), "PRO SPEC", fill=(245, 245, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 20), anchor="mm")
    draw_kc.text((790, 615), "HEAVY DUTY", fill=(212, 175, 55), font=get_font(["arialbd.ttf", "arial.ttf"], 12), anchor="mm")

    # 5. Weatherproof Safety Diamond (Bottom Center)
    draw_kc.polygon([(512, 680), (620, 780), (512, 880), (404, 780)], fill=(20, 21, 26), outline=(57, 255, 20), width=3)
    draw_kc.text((512, 780), "100%\nTOUGH", fill=(245, 245, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 22), anchor="mm")

    out_kc = os.path.join(PUB_PRODUCTS, "krown-construction-jobsite-decals.jpg")
    c_kc.convert("RGB").save(out_kc, "JPEG", quality=95)
    print(f"Saved: {out_kc}")

if __name__ == "__main__":
    fix_krown_shorts()
    fix_krown_beanie()
    render_krown_r112_colorways()
    render_krown_work_shirt()
    render_photoreal_desk_mat_with_mouse()
    render_separate_sticker_packs()
    print("--- ALL REMAINING PRODUCT VISUAL ASSETS RENDERED AND SAVED! ---")
