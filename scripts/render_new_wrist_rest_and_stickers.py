import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUB_BRANDING = os.path.join(BASE_DIR, "public", "images", "branding")
GAMING_DIR = os.path.join(PUB_BRANDING, "gaming")
BRAIN_DIR = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7"
USER_UP = os.path.join(BRAIN_DIR, ".user_uploaded")

os.makedirs(PUB_PRODUCTS, exist_ok=True)

# 1. Branding Assets
krown_gold_crest_path = os.path.join(PUB_BRANDING, "krown-gold-crest-transparent.png")
krown_gold_crest = Image.open(krown_gold_crest_path).convert("RGBA")

owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-green-eyes-clean.png")
if not os.path.exists(owl_smokey_path):
    owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-clean-alpha.png")
owl_smokey = Image.open(owl_smokey_path).convert("RGBA")

gothic_two_tone_path = os.path.join(GAMING_DIR, "axiom-two-tone-gothic-clean-alpha.png")
gothic_two_tone = Image.open(gothic_two_tone_path).convert("RGBA")

def get_font(name_list, size):
    for n in name_list:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()

font_sub = get_font(["arialbd.ttf", "segoeuib.ttf", "arial.ttf"], 22)
font_label = get_font(["arialbd.ttf", "impact.ttf"], 28)
font_micro = get_font(["arialbd.ttf", "arial.ttf"], 14)


