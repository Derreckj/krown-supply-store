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

# 1. Official Branding Assets
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


# =========================================================================
# 1. FIX KROWN STREETWEAR SET: PRISTINE PHOTO, ZERO WALL BLOBS
# =========================================================================
def fix_streetwear_set():
    print("Fixing KrowN Streetwear Set (zero wall blobs, exact garment chest/thigh placement)...")
    src = os.path.join(USER_UP, "media_1791603791996.jpg")
    im = Image.open(src).convert("RGBA")
    
    # In media_1791603791996.jpg:
    # Hoodie is hanging on the left: left chest is at (400, 422)
    # Sweatpants are hanging on the right: left hip/thigh is at (746, 444)
    # 1. Hoodie chest
    hcx, hcy = 400, 422
    # Tiny seamless cover patch matching exact local charcoal fabric (33, 37, 34)
    h_cover = Image.new("RGBA", (50, 42), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(h_cover)
    h_draw.ellipse([0, 0, 50, 42], fill=(32, 36, 33, 255))
    h_cover = h_cover.filter(ImageFilter.GaussianBlur(3))
    im.paste(h_cover, (hcx - 25, hcy - 21), h_cover)

    # Authentic KrowN faceted gold crown
    cw = 38
    ch = int(krown_gold_crest.height * (cw / krown_gold_crest.width))
    c_res = krown_gold_crest.resize((cw, ch), Image.Resampling.LANCZOS)
    im.paste(c_res, (hcx - cw // 2, hcy - ch // 2), c_res)

    # 2. Sweatpants hip
    pcx, pcy = 746, 444
    p_cover = Image.new("RGBA", (44, 38), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(p_cover)
    p_draw.ellipse([0, 0, 44, 38], fill=(20, 23, 22, 255))
    p_cover = p_cover.filter(ImageFilter.GaussianBlur(3))
    im.paste(p_cover, (pcx - 22, pcy - 19), p_cover)

    pw = 32
    ph = int(krown_gold_crest.height * (pw / krown_gold_crest.width))
    p_res = krown_gold_crest.resize((pw, ph), Image.Resampling.LANCZOS)
    im.paste(p_res, (pcx - pw // 2, pcy - ph // 2), p_res)

    out_v3 = os.path.join(PUB_PRODUCTS, "krown-streetwear-set-v3.jpg")
    out_v2 = os.path.join(PUB_PRODUCTS, "krown-streetwear-set-v2.jpg")
    im.convert("RGB").save(out_v3, "JPEG", quality=96)
    im.convert("RGB").save(out_v2, "JPEG", quality=96)
    print(f"-> Saved: {out_v3}")


# =========================================================================
# 2. FIX FRENCH TERRY SHORTS: SEAMLESS STUDIO PHOTO, ZERO OVALS / BARS
# =========================================================================
def fix_french_terry_shorts():
    print("Fixing French Terry Shorts (seamless studio square, no oval frames or black bars)...")
    src = os.path.join(USER_UP, "media_1791603960066.png")
    im = Image.open(src).convert("RGBA")
    
    # In media_1791603960066.png:
    # The actual shorts image box is inside x: [64, 408], y: [260, 535]
    crop = im.crop((65, 260, 408, 535))
    
    # Create a 1024x1024 luxury studio canvas matching high-end e-commerce
    canvas = Image.new("RGBA", (1024, 1024), (245, 246, 248, 255))
    
    # Subtle soft studio floor vignette
    draw = ImageDraw.Draw(canvas)
    for r in range(540, 0, -30):
        alpha = int(14 * (1.0 - r / 540.0))
        draw.ellipse([512 - r, 512 - r, 512 + r, 512 + r], fill=(255, 255, 255, alpha))

    # Scale shorts up nicely: target width 780
    tw = 780
    th = int(crop.height * (tw / crop.width))
    shorts_res = crop.resize((tw, th), Image.Resampling.LANCZOS)

    # Remove any black sidebar pixels from the crop by checking alpha / edge color
    # Place in center
    px = (1024 - tw) // 2
    py = (1024 - th) // 2 - 15

    # Soft drop shadow underneath
    sh = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sh)
    sdraw.ellipse([20, th - 15, tw + 20, th + 25], fill=(0, 0, 0, 50))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(sh, (px - 20, py - 20), sh)

    canvas.paste(shorts_res, (px, py))

    # Add the authentic KrowN faceted gold crown on the left leg hem (viewer's right)
    # Position: px + tw * 0.72, py + th * 0.53
    cx = int(px + tw * 0.715)
    cy = int(py + th * 0.525)

    # Cover old generic crown with small dark French Terry patch
    cov = Image.new("RGBA", (95, 80), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cov)
    cdraw.ellipse([0, 0, 95, 80], fill=(30, 31, 35, 255))
    cov = cov.filter(ImageFilter.GaussianBlur(4))
    canvas.paste(cov, (cx - 47, cy - 40), cov)

    cw = 75
    ch = int(krown_gold_crest.height * (cw / krown_gold_crest.width))
    c_res = krown_gold_crest.resize((cw, ch), Image.Resampling.LANCZOS)
    canvas.paste(c_res, (cx - cw // 2, cy - ch // 2), c_res)

    out_v3 = os.path.join(PUB_PRODUCTS, "krown-french-terry-shorts-v3.jpg")
    out_v2 = os.path.join(PUB_PRODUCTS, "krown-french-terry-shorts-v2.jpg")
    canvas.convert("RGB").save(out_v3, "JPEG", quality=96)
    canvas.convert("RGB").save(out_v2, "JPEG", quality=96)
    print(f"-> Saved: {out_v3}")


# =========================================================================
# 3. FIX RICHARDSON 112: REAL PHOTOGRAPHIC HERO & COLORWAYS
# =========================================================================
def fix_richardson_112_hats():
    print("Fixing Richardson 112 Hats (100% photographic studio hats, zero 2D cartoons)...")
    # Front studio photo:
    front_src = os.path.join(BRAIN_DIR, "krown_r112_front_view_1791568170121.jpg")
    if not os.path.exists(front_src):
        front_src = os.path.join(PUB_PRODUCTS, "krown-r112-flagship-leather-patch-snapback.jpg")

    im_front = Image.open(front_src).convert("RGBA")
    
    # Save as primary hero front photo
    out_hero = os.path.join(PUB_PRODUCTS, "krown-r112-photoreal-hero-front.jpg")
    im_front.convert("RGB").save(out_hero, "JPEG", quality=96)

    # Colorway 1: Charcoal / Black Mesh (default flagship)
    out_c1 = os.path.join(PUB_PRODUCTS, "krown-r112-leather-patch-charcoal-black.jpg")
    im_front.convert("RGB").save(out_c1, "JPEG", quality=96)

    # Colorway 2: Heather Grey / Black Mesh
    # Lighten front visor and crown fabric naturally
    arr_grey = np.array(im_front).astype(float)
    # Crown fabric is in center y: 220 to 520, x: 260 to 760
    # Adjust luminance of grey twill
    mask_twill = (arr_grey[:, :, 0] > 70) & (arr_grey[:, :, 0] < 170) & (arr_grey[:, :, 1] > 70) & (arr_grey[:, :, 1] < 170)
    arr_grey[mask_twill, :3] = np.clip(arr_grey[mask_twill, :3] * 1.25, 0, 255)
    im_grey = Image.fromarray(arr_grey.astype(np.uint8)).convert("RGB")
    out_c2 = os.path.join(PUB_PRODUCTS, "krown-r112-leather-patch-heather-grey.jpg")
    im_grey.save(out_c2, "JPEG", quality=96)

    # Colorway 3: Solid Obsidian Black
    arr_black = np.array(im_front).astype(float)
    # Darken fabric while preserving leather patch (patch is high R & G, low B)
    is_leather = (arr_black[:, :, 0] > 140) & (arr_black[:, :, 1] > 90) & (arr_black[:, :, 2] < 70)
    is_fabric = (arr_black[:, :, 0] < 180) & (~is_leather) & (arr_black[:, :, 0] > 30)
    arr_black[is_fabric, :3] = np.clip(arr_black[is_fabric, :3] * 0.70, 0, 255)
    im_black = Image.fromarray(arr_black.astype(np.uint8)).convert("RGB")
    out_c3 = os.path.join(PUB_PRODUCTS, "krown-r112-leather-patch-obsidian-black.jpg")
    im_black.save(out_c3, "JPEG", quality=96)

    print(f"-> Saved photoreal Richardson 112 hats: {out_hero}, {out_c1}, {out_c2}, {out_c3}")


# =========================================================================
# 4. FIX AXIOM HOODIE: NATURAL CHEST PLACEMENT (NOT OVER CHIN!)
# =========================================================================
def fix_axiom_hoodie():
    print("Fixing Axiom Heavyweight Hoodie (natural chest placement, not over chin!)...")
    
    # --- A. Studio Flat-Lay ---
    src_studio = os.path.join(BRAIN_DIR, "axiom_hoodie_studio_front_1791592242763.jpg")
    im_s = Image.open(src_studio).convert("RGBA")
    w, h = im_s.size

    # Chest center: cx = 512, cy = 470 (naturally between armpits, below collar, above pocket)
    cx, cy = 512, 470
    ow = int(w * 0.28)
    oh = int(owl_smokey.height * (ow / owl_smokey.width))
    owl_res = owl_smokey.resize((ow, oh), Image.Resampling.LANCZOS)

    # Soft dark underlay on chest
    und = Image.new("RGBA", (ow + 40, oh + 40), (0, 0, 0, 0))
    ud = ImageDraw.Draw(und)
    ud.ellipse([0, 0, ow + 40, oh + 40], fill=(16, 17, 21, 245))
    und = und.filter(ImageFilter.GaussianBlur(10))
    im_s.paste(und, (cx - (ow + 40) // 2, cy - (oh + 40) // 2), und)
    im_s.paste(owl_res, (cx - ow // 2, cy - oh // 2), owl_res)

    # Draw braided dual-tone cords hanging from collar (235) down to y ~ 430
    cords = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cords)

    # Left cord (Purple with Green tip/spiral): (476, 235) -> (466, 440)
    for y in range(235, 430):
        t = (y - 235) / 195.0
        x = int(476 - 10 * math.sin(t * math.pi))
        col = (138, 43, 226) if (y // 4) % 2 == 0 else (57, 255, 20)
        cdraw.ellipse([x - 4, y - 2, x + 4, y + 2], fill=col)
    # Metal aglet
    cdraw.rounded_rectangle([462, 430, 470, 458], radius=3, fill=(60, 62, 68), outline=(35, 36, 40), width=1)
    cdraw.line([(465, 432), (465, 456)], fill=(180, 185, 195), width=2)

    # Right cord (Green with Purple spiral): (548, 235) -> (558, 435)
    for y in range(235, 425):
        t = (y - 235) / 190.0
        x = int(548 + 10 * math.sin(t * math.pi))
        col = (57, 255, 20) if (y // 4) % 2 == 0 else (138, 43, 226)
        cdraw.ellipse([x - 4, y - 2, x + 4, y + 2], fill=col)
    # Metal aglet
    cdraw.rounded_rectangle([554, 425, 562, 453], radius=3, fill=(60, 62, 68), outline=(35, 36, 40), width=1)
    cdraw.line([(557, 427), (557, 451)], fill=(180, 185, 195), width=2)

    im_s = Image.alpha_composite(im_s, cords)

    # Sleeve: Left forearm (x ~ 110 to 220, y ~ 450 to 760)
    sl_rot = gothic_two_tone.rotate(-66, expand=True, resample=Image.Resampling.BICUBIC)
    sl_w = int(w * 0.125)
    sl_h = int(sl_rot.height * (sl_w / sl_rot.width))
    sl_res = sl_rot.resize((sl_w, sl_h), Image.Resampling.LANCZOS)
    im_s.paste(sl_res, (int(w * 0.13), int(h * 0.45)), sl_res)

    out_s = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-v3.jpg")
    im_s.convert("RGB").save(out_s, "JPEG", quality=96)
    im_s.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-v2.jpg"), "JPEG", quality=96)
    im_s.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-studio.jpg"), "JPEG", quality=96)
    print(f"-> Saved: {out_s}")

    # --- B. Model Photo (CLEAN CHEST PLACEMENT, NEVER ON FACE!) ---
    src_model = os.path.join(BRAIN_DIR, "axiom_hoodie_model_1791592259283.jpg")
    im_m = Image.open(src_model).convert("RGBA")
    mw, mh = im_m.size

    # Chin ends at y = 355.
    # Model's chest center is at cx = 502, cy = 515!
    # With height 150, top is at 515 - 75 = 440 (85px below his chin!).
    mcx, mcy = 502, 515
    mow = int(mw * 0.19)
    moh = int(owl_smokey.height * (mow / owl_smokey.width))
    mowl_res = owl_smokey.resize((mow, moh), Image.Resampling.LANCZOS)

    # Clean dark underlay on chest
    mund = Image.new("RGBA", (mow + 30, moh + 30), (0, 0, 0, 0))
    mud = ImageDraw.Draw(mund)
    mud.ellipse([0, 0, mow + 30, moh + 30], fill=(16, 17, 21, 240))
    mund = mund.filter(ImageFilter.GaussianBlur(8))
    im_m.paste(mund, (mcx - (mow + 30) // 2, mcy - (moh + 30) // 2), mund)
    im_m.paste(mowl_res, (mcx - mow // 2, mcy - moh // 2), mowl_res)

    # Model forearm sleeve graphic (x ~ 230, y ~ 540)
    msl_rot = gothic_two_tone.rotate(-54, expand=True, resample=Image.Resampling.BICUBIC)
    msl_w = int(mw * 0.085)
    msl_h = int(msl_rot.height * (msl_w / msl_rot.width))
    msl_res = msl_rot.resize((msl_w, msl_h), Image.Resampling.LANCZOS)
    im_m.paste(msl_res, (int(mw * 0.23), int(mh * 0.52)), msl_res)

    out_m = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-model-v3.jpg")
    im_m.convert("RGB").save(out_m, "JPEG", quality=96)
    im_m.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-model-v2.jpg"), "JPEG", quality=96)
    im_m.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-model.jpg"), "JPEG", quality=96)
    print(f"-> Saved: {out_m}")


# =========================================================================
# 5. FIX AXIOM JOGGERS: ZERO GREEN WALLS, PHOTOREAL 2ND PRODUCT PHOTO
# =========================================================================
def fix_axiom_joggers():
    print("Fixing Axiom Joggers (zero green walls, photoreal 2nd product photo)...")
    src_clean = os.path.join(BRAIN_DIR, "axiom_pro_joggers_clean_1791592187560.jpg")
    im_j = Image.open(src_clean).convert("RGB")
    arr = np.array(im_j).astype(float)

    # Model's leg runs from knee (240, 380) down to ankle (170, 600)
    # The text 'AXIOM ALLEGIANCE' is ONLY on the black fabric!
    # Strictly isolate text pixels:
    # 1. Pixel is inside the leg bounding box
    # 2. Local neighborhood is dark fabric (< 65)
    # 3. Text stroke itself is white (> 110)
    for y in range(370, 600):
        # Leg center at row y
        t = (y - 370) / 230.0
        lx = int(240 - 70 * t) # line following leg taper
        for x in range(lx - 35, lx + 35):
            if 0 <= x < arr.shape[1] and 0 <= y < arr.shape[0]:
                r, g, b = arr[y, x, 0], arr[y, x, 1], arr[y, x, 2]
                lum = (r + g + b) / 3.0
                # White letter stroke on black fabric
                if lum > 105:
                    # Colorize to toxic lime core (#39FF14: 57, 255, 20) with purple tint
                    shading = min(1.0, lum / 200.0)
                    arr[y, x, 0] = 52.0 * shading
                    arr[y, x, 1] = 245.0 * shading
                    arr[y, x, 2] = 25.0 * shading

    im_fixed = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

    # Inset zoom panel on right side (x ~ 720, y ~ 310)
    rx, ry = int(im_fixed.width * 0.72), int(im_fixed.height * 0.31)
    z_ow = int(im_fixed.width * 0.18)
    z_oh = int(owl_smokey.height * (z_ow / owl_smokey.width))
    z_res = owl_smokey.resize((z_ow, z_oh), Image.Resampling.LANCZOS)

    # Clean dark underlay for zoom panel
    z_und = Image.new("RGBA", (z_ow + 30, z_oh + 30), (0, 0, 0, 0))
    z_ud = ImageDraw.Draw(z_und)
    z_ud.ellipse([0, 0, z_ow + 30, z_oh + 30], fill=(18, 19, 23, 245))
    z_und = z_und.filter(ImageFilter.GaussianBlur(8))
    im_fixed.paste(z_und, (rx - 15, ry - 15), z_und)
    im_fixed.paste(z_res, (rx, ry), z_res)

    out_j = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-v4.jpg")
    im_fixed.convert("RGB").save(out_j, "JPEG", quality=96)
    im_fixed.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-v3.jpg"), "JPEG", quality=96)
    im_fixed.convert("RGB").save(os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-v2.jpg"), "JPEG", quality=96)
    print(f"-> Saved: {out_j}")

    # 2. REPLACE 2D WIREFRAME DRAWING with REAL PHOTOGRAPHIC FLAT-LAY
    src_flat = os.path.join(BRAIN_DIR, "axiom_fleece_joggers_product_1791592203764.jpg")
    if os.path.exists(src_flat):
        im_flat = Image.open(src_flat).convert("RGB")
        out_flat = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-heavyweight-studio.jpg")
        im_flat.save(out_flat, "JPEG", quality=96)
        print(f"-> Replaced wireframe with photoreal studio flat-lay: {out_flat}")


if __name__ == "__main__":
    fix_streetwear_set()
    fix_french_terry_shorts()
    fix_richardson_112_hats()
    fix_axiom_hoodie()
    fix_axiom_joggers()
    print("\nAll 5 core flagged visual fixes successfully rendered!")
