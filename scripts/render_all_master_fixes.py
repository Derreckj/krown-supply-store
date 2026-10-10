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

# Authentic assets
krown_gold_crest_path = os.path.join(PUB_BRANDING, "krown-gold-crest-transparent.png")
krown_gold_crest = Image.open(krown_gold_crest_path).convert("RGBA") if os.path.exists(krown_gold_crest_path) else None

owl_mascot_path = os.path.join(GAMING_DIR, "axiom-owl-mascot.png")
owl_mascot = Image.open(owl_mascot_path).convert("RGBA") if os.path.exists(owl_mascot_path) else None

owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-green-eyes-clean.png")
if not os.path.exists(owl_smokey_path):
    owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-clean.png")
owl_smokey = Image.open(owl_smokey_path).convert("RGBA") if os.path.exists(owl_smokey_path) else None

kc_logo_candidates = [
    os.path.join(CONST_DIR, "KC logo black and gold.png"),
    os.path.join(CONST_DIR, "KC logo by itself.png"),
    os.path.join(CONST_DIR, "KC.png"),
]
kc_logo = None
for c in kc_logo_candidates:
    if os.path.exists(c):
        kc_logo = Image.open(c).convert("RGBA")
        break

# -------------------------------------------------------------------------
# 1. FIX SHORTS THUMBNAIL: Clean 1024x1024 Studio Crop + Authentic Crown
# -------------------------------------------------------------------------
def render_shorts_v2():
    print("1. Rendering Shorts V2: Studio Square (No phone screenshot borders!)...")
    src = os.path.join(USER_UP, "media_1791603960066.png")
    im = Image.open(src).convert("RGBA")
    
    # In media_1791603960066.png:
    # The shorts box is roughly x: [60, 412], y: [248, 452]
    shorts_crop = im.crop((55, 244, 417, 456))
    
    # Create 1024x1024 clean studio canvas with soft neutral light
    canvas = Image.new("RGBA", (1024, 1024), (242, 243, 245, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Soft studio vignette
    for r in range(600, 0, -20):
        alpha = int(18 * (1.0 - r / 600.0))
        draw.ellipse([512 - r, 512 - r, 512 + r, 512 + r], fill=(255, 255, 255, alpha))
        
    # Scale shorts crop up cleanly to fill ~760x760
    target_w = 780
    target_h = int(shorts_crop.height * (target_w / shorts_crop.width))
    shorts_res = shorts_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Paste centered
    paste_x = (1024 - target_w) // 2
    paste_y = (1024 - target_h) // 2 - 10
    
    # Soft drop shadow underneath shorts
    sh_shadow = Image.new("RGBA", (target_w + 40, target_h + 40), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sh_shadow)
    s_draw.ellipse([20, target_h - 20, target_w + 20, target_h + 30], fill=(0, 0, 0, 45))
    sh_shadow = sh_shadow.filter(ImageFilter.GaussianBlur(14))
    canvas.paste(sh_shadow, (paste_x - 20, paste_y - 20), sh_shadow)
    
    canvas.paste(shorts_res, (paste_x, paste_y), shorts_res)
    
    # Cleanly embroider the authentic KrowN faceted gold crown on the left thigh (viewer's right)
    if krown_gold_crest:
        # Thigh coord on canvas: paste_x + target_w * 0.72, paste_y + target_h * 0.52
        cx = int(paste_x + target_w * 0.71)
        cy = int(paste_y + target_h * 0.52)
        
        # Cover old generic crown with dark French Terry patch
        cover = Image.new("RGBA", (110, 95), (0, 0, 0, 0))
        c_draw = ImageDraw.Draw(cover)
        c_draw.ellipse([0, 0, 110, 95], fill=(32, 33, 37, 255))
        cover = cover.filter(ImageFilter.GaussianBlur(5))
        canvas.paste(cover, (cx - 55, cy - 47), cover)
        
        # Authentic gold crown
        cw = 75
        ch = int(krown_gold_crest.height * (cw / krown_gold_crest.width))
        c_res = krown_gold_crest.resize((cw, ch), Image.Resampling.LANCZOS)
        
        # Embroidery drop shadow
        emb_sh = Image.new("RGBA", (cw + 12, ch + 12), (0, 0, 0, 0))
        es_draw = ImageDraw.Draw(emb_sh)
        es_draw.ellipse([4, 6, cw + 8, ch + 8], fill=(0, 0, 0, 150))
        emb_sh = emb_sh.filter(ImageFilter.GaussianBlur(3))
        canvas.paste(emb_sh, (cx - cw // 2 - 2, cy - ch // 2 + 2), emb_sh)
        canvas.paste(c_res, (cx - cw // 2, cy - ch // 2), c_res)
        
    out_p = os.path.join(PUB_PRODUCTS, "krown-french-terry-shorts-v2.jpg")
    canvas.convert("RGB").save(out_p, "JPEG", quality=96)
    print(f"-> Saved: {out_p}")


# -------------------------------------------------------------------------
# 2. AXIOM DAD HAT V2: 100% PURE OWL MASCOT (ZERO GOLD CROWN)
# -------------------------------------------------------------------------
def render_axiom_dad_hat_v2():
    print("2. Rendering Axiom Dad Hat V2: Pristine Black Chino Twill, Owl ONLY (0% Crown)...")
    base_src = os.path.join(USER_UP, "media_1791603906255.jpg")
    canvas = Image.open(base_src).convert("RGBA")
    w, h = canvas.size
    
    # The center embroidery is at cx = w // 2, cy = int(h * 0.54)
    cx = w // 2
    cy = int(h * 0.535)
    
    # Patch over the entire old embroidery area with genuine garment-washed black chino twill texture
    patch_w = int(w * 0.28)
    patch_h = int(h * 0.26)
    
    twill_patch = Image.new("RGBA", (patch_w, patch_h), (0, 0, 0, 0))
    tp_draw = ImageDraw.Draw(twill_patch)
    tp_draw.ellipse([0, 0, patch_w, patch_h], fill=(34, 35, 39, 255))
    # Soft edge feather
    twill_patch = twill_patch.filter(ImageFilter.GaussianBlur(8))
    canvas.paste(twill_patch, (cx - patch_w // 2, cy - patch_h // 2), twill_patch)
    
    # Composite the PURE Axiom Owl Mascot (Zero gold crown, purple head & green glowing eyes)
    if owl_mascot:
        owl_target_w = int(w * 0.165)
        owl_target_h = int(owl_mascot.height * (owl_target_w / owl_mascot.width))
        owl_res = owl_mascot.resize((owl_target_w, owl_target_h), Image.Resampling.LANCZOS)
        
        # Soft embroidery satin-stitch drop shadow
        sh = Image.new("RGBA", (owl_target_w + 14, owl_target_h + 14), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh)
        sh_draw.ellipse([4, 6, owl_target_w + 10, owl_target_h + 10], fill=(0, 0, 0, 160))
        sh = sh.filter(ImageFilter.GaussianBlur(4))
        
        canvas.paste(sh, (cx - owl_target_w // 2 - 2, cy - owl_target_h // 2 + 2), sh)
        canvas.paste(owl_res, (cx - owl_target_w // 2, cy - owl_target_h // 2), owl_res)
        
    out_p = os.path.join(PUB_PRODUCTS, "axiom-dad-hat-washed-black-v2.jpg")
    canvas.convert("RGB").save(out_p, "JPEG", quality=96)
    print(f"-> Saved: {out_p}")


# -------------------------------------------------------------------------
# 3. AXIOM LOOKBOOK MODEL: WEARING AXIOM ALLEGIANCE APPAREL (ZERO KROWN HOODIE)
# -------------------------------------------------------------------------
def render_axiom_model_lookbook_v2():
    print("3. Rendering Axiom Model Lookbook V2: Model Wearing Pure Axiom Apparel...")
    src = os.path.join(PUB_PRODUCTS, "axiom-hat-model-lookbook.jpg")
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    
    # In the model lookbook photo, model stands in brick courtyard.
    # The chest logo on the model's hoodie is at x ~ w*0.315, y ~ h*0.485
    cx = int(w * 0.315)
    cy = int(h * 0.485)
    
    # Patch over the old KrowN chest gold logo with dark washed fleece
    patch_w = int(w * 0.08)
    patch_h = int(h * 0.06)
    dp = Image.new("RGBA", (patch_w, patch_h), (0, 0, 0, 0))
    dp_draw = ImageDraw.Draw(dp)
    dp_draw.ellipse([0, 0, patch_w, patch_h], fill=(22, 23, 26, 255))
    dp = dp.filter(ImageFilter.GaussianBlur(5))
    im.paste(dp, (cx - patch_w // 2, cy - patch_h // 2), dp)
    
    # Paste clean Axiom Owl mascot emblem on model's chest
    if owl_mascot:
        owl_w = int(w * 0.055)
        owl_h = int(owl_mascot.height * (owl_w / owl_mascot.width))
        owl_res = owl_mascot.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
        im.paste(owl_res, (cx - owl_w // 2, cy - owl_h // 2), owl_res)
        
    out_p = os.path.join(PUB_PRODUCTS, "axiom-hat-model-lookbook-v2.jpg")
    im.convert("RGB").save(out_p, "JPEG", quality=95)
    print(f"-> Saved: {out_p}")


# -------------------------------------------------------------------------
# 4. KROWN STREETWEAR SET V2: AUTHENTIC KROWN FACETED GOLD CROWN
# -------------------------------------------------------------------------
def render_streetwear_set_v2():
    print("4. Rendering KrowN Streetwear Set V2: Authentic Faceted Gold Crown on Hoodie & Pants...")
    src = os.path.join(USER_UP, "media_1791603791996.jpg")
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    
    # Hoodie chest is roughly cx = int(w*0.50), cy = int(h*0.32)
    # Sweatpants left hip is cx = int(w*0.37), cy = int(h*0.62)
    
    if krown_gold_crest:
        # 1. Hoodie chest
        hcx = int(w * 0.50)
        hcy = int(h * 0.315)
        
        # Cover old generic crown
        h_cover = Image.new("RGBA", (140, 110), (0, 0, 0, 0))
        hc_draw = ImageDraw.Draw(h_cover)
        hc_draw.ellipse([0, 0, 140, 110], fill=(28, 29, 33, 255))
        h_cover = h_cover.filter(ImageFilter.GaussianBlur(8))
        im.paste(h_cover, (hcx - 70, hcy - 55), h_cover)
        
        # Authentic crown
        hw = 95
        hh = int(krown_gold_crest.height * (hw / krown_gold_crest.width))
        h_res = krown_gold_crest.resize((hw, hh), Image.Resampling.LANCZOS)
        im.paste(h_res, (hcx - hw // 2, hcy - hh // 2), h_res)
        
        # 2. Sweatpants thigh
        pcx = int(w * 0.38)
        pcy = int(h * 0.63)
        
        p_cover = Image.new("RGBA", (110, 90), (0, 0, 0, 0))
        pc_draw = ImageDraw.Draw(p_cover)
        pc_draw.ellipse([0, 0, 110, 90], fill=(28, 29, 33, 255))
        p_cover = p_cover.filter(ImageFilter.GaussianBlur(6))
        im.paste(p_cover, (pcx - 55, pcy - 45), p_cover)
        
        pw = 70
        ph = int(krown_gold_crest.height * (pw / krown_gold_crest.width))
        p_res = krown_gold_crest.resize((pw, ph), Image.Resampling.LANCZOS)
        im.paste(p_res, (pcx - pw // 2, pcy - ph // 2), p_res)
        
    out_p = os.path.join(PUB_PRODUCTS, "krown-streetwear-set-v2.jpg")
    im.convert("RGB").save(out_p, "JPEG", quality=96)
    print(f"-> Saved: {out_p}")


# -------------------------------------------------------------------------
# 5. KROWN BEANIE V2: "SINCE 2018" (8 YEARS) & AUTHENTIC LOGO
# -------------------------------------------------------------------------
def render_beanie_v2():
    print("5. Rendering KrowN Construction Beanie V2: Patch with 'SINCE 2018'...")
    src = os.path.join(BRAIN_DIR, "krown_beanie_studio_front_1791570168479.jpg")
    if not os.path.exists(src):
        src = os.path.join(PUB_PRODUCTS, "krown-beanie-studio-front.jpg")
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    
    # Patch position on ribbed cuff: cx = int(w*0.50), cy = int(h*0.235)
    pw = int(w * 0.26)
    ph = int(h * 0.11)
    px = int(w * 0.37)
    py = int(h * 0.18)
    
    patch = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(patch)
    
    # Heavy leatherette patch with stitched border
    pdraw.rounded_rectangle([0, 0, pw, ph], radius=12, fill=(20, 18, 24), outline=(212, 175, 55), width=3)
    pdraw.rounded_rectangle([3, 3, pw - 3, ph - 3], radius=10, outline=(140, 110, 35), width=1)
    
    # Authentic KC Monogram / Emblem
    f_kc = get_font(["impact.ttf", "arialbd.ttf"], int(ph * 0.38))
    f_sub = get_font(["arialbd.ttf"], int(ph * 0.14))
    f_date = get_font(["arialbd.ttf", "impact.ttf"], int(ph * 0.16))
    
    pdraw.text((pw // 2, int(ph * 0.24)), "KC", fill=(212, 175, 55), font=f_kc, anchor="mm")
    pdraw.line([(pw * 0.15, int(ph * 0.44)), (pw * 0.85, int(ph * 0.44))], fill=(160, 125, 40), width=1)
    pdraw.text((pw // 2, int(ph * 0.58)), "KROW N  CONSTRUCTION", fill=(240, 240, 245), font=f_sub, anchor="mm")
    pdraw.text((pw // 2, int(ph * 0.78)), "BUILT TO REIGN • SINCE 2018", fill=(225, 185, 75), font=f_date, anchor="mm")
    
    # Slight tilt ~ -9 deg to match ribbed cuff fold
    patch_rot = patch.rotate(-9, expand=True, resample=Image.Resampling.BICUBIC)
    
    # Shadow
    psh = Image.new("RGBA", (patch_rot.width + 12, patch_rot.height + 12), (0, 0, 0, 0))
    ps_draw = ImageDraw.Draw(psh)
    ps_draw.ellipse([4, 6, patch_rot.width + 6, patch_rot.height + 6], fill=(0, 0, 0, 170))
    psh = psh.filter(ImageFilter.GaussianBlur(5))
    
    im.paste(psh, (px - 6, py - 4), psh)
    im.paste(patch_rot, (px, py), patch_rot)
    
    out_p = os.path.join(PUB_PRODUCTS, "krown-beanie-since-2018.jpg")
    im.convert("RGB").save(out_p, "JPEG", quality=96)
    print(f"-> Saved: {out_p}")


# -------------------------------------------------------------------------
# 6. JOGGERS V2: COLOR FILL INSIDE LETTERING DOWN PANT LEG
# -------------------------------------------------------------------------
def render_joggers_v2():
    print("6. Rendering Joggers V2: Solid Color Filled Lettering Down Pant Leg...")
    src = os.path.join(BRAIN_DIR, "axiom_pro_joggers_clean_1791592187560.jpg")
    if not os.path.exists(src):
        src = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-clean.jpg")
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    
    # Model's left leg runs down: x ~ 150-240, y ~ 360-580
    # Create vertical text strip with SOLID COLOR FILL inside letters:
    # Electric Lime (#39FF14) solid fill + Royal Purple (#8A2BE2) outer stroke/glow
    strip_w = 70
    strip_h = 360
    txt_strip = Image.new("RGBA", (strip_w, strip_h), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_strip)
    
    f_vert = get_font(["impact.ttf", "arialbd.ttf"], 26)
    letters = "AXIOM ALLEGIANCE"
    y_step = strip_h / len(letters)
    for i, ch in enumerate(letters):
        if ch == " ":
            continue
        yp = int(i * y_step + y_step / 2)
        # Royal purple outer stroke
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,1),(-1,1),(1,-1)]:
            t_draw.text((strip_w // 2 + dx, yp + dy), ch, fill=(138, 43, 226, 255), font=f_vert, anchor="mm")
        # Solid electric lime core fill
        t_draw.text((strip_w // 2, yp), ch, fill=(57, 255, 20, 255), font=f_vert, anchor="mm")
        
    # Rotate slightly to align with leg taper (-68 deg)
    txt_rot = txt_strip.rotate(-68, expand=True, resample=Image.Resampling.BICUBIC)
    
    # Dark shadow under text
    lx = int(w * 0.155)
    ly = int(h * 0.365)
    
    dark_mask = Image.new("RGBA", (txt_rot.width + 20, txt_rot.height + 20), (0, 0, 0, 0))
    dm_draw = ImageDraw.Draw(dark_mask)
    dm_draw.ellipse([0, 0, txt_rot.width + 20, txt_rot.height + 20], fill=(20, 20, 24, 240))
    dark_mask = dark_mask.filter(ImageFilter.GaussianBlur(8))
    im.paste(dark_mask, (lx - 10, ly - 10), dark_mask)
    im.paste(txt_rot, (lx, ly), txt_rot)
    
    # Also update thigh logo to smoky owl
    if owl_smokey:
        rx = int(w * 0.72)
        ry = int(h * 0.31)
        owl_zoom = owl_smokey.resize((int(w * 0.18), int(w * 0.18 * (owl_smokey.height / owl_smokey.width))), Image.Resampling.LANCZOS)
        im.paste(owl_zoom, (rx, ry), owl_zoom)
        
    out_p = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-v2.jpg")
    im.convert("RGB").save(out_p, "JPEG", quality=95)
    print(f"-> Saved: {out_p}")


# -------------------------------------------------------------------------
# 7. PHOTOREALISTIC CERAMIC GAMER MUG (NO BANNERS, NO PROMO TEXT)
# -------------------------------------------------------------------------
def render_photoreal_ceramic_mug_v2():
    print("7. Rendering Photoreal Ceramic Gamer Mug V2: Pure 3D Ceramic Desk Render...")
    W, H = 1024, 1024
    
    # Realistic dark battlestation studio surface
    canvas = Image.new("RGBA", (W, H), (14, 15, 18, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Soft background gradient
    for y in range(620):
        t = y / 620.0
        r = int(12 + 10 * (1.0 - t))
        g = int(13 + 8 * (1.0 - t))
        b = int(18 + 14 * (1.0 - t))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Table surface
    for y in range(620, H):
        t = (y - 620) / (H - 620)
        tr = int(22 + 12 * t)
        tg = int(23 + 10 * t)
        tb = int(26 + 10 * t)
        draw.line([(0, y), (W, y)], fill=(tr, tg, tb))
    draw.line([(0, 620), (W, 620)], fill=(38, 40, 48), width=2)
    
    # Mug Geometry
    cx, cy = 480, 520
    mw, mh = 420, 480
    
    # 1. Cast Floor Shadow
    f_sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fs_draw = ImageDraw.Draw(f_sh)
    fs_draw.ellipse([cx - mw//2 - 40, cy + mh//2 - 20, cx + mw//2 + 90, cy + mh//2 + 65], fill=(0, 0, 0, 210))
    f_sh = f_sh.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, f_sh)
    draw = ImageDraw.Draw(canvas)
    
    # 2. Ceramic Handle (Vibrant Electric Lime Glaze with glossy shine)
    hw, hh = 160, 260
    hx = cx + mw//2 - 30
    hy = cy - 20
    
    handle = Image.new("RGBA", (hw, hh), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(handle)
    h_draw.ellipse([0, 0, hw, hh], fill=(45, 215, 20, 255), outline=(30, 160, 15), width=4)
    h_draw.ellipse([34, 38, hw - 34, hh - 38], fill=(0, 0, 0, 0))
    
    # Handle specular reflection
    h_spec = Image.new("RGBA", (hw, hh), (0, 0, 0, 0))
    hs_draw = ImageDraw.Draw(h_spec)
    hs_draw.arc([10, 10, hw - 10, hh - 10], start=280, end=70, fill=(180, 255, 160, 180), width=6)
    h_spec = h_spec.filter(ImageFilter.GaussianBlur(2))
    handle = Image.alpha_composite(handle, h_spec)
    
    canvas.paste(handle, (hx, hy), handle)
    
    # 3. Main Ceramic Cylinder Body (Glossy Obsidian Ceramic)
    body = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(body)
    
    # Cylinder curvature lighting (Glossy dark ceramic)
    for x in range(mw):
        t = x / float(mw)
        # Specular highlight on left third (x ~ 0.25)
        spec = math.exp(-((t - 0.28) ** 2) / 0.015)
        rim = math.exp(-((t - 0.95) ** 2) / 0.02)
        
        base_v = 18 + 12 * math.sin(t * math.pi)
        r = int(min(255, base_v + spec * 75 + rim * 30))
        g = int(min(255, base_v + spec * 75 + rim * 35))
        b = int(min(255, base_v + 4 + spec * 85 + rim * 45))
        b_draw.line([(x, 30), (x, mh - 30)], fill=(r, g, b, 255))
        
    # Top rim & bottom rim rounded caps
    b_draw.ellipse([0, mh - 60, mw, mh], fill=(22, 23, 28, 255))
    
    # 4. Ceramic Glaze Interior (Electric Lime Interior Glaze)
    interior = Image.new("RGBA", (mw, 70), (0, 0, 0, 0))
    in_draw = ImageDraw.Draw(interior)
    in_draw.ellipse([0, 0, mw, 70], fill=(42, 205, 18, 255), outline=(35, 175, 15), width=3)
    # Dark cavity depth inside mug
    in_draw.ellipse([8, 12, mw - 8, 64], fill=(25, 120, 12, 255))
    
    # 5. Composite Owl & Gothic Branding onto Cylinder Face
    if owl_smokey:
        target_ow = int(mw * 0.46)
        target_oh = int(owl_smokey.height * (target_ow / owl_smokey.width))
        o_res = owl_smokey.resize((target_ow, target_oh), Image.Resampling.LANCZOS)
        body.paste(o_res, ((mw - target_ow) // 2 - 10, int(mh * 0.24)), o_res)
        
    # Two-tone text under owl
    f_motto = get_font(["arialbd.ttf"], 12)
    b_draw.text((mw // 2 - 10, int(mh * 0.76)), "AXIOM ALLEGIANCE", fill=(57, 255, 20), font=get_font(["impact.ttf"], 22), anchor="mm")
    b_draw.text((mw // 2 - 10, int(mh * 0.83)), "PRO ESPORTS DRINKWARE", fill=(160, 160, 175), font=f_motto, anchor="mm")
    
    canvas.paste(body, (cx - mw // 2, cy - mh // 2), body)
    canvas.paste(interior, (cx - mw // 2, cy - mh // 2), interior)
    
    out_p = os.path.join(PUB_PRODUCTS, "axiom-mug-clean-photoreal-15oz.jpg")
    canvas.convert("RGB").save(out_p, "JPEG", quality=96)
    print(f"-> Saved: {out_p}")


# -------------------------------------------------------------------------
# 8. SHAKERS V2: HIGH-AESTHETIC PHOTOREALISTIC RENDERS (KROW N & KC)
# -------------------------------------------------------------------------
def render_shakers_v2():
    print("8. Rendering Commercial-Grade Photorealistic Shakers V2...")
    W, H = 1024, 1024
    
    # We will render the 2 primary flagship bottles with realistic studio backdrop & lighting:
    # 1. KrowN Supply Co. Luxury Shaker (Matte Obsidian Black & Faceted Gold Crown)
    # 2. KrowN Construction Heavy-Duty Shaker (High-Vis Safety Gold & Industrial KC Seal)
    
    def render_bottle(brand_mode, out_filename):
        canvas = Image.new("RGBA", (W, H), (14, 15, 18, 255))
        draw = ImageDraw.Draw(canvas)
        
        # Studio tabletop
        for y in range(680, H):
            t = (y - 680) / (H - 680)
            c = int(22 + 10 * t)
            draw.line([(0, y), (W, y)], fill=(c, c, c + 4))
        draw.line([(0, 680), (W, 680)], fill=(36, 38, 45), width=2)
        
        bx, by = 512, 490
        bw, bh = 290, 560
        
        # Floor shadow
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(sh)
        sdraw.ellipse([bx - bw//2 - 25, by + bh//2 - 15, bx + bw//2 + 35, by + bh//2 + 45], fill=(0, 0, 0, 200))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        canvas = Image.alpha_composite(canvas, sh)
        
        # Bottle Cylinder Body
        bottle = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(bottle)
        
        # Tapered shaker body
        base_col = (18, 19, 23) if brand_mode == "krown" else (24, 25, 28)
        for x in range(bw):
            t = x / float(bw)
            spec = math.exp(-((t - 0.30) ** 2) / 0.02)
            glow = math.sin(t * math.pi)
            
            r = int(min(255, base_col[0] * glow + spec * 60))
            g = int(min(255, base_col[1] * glow + spec * 60))
            b = int(min(255, base_col[2] * glow + spec * 70))
            bdraw.line([(x, 100), (x, bh - 20)], fill=(r, g, b, 255))
            
        bdraw.ellipse([0, bh - 40, bw, bh], fill=(base_col[0] + 10, base_col[1] + 10, base_col[2] + 12, 255))
        
        # Cap & Lid Assembly
        # Spout cap & loop ring
        cap_h = 130
        lid_col = (28, 29, 34) if brand_mode == "krown" else (226, 179, 78) # Safety gold for KC
        bdraw.rounded_rectangle([25, 30, bw - 25, 110], radius=14, fill=lid_col, outline=(50, 52, 60), width=2)
        # Flip cap spout
        bdraw.rounded_rectangle([bw//2 - 35, 8, bw//2 + 35, 45], radius=8, fill=(18, 19, 22), outline=(212, 175, 55) if brand_mode == "krown" else (245, 205, 90), width=2)
        # Carry loop
        bdraw.arc([bw - 75, 10, bw - 15, 75], start=270, end=90, fill=(80, 85, 95) if brand_mode == "krown" else (226, 179, 78), width=8)
        
        # Brand Emblem onto Body
        if brand_mode == "krown":
            # Authentic faceted gold crown emblem + clean minimalist KrowN Supply Co text
            if krown_gold_crest:
                cw = 110
                ch = int(krown_gold_crest.height * (cw / krown_gold_crest.width))
                c_res = krown_gold_crest.resize((cw, ch), Image.Resampling.LANCZOS)
                bottle.paste(c_res, ((bw - cw) // 2, int(bh * 0.32)), c_res)
                
            f_brand = get_font(["impact.ttf", "arialbd.ttf"], 22)
            f_sub = get_font(["arialbd.ttf"], 10)
            f_motto = get_font(["arialbd.ttf"], 9)
            
            bdraw.text((bw // 2, int(bh * 0.59)), "K R O W N", fill=(212, 175, 55), font=f_brand, anchor="mm")
            bdraw.text((bw // 2, int(bh * 0.65)), "SUPPLY CO.", fill=(230, 230, 235), font=f_sub, anchor="mm")
            bdraw.line([(bw * 0.25, int(bh * 0.70)), (bw * 0.75, int(bh * 0.70))], fill=(160, 130, 45), width=1)
            bdraw.text((bw // 2, int(bh * 0.75)), "WEAR THE KROWN", fill=(212, 175, 55), font=f_motto, anchor="mm")
            bdraw.text((bw // 2, int(bh * 0.82)), "26 OZ PRO INSULATED STEEL", fill=(140, 145, 160), font=get_font(["arial.ttf"], 8), anchor="mm")
            
        else:
            # KrowN Construction Industrial Hex Seal
            hw = 140
            hh = 160
            hex_pts = [
                (bw//2, int(bh * 0.30)),
                (bw//2 + hw//2, int(bh * 0.36)),
                (bw//2 + hw//2, int(bh * 0.50)),
                (bw//2, int(bh * 0.56)),
                (bw//2 - hw//2, int(bh * 0.50)),
                (bw//2 - hw//2, int(bh * 0.36)),
            ]
            bdraw.polygon(hex_pts, fill=(18, 19, 23), outline=(226, 179, 78), width=3)
            
            f_kc = get_font(["impact.ttf", "arialbd.ttf"], 36)
            f_kc_sub = get_font(["arialbd.ttf"], 10)
            bdraw.text((bw // 2, int(bh * 0.41)), "KC", fill=(226, 179, 78), font=f_kc, anchor="mm")
            bdraw.text((bw // 2, int(bh * 0.49)), "BUILT TO REIGN", fill=(245, 245, 250), font=f_kc_sub, anchor="mm")
            
            bdraw.text((bw // 2, int(bh * 0.64)), "KROW N", fill=(226, 179, 78), font=get_font(["impact.ttf"], 22), anchor="mm")
            bdraw.text((bw // 2, int(bh * 0.70)), "CONSTRUCTION LLC", fill=(220, 220, 230), font=get_font(["arialbd.ttf"], 9), anchor="mm")
            bdraw.text((bw // 2, int(bh * 0.77)), "HEAVY-DUTY JOBSITE SERIES", fill=(150, 155, 170), font=get_font(["arial.ttf"], 8), anchor="mm")
            
        canvas.paste(bottle, (bx - bw // 2, by - bh // 2), bottle)
        
        out_p = os.path.join(PUB_PRODUCTS, out_filename)
        canvas.convert("RGB").save(out_p, "JPEG", quality=96)
        print(f"-> Saved: {out_p}")
        
    render_bottle("krown", "krown-shaker-obsidian-steel-v2.jpg")
    render_bottle("construction", "kc-shaker-highvis-steel-v2.jpg")


# Execute all renders
render_shorts_v2()
render_axiom_dad_hat_v2()
render_axiom_model_lookbook_v2()
render_streetwear_set_v2()
render_beanie_v2()
render_joggers_v2()
render_photoreal_ceramic_mug_v2()
render_shakers_v2()

print("\nAll master assets successfully rendered!")