# =========================================================================
# 1. CLEAN KROWN STREETWEAR SET (v4): ZERO WALL BLOBS, ZERO POCKET BLOBS
# =========================================================================
def render_krown_streetwear_set_v4():
    print("1. Rendering KrowN Streetwear Set v4 (Pristine Wall, Zero Blobs, Crisp Gold Crests)...")
    src = os.path.join(USER_UP, "media_1791603791996.jpg")
    im = Image.open(src).convert("RGBA")
    W, H = im.size

    # Repair Wall Smudge between hoodie and sweatpants:
    # Smudge is around x=530..620, y=220..320.
    # We sample the clean concrete wall from y=80..180, x=530..620.
    clean_wall_sample = im.crop((530, 80, 625, 180))
    # We create a smooth feather mask for the wall repair
    wall_patch = clean_wall_sample.resize((95, 120), Image.Resampling.LANCZOS)
    
    # Feather mask for wall patch
    mask_wall = Image.new("L", (95, 120), 0)
    m_draw = ImageDraw.Draw(mask_wall)
    m_draw.ellipse([5, 5, 90, 115], fill=255)
    mask_wall = mask_wall.filter(ImageFilter.GaussianBlur(10))
    im.paste(wall_patch, (530, 220), mask_wall)

    # Repair Pocket Smudge on kangaroo pocket:
    # Smudge is around x=425..495, y=425..485.
    # Clean charcoal fabric sample from x=320..390, y=425..485.
    clean_fabric_sample = im.crop((320, 425, 390, 485))
    fabric_patch = clean_fabric_sample.resize((70, 60), Image.Resampling.LANCZOS)
    mask_pocket = Image.new("L", (70, 60), 0)
    p_draw = ImageDraw.Draw(mask_pocket)
    p_draw.ellipse([5, 5, 65, 55], fill=255)
    mask_pocket = mask_pocket.filter(ImageFilter.GaussianBlur(8))
    im.paste(fabric_patch, (425, 425), mask_pocket)

    # Left chest placement for Hoodie: (400, 422)
    hcx, hcy = 400, 422
    # Seamless base cover under gold crest
    h_cover = Image.new("RGBA", (50, 42), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(h_cover)
    h_draw.ellipse([0, 0, 50, 42], fill=(32, 36, 33, 255))
    h_cover = h_cover.filter(ImageFilter.GaussianBlur(3))
    im.paste(h_cover, (hcx - 25, hcy - 21), h_cover)

    # Authentic KrowN faceted gold crown on hoodie chest
    cw = 38
    ch = int(krown_gold_crest.height * (cw / krown_gold_crest.width))
    c_res = krown_gold_crest.resize((cw, ch), Image.Resampling.LANCZOS)
    im.paste(c_res, (hcx - cw // 2, hcy - ch // 2), c_res)

    # Left hip placement for Sweatpants: (746, 444)
    scx, scy = 746, 444
    s_cover = Image.new("RGBA", (44, 38), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_cover)
    s_draw.ellipse([0, 0, 44, 38], fill=(30, 34, 31, 255))
    s_cover = s_cover.filter(ImageFilter.GaussianBlur(3))
    im.paste(s_cover, (scx - 22, scy - 19), s_cover)

    pw = 32
    ph = int(krown_gold_crest.height * (pw / krown_gold_crest.width))
    p_res = krown_gold_crest.resize((pw, ph), Image.Resampling.LANCZOS)
    im.paste(p_res, (scx - pw // 2, scy - ph // 2), p_res)

    out_v4 = os.path.join(PUB_PRODUCTS, "krown-streetwear-set-clean-v4.jpg")
    im.convert("RGB").save(out_v4, "JPEG", quality=98)
    # Also update v3 and v2 in place so nothing breaks
    im.convert("RGB").save(os.path.join(PUB_PRODUCTS, "krown-streetwear-set-v3.jpg"), "JPEG", quality=98)
    print(f"-> Saved clean streetwear set: {out_v4}")


# =========================================================================
# 2. REDESIGN WRIST REST: PHOTOREALISTIC TOURNAMENT SPEC, NO "COOLING GEL"
# =========================================================================
def render_wrist_rest_clean_v3():
    print("2. Rendering Wrist Rest Clean v3 (Zero 'Cooling Gel' text, Photorealistic Battlestation Studio)...")
    W, H = 1024, 1024
    
    # High-end dark battlestation studio background
    # Subtle dark carbon / micro-weave desk mat surface with soft radial studio spotlight
    bg = Image.new("RGBA", (W, H), (14, 15, 19, 255))
    bg_draw = ImageDraw.Draw(bg)
    
    # Ambient radial studio gradient
    cx, cy = 512, 512
    for r in range(600, 0, -4):
        alpha = int(45 * (1.0 - r / 600.0))
        # subtle royal purple / midnight ambient glow
        bg_draw.ellipse([cx - r, cy - r*0.8, cx + r, cy + r*0.8], fill=(35, 15, 55, alpha))

    # Fine desk mat micro-texture
    noise = np.random.RandomState(42).randint(-3, 4, (H, W, 3))
    bg_arr = np.array(bg.convert("RGB"), dtype=np.int16)
    bg_arr = np.clip(bg_arr + noise, 0, 255).astype(np.uint8)
    bg = Image.fromarray(bg_arr).convert("RGBA")

    # Render a Realistic Tournament Keyboard Wrist Rest (Tenkeyless / Compact 80% format)
    # Pad dimensions: width 820, height 180 (centered at cx=512, cy=520)
    pad_w, pad_h = 820, 180
    px1 = cx - pad_w // 2
    py1 = cy - pad_h // 2 + 20
    px2 = px1 + pad_w
    py2 = py1 + pad_h

    # 1. Realistic Multi-Layer Floor Drop Shadows
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    # Ambient contact shadow (tight, deep)
    s_draw.rounded_rectangle([px1 - 4, py1 + 10, px2 + 4, py2 + 24], radius=24, fill=(0, 0, 0, 230))
    # Extended soft ambient shadow
    s_draw.rounded_rectangle([px1 - 18, py1 + 22, px2 + 18, py2 + 45], radius=32, fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    bg = Image.alpha_composite(bg, shadow)

    # 2. Wrist Rest Body Layer
    pad = Image.new("RGBA", (pad_w, pad_h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(pad)

    # Deep matte obsidian lycra surface with subtle ergonomic cushion curvature
    # Draw ergonomic gradient from back (high) to front slope (low)
    for y in range(pad_h):
        # 15 degree ergonomic slope: top edge slightly darker, center has silky sheen
        norm_y = y / float(pad_h)
        if norm_y < 0.25:
            # Back edge bevel
            shade = int(18 + 12 * (norm_y / 0.25))
        elif norm_y < 0.75:
            # Rest surface silky sheen
            shade = int(30 - 6 * abs(norm_y - 0.5) / 0.25)
        else:
            # Front beveled slope
            shade = int(24 - 10 * ((norm_y - 0.75) / 0.25))
        p_draw.line([(0, y), (pad_w, y)], fill=(shade, shade + 1, shade + 3, 255))

    # Mask pad to rounded ergonomic cushion shape (radius 22)
    pad_mask = Image.new("L", (pad_w, pad_h), 0)
    pm_draw = ImageDraw.Draw(pad_mask)
    pm_draw.rounded_rectangle([0, 0, pad_w, pad_h], radius=22, fill=255)
    
    pad_shaped = Image.new("RGBA", (pad_w, pad_h), (0, 0, 0, 0))
    pad_shaped.paste(pad, (0, 0), pad_mask)

    # 3. Precision Anti-Fray Perimeter Stitching (Double-stitched tournament seam)
    ps_draw = ImageDraw.Draw(pad_shaped)
    # Outer precision royal purple seam
    ps_draw.rounded_rectangle([3, 3, pad_w - 4, pad_h - 4], radius=19, outline=(138, 43, 226, 220), width=2)
    # Inner precision toxic green micro-accent stitch (subtle, 1px)
    ps_draw.rounded_rectangle([6, 6, pad_w - 7, pad_h - 7], radius=16, outline=(57, 255, 20, 140), width=1)

    # 4. Official Branding on Wrist Rest:
    # CLEAN AESTHETIC: Sleek Axiom Owl + Gothic "AXIOM ALLEGIANCE"
    # ABSOLUTELY ZERO "tournament cooling gel" text, ZERO "ergonomic memory core"!
    
    # Left Emblem: Official Smoky Axiom Owl with Glowing Toxic Green Eyes
    owl_h = int(pad_h * 0.74)
    owl_w = int(owl_smokey.width * (owl_h / owl_smokey.height))
    owl_resized = owl_smokey.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
    pad_shaped.paste(owl_resized, (48, (pad_h - owl_h) // 2), owl_resized)

    # Center-Left Typography: Two-Tone Gothic "AXIOM ALLEGIANCE"
    g_h = int(pad_h * 0.42)
    g_w = int(gothic_two_tone.width * (g_h / gothic_two_tone.height))
    g_resized = gothic_two_tone.resize((g_w, g_h), Image.Resampling.LANCZOS)
    pad_shaped.paste(g_resized, (48 + owl_w + 32, (pad_h - g_h) // 2), g_resized)

    # Right Accent: Subtle Minimalist AXA Hex Crest watermark
    hex_badge = Image.new("RGBA", (70, 70), (0, 0, 0, 0))
    hb_draw = ImageDraw.Draw(hex_badge)
    hb_draw.polygon([(35, 4), (66, 20), (66, 50), (35, 66), (4, 50), (4, 20)], outline=(138, 43, 226, 120), width=2)
    hb_draw.text((35, 35), "AXA", fill=(57, 255, 20, 160), font=get_font(["impact.ttf", "arialbd.ttf"], 16), anchor="mm")
    pad_shaped.paste(hex_badge, (pad_w - 110, (pad_h - 70) // 2), hex_badge)

    # Paste wrist rest onto battlestation background
    bg.paste(pad_shaped, (px1, py1), pad_shaped)

    # Studio Lighting Highlights (Subtle specular reflections across the lycra cushion)
    highlight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    # Sleek top bevel edge highlight
    hl_draw.line([(px1 + 25, py1 + 4), (px2 - 25, py1 + 4)], fill=(255, 255, 255, 38), width=2)
    bg = Image.alpha_composite(bg, highlight)

    # High-end Editorial UI Overlays (Subtle, professional)
    draw_final = ImageDraw.Draw(bg)
    draw_final.text((cx, 75), "AXIOM ALLEGIANCE // TOURNAMENT GEAR", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw_final.text((cx, 115), "PRO ERGONOMIC KEYBOARD WRIST REST", fill=(245, 245, 255), font=get_font(["arialbd.ttf", "impact.ttf"], 36), anchor="mm")
    
    # 3 Size indicators at bottom
    sizes_info = [
        ("COMPACT 60%", "11.4\" x 2.9\"", "$19.99"),
        ("TENKEYLESS 80%", "14.2\" x 2.9\"", "$21.99"),
        ("FULL-SIZE 100%", "17.5\" x 2.9\"", "$23.99"),
    ]
    for i, (sz, dim, pr) in enumerate(sizes_info):
        bx = cx - 280 + i * 280
        by = 840
        draw_final.rounded_rectangle([bx - 120, by, bx + 120, by + 75], radius=10, fill=(20, 22, 28), outline=(42, 45, 56), width=1)
        draw_final.text((bx, by + 22), sz, fill=(57, 255, 20), font=get_font(["arialbd.ttf"], 16), anchor="mm")
        draw_final.text((bx, by + 46), f"{dim} • {pr}", fill=(200, 200, 215), font=get_font(["arial.ttf"], 13), anchor="mm")

    draw_final.text((cx, 970), "ANTI-FRAY PRECISION STITCHING • TEXTURED NON-SLIP SILICONE BASE • SILKY LYCRA GLIDE", fill=(130, 135, 150), font=get_font(["arial.ttf"], 12), anchor="mm")

    out_wr = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-clean-v3.jpg")
    bg.convert("RGB").save(out_wr, "JPEG", quality=96)
    # Also overwrite the old tournament-edition files so existing references pick up the pristine redesign
    bg.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-tournament-edition-v2.jpg"), "JPEG", quality=96)
    bg.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-tournament-edition.jpg"), "JPEG", quality=96)
    print(f"-> Saved clean wrist rest: {out_wr}")


# =========================================================================
# 2B. COMPANION IN-SITU BATTLESTATION SETUP (Keyboard + Wrist Rest)
# =========================================================================
def render_wrist_rest_setup_v3():
    print("2B. Rendering Wrist Rest In-Situ Battlestation Setup v3...")
    W, H = 1024, 1024
    bg = Image.new("RGBA", (W, H), (12, 13, 17, 255))
    draw = ImageDraw.Draw(bg)
    cx = 512

    # Subtle ambient lighting
    for r in range(550, 0, -5):
        alpha = int(40 * (1.0 - r / 550.0))
        draw.ellipse([cx - r, 450 - r*0.7, cx + r, 450 + r*0.7], fill=(30, 15, 48, alpha))

    # Sleek Minimalist Mechanical Keyboard (TKL)
    kb_w, kb_h = 740, 250
    kb_y = 190
    # Keyboard shadow
    kb_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kbs_draw = ImageDraw.Draw(kb_shadow)
    kbs_draw.rounded_rectangle([cx - kb_w//2 - 6, kb_y + 10, cx + kb_w//2 + 6, kb_y + kb_h + 20], radius=16, fill=(0, 0, 0, 200))
    kb_shadow = kb_shadow.filter(ImageFilter.GaussianBlur(14))
    bg = Image.alpha_composite(bg, kb_shadow)
    draw = ImageDraw.Draw(bg)

    # Keyboard CNC Aluminum Case
    draw.rounded_rectangle([cx - kb_w//2, kb_y, cx + kb_w//2, kb_y + kb_h], radius=12, fill=(22, 23, 28), outline=(48, 51, 62), width=2)
    # Subtle Toxic Green Underglow Line
    draw.line([(cx - kb_w//2 + 30, kb_y + kb_h - 2), (cx + kb_w//2 - 30, kb_y + kb_h - 2)], fill=(57, 255, 20, 200), width=3)

    # Realistic Keycaps Grid (Charcoal PBT keycaps with subtle purple WASD / Esc accents)
    for row in range(5):
        ky = kb_y + 20 + row * 43
        for col in range(16):
            kx = cx - kb_w//2 + 32 + col * 42
            # Keycap body
            is_wasd = (row == 2 and col in [2, 3, 4]) or (row == 1 and col == 3)
            fill_col = (38, 22, 54) if is_wasd else (30, 31, 38)
            border_col = (138, 43, 226) if is_wasd else (46, 48, 58)
            draw.rounded_rectangle([kx, ky, kx + 36, ky + 36], radius=4, fill=fill_col, outline=border_col, width=1)

    # Wrist Rest Positioned Flush in Front of Keyboard
    wr_w, wr_h = 740, 140
    wr_y = kb_y + kb_h + 30

    # Wrist rest shadow
    wr_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wrs_draw = ImageDraw.Draw(wr_shadow)
    wrs_draw.rounded_rectangle([cx - wr_w//2 - 8, wr_y + 12, cx + wr_w//2 + 8, wr_y + wr_h + 26], radius=18, fill=(0, 0, 0, 220))
    wr_shadow = wr_shadow.filter(ImageFilter.GaussianBlur(16))
    bg = Image.alpha_composite(bg, wr_shadow)
    draw = ImageDraw.Draw(bg)

    # Wrist rest body
    pad = Image.new("RGBA", (wr_w, wr_h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(pad)
    # Ergonomic gradient
    for y in range(wr_h):
        norm = y / float(wr_h)
        val = int(24 + 6 * math.sin(norm * math.pi))
        p_draw.line([(0, y), (wr_w, y)], fill=(val, val + 1, val + 3, 255))
    
    pad_mask = Image.new("L", (wr_w, wr_h), 0)
    ImageDraw.Draw(pad_mask).rounded_rectangle([0, 0, wr_w, wr_h], radius=18, fill=255)
    pad_shaped = Image.new("RGBA", (wr_w, wr_h), (0, 0, 0, 0))
    pad_shaped.paste(pad, (0, 0), pad_mask)

    # Precision stitched borders
    ps_draw = ImageDraw.Draw(pad_shaped)
    ps_draw.rounded_rectangle([2, 2, wr_w - 3, wr_h - 3], radius=16, outline=(138, 43, 226, 220), width=2)
    ps_draw.rounded_rectangle([5, 5, wr_w - 6, wr_h - 6], radius=13, outline=(57, 255, 20, 140), width=1)

    # Official Clean Branding: Smoky Owl + Gothic AXIOM ALLEGIANCE
    # ZERO "cooling gel" text!
    owl_h = int(wr_h * 0.72)
    owl_w = int(owl_smokey.width * (owl_h / owl_smokey.height))
    owl_res = owl_smokey.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
    pad_shaped.paste(owl_res, (40, (wr_h - owl_h) // 2), owl_res)

    g_h = int(wr_h * 0.40)
    g_w = int(gothic_two_tone.width * (g_h / gothic_two_tone.height))
    g_res = gothic_two_tone.resize((g_w, g_h), Image.Resampling.LANCZOS)
    pad_shaped.paste(g_res, (40 + owl_w + 28, (wr_h - g_h) // 2), g_res)

    bg.paste(pad_shaped, (cx - wr_w//2, wr_y), pad_shaped)
    draw = ImageDraw.Draw(bg)

    # Editorial Callout Cards
    draw.text((cx, 65), "AXIOM ALLEGIANCE // BATTLESTATION SETUP", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw.text((cx, 105), "FLUSH ERGONOMIC TOURNAMENT MATING", fill=(245, 245, 255), font=get_font(["arialbd.ttf", "impact.ttf"], 30), anchor="mm")

    c_y = 660
    callouts = [
        ("01. SEAMLESS FITMENT", "Engineered to sit perfectly flush against 60%, TKL, and Full-Size boards."),
        ("02. MARATHON ERGONOMICS", "Optimum 15° slope eliminates wrist extension fatigue during long sessions."),
        ("03. COMMERCIAL GRADE", "Anti-fray stitched edge perimeter and heavy-grip non-slip silicone base."),
    ]
    for i, (title, desc) in enumerate(callouts):
        cy_i = c_y + i * 85
        draw.rounded_rectangle([cx - 370, cy_i, cx + 370, cy_i + 70], radius=8, fill=(18, 19, 25), outline=(40, 42, 54), width=1)
        draw.text((cx - 350, cy_i + 22), title, fill=(57, 255, 20), font=get_font(["arialbd.ttf"], 18), anchor="ls")
        draw.text((cx - 350, cy_i + 48), desc, fill=(180, 185, 200), font=get_font(["arial.ttf"], 14), anchor="ls")

    draw.text((cx, 970), "DESIGNED FOR COMPETITIVE ESPORTS • AXIOM ALLEGIANCE OFFICIAL GEAR", fill=(120, 125, 140), font=get_font(["arial.ttf"], 12), anchor="mm")

    out_setup = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-setup-v3.jpg")
    bg.convert("RGB").save(out_setup, "JPEG", quality=96)
    bg.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-stealth-setup.jpg"), "JPEG", quality=96)
    print(f"-> Saved clean wrist rest setup: {out_setup}")


# =========================================================================
# 3. REDESIGN STICKERS: AUTHENTIC DIE-CUT HOLOGRAPHIC VINYL 5-PACK
# =========================================================================
def render_stickers_holographic_v3():
    print("3. Rendering Axiom Holographic Stickers v3 (Die-Cut Vinyl, Rainbow Sheen, Real Desk Surface)...")
    W, H = 1024, 1024

    # High-end cutting mat / dark battlestation slate desk surface
    bg = Image.new("RGBA", (W, H), (15, 16, 20, 255))
    draw = ImageDraw.Draw(bg)

    # Subtle workbench grid lines (photorealistic self-healing craft mat aesthetic)
    grid_col = (25, 27, 34)
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=grid_col, width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=grid_col, width=1)

    # Ambient studio spotlight from top-left
    spotlight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(spotlight)
    for r in range(700, 0, -5):
        alpha = int(35 * (1.0 - r / 700.0))
        s_draw.ellipse([300 - r, 300 - r, 300 + r, 300 + r], fill=(138, 43, 226, alpha))
    bg = Image.alpha_composite(bg, spotlight)

    # Function to create an authentic Die-Cut Holographic Sticker
    def make_die_cut_sticker(fg_img, border_radius=16, border_width=10, angle=0):
        # 1. Expand canvas for white die-cut vinyl border
        fw, fh = fg_img.size
        bw = fw + border_width * 2
        bh = fh + border_width * 2

        # Create sticker base with white die-cut vinyl edge
        stk = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        stk_draw = ImageDraw.Draw(stk)

        # White die-cut vinyl border
        stk_draw.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=border_radius, fill=(248, 248, 252, 255))
        # Inner thin silver foil rim
        stk_draw.rounded_rectangle([2, 2, bw - 3, bh - 3], radius=border_radius - 2, outline=(220, 220, 230), width=1)

        # 2. Paste graphic centered
        stk.paste(fg_img, (border_width, border_width), fg_img)

        # 3. Holographic Iridescent Rainbow Sheen Overlay
        holo_overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        ho_draw = ImageDraw.Draw(holo_overlay)
        # Diagonal rainbow sheen bands (Violet -> Cyan -> Lime -> Gold -> Magenta)
        for d in range(-bw, bw + bh, 6):
            # calculate rainbow cycle
            phase = (d % 180) / 180.0
            r = int(127 + 127 * math.sin(phase * 2 * math.pi))
            g = int(127 + 127 * math.sin((phase + 0.33) * 2 * math.pi))
            b = int(127 + 127 * math.sin((phase + 0.66) * 2 * math.pi))
            ho_draw.line([(d, 0), (d + bh, bh)], fill=(r, g, b, 50), width=4)
        
        # Clip holo overlay to sticker contour
        stk_mask = stk.split()[3]
        stk = Image.composite(Image.alpha_composite(stk, holo_overlay), stk, stk_mask)

        # 4. Glossy Specular Light Reflection Streak across sticker
        spec = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        sp_draw = ImageDraw.Draw(spec)
        sp_draw.polygon([(bw * 0.2, 0), (bw * 0.45, 0), (bw * 0.25, bh), (0, bh)], fill=(255, 255, 255, 45))
        stk = Image.composite(Image.alpha_composite(stk, spec), stk, stk_mask)

        # 5. Realistic Drop Shadow
        if angle != 0:
            stk = stk.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

        sw, sh = stk.size
        shadow = Image.new("RGBA", (sw + 24, sh + 24), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_mask = stk.split()[3]
        shadow.paste((0, 0, 0, 180), (12, 14), sh_mask)
        shadow = shadow.filter(ImageFilter.GaussianBlur(8))

        return stk, shadow

    # The 5 Stickers to Layout:
    
    # STICKER 1: Large Die-Cut Smoky Axiom Owl Mascot (Center Hero, 280x260)
    owl_crop = owl_smokey.resize((260, 240), Image.Resampling.LANCZOS)
    stk1, sh1 = make_die_cut_sticker(owl_crop, border_radius=20, border_width=12, angle=-3)

    # STICKER 2: Gothic "AXIOM ALLEGIANCE" Two-Tone Bumper Banner (Top, 460x90)
    goth_crop = gothic_two_tone.resize((440, 85), Image.Resampling.LANCZOS)
    stk2, sh2 = make_die_cut_sticker(goth_crop, border_radius=14, border_width=10, angle=2)

    # STICKER 3: Geometric AXA Diamond Shield (Bottom Left, 160x180)
    shield_img = Image.new("RGBA", (150, 170), (0, 0, 0, 0))
    sh_d = ImageDraw.Draw(shield_img)
    # Diamond crest body
    sh_d.polygon([(75, 4), (146, 50), (75, 166), (4, 50)], fill=(22, 18, 32, 255), outline=(138, 43, 226), width=4)
    sh_d.polygon([(75, 14), (136, 52), (75, 154), (14, 52)], fill=(26, 22, 38, 255))
    sh_d.text((75, 60), "AXA", fill=(57, 255, 20), font=get_font(["impact.ttf", "arialbd.ttf"], 36), anchor="mm")
    sh_d.text((75, 96), "ESPORTS", fill=(240, 240, 255), font=get_font(["arialbd.ttf"], 12), anchor="mm")
    stk3, sh3 = make_die_cut_sticker(shield_img, border_radius=16, border_width=10, angle=-5)

    # STICKER 4: Hexagonal "PLAY TO REIGN" Battle Seal (Bottom Right, 170x170)
    hex_img = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    hx_d = ImageDraw.Draw(hex_img)
    hx_d.polygon([(80, 4), (156, 45), (156, 115), (80, 156), (4, 115), (4, 45)], fill=(18, 20, 28, 255), outline=(57, 255, 20), width=4)
    hx_d.text((80, 42), "AXIOM", fill=(138, 43, 226), font=get_font(["impact.ttf", "arialbd.ttf"], 24), anchor="mm")
    hx_d.text((80, 78), "ALLEGIANCE", fill=(245, 245, 255), font=get_font(["impact.ttf", "arialbd.ttf"], 16), anchor="mm")
    hx_d.text((80, 115), "“PLAY TO REIGN”", fill=(57, 255, 20), font=get_font(["arialbd.ttf"], 11), anchor="mm")
    stk4, sh4 = make_die_cut_sticker(hex_img, border_radius=16, border_width=10, angle=4)

    # STICKER 5: Minimalist Toxic Owl Head Crest (Bottom Center, 160x160)
    classic_owl_p = os.path.join(GAMING_DIR, "axiom-owl-mascot.png")
    if os.path.exists(classic_owl_p):
        owl_face = Image.open(classic_owl_p).convert("RGBA").resize((150, 160), Image.Resampling.LANCZOS)
    else:
        owl_face = owl_smokey.resize((150, 150), Image.Resampling.LANCZOS)
    stk5, sh5 = make_die_cut_sticker(owl_face, border_radius=18, border_width=10, angle=1)

    # Positions on desk surface:
    placements = [
        # (stk, sh, x, y)
        (stk2, sh2, 270, 140), # Gothic banner top
        (stk1, sh1, 355, 330), # Large smoky owl center
        (stk3, sh3, 110, 490), # Shield left
        (stk5, sh5, 415, 660), # Owl head bottom center
        (stk4, sh4, 720, 490), # Hex seal right
    ]

    # Paste shadows first
    for stk, sh, px, py in placements:
        bg.paste(sh, (px - 12, py - 10), sh)

    # Paste stickers
    for stk, sh, px, py in placements:
        bg.paste(stk, (px, py), stk)

    # Editorial Header & Features
    draw_f = ImageDraw.Draw(bg)
    draw_f.text((512, 50), "AXIOM ALLEGIANCE // MERCHANDISE LOADOUT", fill=(138, 43, 226), font=font_sub, anchor="mm")
    draw_f.text((512, 90), "HOLOGRAPHIC BATTLE PACK DECALS (5-PACK)", fill=(245, 245, 255), font=get_font(["arialbd.ttf", "impact.ttf"], 32), anchor="mm")

    # Feature callouts at bottom
    features = [
        "• 6 MIL WEATHERPROOF VINYL",
        "• UV-RESISTANT LAMINATE",
        "• IRIDESCENT HOLOGRAPHIC FOIL",
        "• DIE-CUT EASY-PEEL",
    ]
    draw_f.text((512, 955), "  |  ".join(features), fill=(57, 255, 20), font=get_font(["arialbd.ttf"], 13), anchor="mm")
    draw_f.text((512, 985), "PERFECT FOR BATTLESTATIONS, GAMING LAPTOPS, RIG CASES & WATER BOTTLES", fill=(140, 145, 160), font=get_font(["arial.ttf"], 11), anchor="mm")

    out_stk = os.path.join(PUB_PRODUCTS, "axiom-stickers-holographic-battle-pack-v3.jpg")
    bg.convert("RGB").save(out_stk, "JPEG", quality=96)
    # Also overwrite the old axiom-stickers-holographic-pack.jpg so all references pick up the new photo
    bg.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-stickers-holographic-pack.jpg"), "JPEG", quality=96)
    print(f"-> Saved clean holographic stickers: {out_stk}")


if __name__ == "__main__":
    render_krown_streetwear_set_v4()
    render_wrist_rest_clean_v3()
    render_wrist_rest_setup_v3()
    render_stickers_holographic_v3()
    print("\nAll new renders generated successfully!")
