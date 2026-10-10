import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUB_BRANDING = os.path.join(BASE_DIR, "public", "images", "branding")
GAMING_DIR = os.path.join(PUB_BRANDING, "gaming")
BRAIN_DIR = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7"

os.makedirs(PUB_PRODUCTS, exist_ok=True)

def get_font(name_list, size):
    for n in name_list:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()

# Load Official Assets
owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-green-eyes-clean.png")
if not os.path.exists(owl_smokey_path):
    owl_smokey_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-clean-alpha.png")
owl_smokey = Image.open(owl_smokey_path).convert("RGBA")

gothic_two_tone_path = os.path.join(GAMING_DIR, "axiom-two-tone-gothic-clean-alpha.png")
gothic_two_tone = Image.open(gothic_two_tone_path).convert("RGBA")

# -------------------------------------------------------------------------
# 1. REDESIGN AXIOM ALLEGIANCE HEAVYWEIGHT 450 GSM STREETWEAR HOODIE (STUDIO)
# -------------------------------------------------------------------------
def redesign_axiom_hoodie_studio():
    print("1. Redesigning Axiom Allegiance Heavyweight 450 GSM Hoodie Studio...")
    base_path = os.path.join(BRAIN_DIR, "axiom_hoodie_studio_front_1791592242763.jpg")
    im = Image.open(base_path).convert("RGBA")
    w, h = im.size

    # --- A. CHEST MASCOT: High-Density Direct Embroidery of Smokey Owl ---
    # Center on chest: cx = w // 2 (512), cy = int(h * 0.43) (440)
    target_ow = int(w * 0.30)
    target_oh = int(owl_smokey.height * (target_ow / owl_smokey.width))
    owl_res = owl_smokey.resize((target_ow, target_oh), Image.Resampling.LANCZOS)
    
    cx = w // 2
    cy = int(h * 0.43)

    # Soft dark French Terry underlay to cleanly replace any underlying print
    underlay = Image.new("RGBA", (target_ow + 50, target_oh + 50), (0, 0, 0, 0))
    u_draw = ImageDraw.Draw(underlay)
    u_draw.ellipse([0, 0, target_ow + 50, target_oh + 50], fill=(16, 17, 21, 250))
    underlay = underlay.filter(ImageFilter.GaussianBlur(12))
    im.paste(underlay, (cx - (target_ow + 50) // 2, cy - (target_oh + 50) // 2), underlay)

    # Subtle 3D embroidery shadow for depth
    owl_shadow = Image.new("RGBA", (target_ow + 20, target_oh + 20), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(owl_shadow)
    s_draw.bitmap((10, 14), owl_res.split()[3], fill=(0, 0, 0, 160))
    owl_shadow = owl_shadow.filter(ImageFilter.GaussianBlur(6))
    im.paste(owl_shadow, (cx - target_ow // 2 - 10, cy - target_oh // 2 - 10), owl_shadow)

    # Paste official glowing green-eyed owl crest
    im.paste(owl_res, (cx - target_ow // 2, cy - target_oh // 2), owl_res)

    # --- B. DUAL-TONE BRAIDED CORDS (ROYAL PURPLE & TOXIC NEON GREEN) ---
    # Collar eyelets are at roughly (470, 240) and (554, 240)
    # Left cord (viewer's left): Royal Purple core (#8A2BE2) with toxic green spirals
    # Right cord (viewer's right): Toxic Green core (#39FF14) with royal purple spirals
    cords_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(cords_layer)

    def draw_braided_cord(start_xy, end_xy, primary_color, secondary_color, control_pts):
        # Generate bezier / natural curve points
        pts = []
        n_steps = 140
        for i in range(n_steps + 1):
            t = i / float(n_steps)
            # Quadratic or cubic bezier
            p0 = start_xy
            p1 = control_pts[0]
            p2 = control_pts[1]
            p3 = end_xy
            # Cubic bezier
            x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
            pts.append((x, y))

        # Cord shadow underneath
        sh_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(sh_layer)
        for i in range(len(pts) - 1):
            sh_draw.line([(pts[i][0] + 4, pts[i][1] + 8), (pts[i+1][0] + 4, pts[i+1][1] + 8)], fill=(0, 0, 0, 140), width=9)
        sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(5))
        nonlocal im
        im = Image.alpha_composite(im, sh_layer)

        # Draw braided segments
        cord_width = 8
        for i in range(len(pts) - 1):
            p_curr = pts[i]
            p_next = pts[i+1]
            
            # Alternate primary and secondary spiral colors to simulate tight braiding
            segment_idx = (i // 3) % 2
            col = primary_color if segment_idx == 0 else secondary_color
            
            # Subtle 3D cylindrical shading
            c_draw.line([p_curr, p_next], fill=col, width=cord_width)

        # Draw sleek cylindrical matte gunmetal metallic aglet at cord tip
        tip_x, tip_y = pts[-1]
        aglet_h = 32
        aglet_w = 9
        c_draw.rounded_rectangle([tip_x - aglet_w//2, tip_y - aglet_h, tip_x + aglet_w//2, tip_y], radius=3, fill=(58, 60, 66), outline=(32, 33, 38), width=1)
        # Specular highlight on metal aglet
        c_draw.line([(tip_x - 1, tip_y - aglet_h + 3), (tip_x - 1, tip_y - 3)], fill=(180, 185, 195, 200), width=2)
        # Dual engraved accent rings on aglet
        c_draw.line([(tip_x - aglet_w//2 + 1, tip_y - 22), (tip_x + aglet_w//2 - 1, tip_y - 22)], fill=(20, 22, 25), width=2)
        c_draw.line([(tip_x - aglet_w//2 + 1, tip_y - 12), (tip_x + aglet_w//2 - 1, tip_y - 12)], fill=(20, 22, 25), width=2)

    # Draw left cord: start near eyelet (476, 235), hang down with natural sway to (462, 490)
    draw_braided_cord(
        (476, 235),
        (462, 495),
        (138, 43, 226),   # Royal purple
        (57, 255, 20),    # Toxic neon green
        [(468, 310), (454, 410)]
    )

    # Draw right cord: start near eyelet (548, 235), hang down with natural sway to (560, 485)
    draw_braided_cord(
        (548, 235),
        (560, 490),
        (57, 255, 20),    # Toxic neon green
        (138, 43, 226),   # Royal purple
        [(556, 310), (568, 410)]
    )

    im = Image.alpha_composite(im, cords_layer)

    # --- C. SLEEVE GRAPHIC: Gothic Two-Tone "AXIOM ALLEGIANCE" down Left Forearm ---
    # Forearm on viewer's left: x ~ 110 to 220, y ~ 440 to 760
    # The sleeve slopes downwards at angle ~ -65 deg
    sleeve_txt = gothic_two_tone.rotate(-66, expand=True, resample=Image.Resampling.BICUBIC)
    sl_w = int(w * 0.125)
    sl_h = int(sleeve_txt.height * (sl_w / sleeve_txt.width))
    sleeve_res = sleeve_txt.resize((sl_w, sl_h), Image.Resampling.LANCZOS)

    # Soft dark fabric underlay on sleeve
    sl_x = int(w * 0.128)
    sl_y = int(h * 0.445)
    
    sl_underlay = Image.new("RGBA", (sl_w + 30, sl_h + 30), (0, 0, 0, 0))
    slu_draw = ImageDraw.Draw(sl_underlay)
    slu_draw.ellipse([0, 0, sl_w + 30, sl_h + 30], fill=(16, 17, 21, 230))
    sl_underlay = sl_underlay.filter(ImageFilter.GaussianBlur(8))
    im.paste(sl_underlay, (sl_x - 15, sl_y - 15), sl_underlay)

    im.paste(sleeve_res, (sl_x, sl_y), sleeve_res)

    # Save cache-busted V2 file
    out_v2 = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-v2.jpg")
    im.convert("RGB").save(out_v2, "JPEG", quality=96, progressive=True)
    # Also save as base studio so both are updated
    out_std = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-studio.jpg")
    im.convert("RGB").save(out_std, "JPEG", quality=96, progressive=True)
    print(f"-> Successfully saved: {out_v2} and {out_std}")


# -------------------------------------------------------------------------
# 2. REDESIGN AXIOM HOODIE LOOKBOOK MODEL (V2)
# -------------------------------------------------------------------------
def redesign_axiom_hoodie_model():
    print("2. Redesigning Axiom Allegiance Hoodie Model Lookbook V2...")
    base_path = os.path.join(BRAIN_DIR, "axiom_hoodie_model_1791592259283.jpg")
    im = Image.open(base_path).convert("RGBA")
    w, h = im.size

    # Model chest crest (centered on model's chest at x ~ w*0.48, y ~ h*0.37)
    cx = int(w * 0.485)
    cy = int(h * 0.375)
    target_ow = int(w * 0.22)
    target_oh = int(owl_smokey.height * (target_ow / owl_smokey.width))
    owl_res = owl_smokey.resize((target_ow, target_oh), Image.Resampling.LANCZOS)

    # Soft dark underlay
    underlay = Image.new("RGBA", (target_ow + 30, target_oh + 30), (0, 0, 0, 0))
    u_draw = ImageDraw.Draw(underlay)
    u_draw.ellipse([0, 0, target_ow + 30, target_oh + 30], fill=(18, 18, 22, 240))
    underlay = underlay.filter(ImageFilter.GaussianBlur(8))
    im.paste(underlay, (cx - target_ow // 2 - 15, cy - target_oh // 2 - 15), underlay)

    im.paste(owl_res, (cx - target_ow // 2, cy - target_oh // 2), owl_res)

    # Sleeve on model's right arm (viewer's left: x ~ w*0.22 to w*0.32, y ~ h*0.42 to h*0.62)
    sleeve_txt = gothic_two_tone.rotate(-54, expand=True, resample=Image.Resampling.BICUBIC)
    sl_w = int(w * 0.095)
    sl_h = int(sleeve_txt.height * (sl_w / sleeve_txt.width))
    sleeve_res = sleeve_txt.resize((sl_w, sl_h), Image.Resampling.LANCZOS)

    sl_x = int(w * 0.225)
    sl_y = int(h * 0.435)
    im.paste(sleeve_res, (sl_x, sl_y), sleeve_res)

    out_v2 = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-model-v2.jpg")
    im.convert("RGB").save(out_v2, "JPEG", quality=96, progressive=True)
    out_std = os.path.join(PUB_PRODUCTS, "axiom-heavyweight-hoodie-model.jpg")
    im.convert("RGB").save(out_std, "JPEG", quality=96, progressive=True)
    print(f"-> Successfully saved: {out_v2} and {out_std}")


# -------------------------------------------------------------------------
# 3. FIX SWEATPANTS THUMBNAIL (V3): ZERO BLACK BLOBS, NATURAL FABRIC COLORIZATION
# -------------------------------------------------------------------------
def redesign_joggers_model_v3():
    print("3. Redesigning Joggers Model V3: Clean Natural Fabric Colorization (No Black Blobs!)...")
    src = os.path.join(BRAIN_DIR, "axiom_pro_joggers_clean_1791592187560.jpg")
    im = Image.open(src).convert("RGB")
    arr = np.array(im).astype(float)

    # The lettering on the model's left calf is in region:
    # y: 340 to 600, x: 120 to 270
    leg_y0, leg_y1 = 340, 600
    leg_x0, leg_x1 = 120, 270

    leg_crop = arr[leg_y0:leg_y1, leg_x0:leg_x1]
    lum = leg_crop.mean(axis=2)

    # The fabric is dark (< 45), while the lettering is bright white (> 65)
    # Extract smooth mask of the lettering
    mask = np.clip((lum - 58.0) / 95.0, 0.0, 1.0)

    # Colorize the letters with team colors:
    # Vibrant Electric Lime (#39FF14: 57, 255, 20) with Royal Purple edge (#8A2BE2: 138, 43, 226)
    colorized = np.zeros_like(leg_crop)
    for y in range(leg_crop.shape[0]):
        colorized[y, :, 0] = 52.0   # R
        colorized[y, :, 1] = 240.0  # G (toxic lime)
        colorized[y, :, 2] = 28.0   # B

    # Preserve natural fabric folds, creases, and light shading
    shading = lum / 185.0
    shading = np.clip(shading, 0.45, 1.15)

    blended_leg = leg_crop * (1.0 - mask[:, :, None]) + colorized * mask[:, :, None] * shading[:, :, None]
    arr[leg_y0:leg_y1, leg_x0:leg_x1] = blended_leg

    res_im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

    # Composite official smoky owl on right thigh zoom panel (x ~ 730, y ~ 315)
    if owl_smokey:
        w, h = res_im.size
        target_ow = int(w * 0.18)
        target_oh = int(owl_smokey.height * (target_ow / owl_smokey.width))
        owl_zoom = owl_smokey.resize((target_ow, target_oh), Image.Resampling.LANCZOS)
        
        rx = int(w * 0.72)
        ry = int(h * 0.31)
        res_im.paste(owl_zoom, (rx, ry), owl_zoom)

    out_v3 = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-v3.jpg")
    res_im.convert("RGB").save(out_v3, "JPEG", quality=96, progressive=True)
    out_v2 = os.path.join(PUB_PRODUCTS, "axiom-sweatpants-pro-model-v2.jpg")
    res_im.convert("RGB").save(out_v2, "JPEG", quality=96, progressive=True)
    print(f"-> Successfully saved: {out_v3} and {out_v2}")


# -------------------------------------------------------------------------
# 4. COPY & CACHE-BUST OTHER KEY PRODUCTS (-v2)
# -------------------------------------------------------------------------
def cache_bust_remaining_flagships():
    print("4. Cache-busting Wrist Rest, Work Shirts, and Stickers...")
    import shutil
    
    # Wrist rest
    src_wr = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-tournament-edition.jpg")
    dst_wr = os.path.join(PUB_PRODUCTS, "axiom-keyboard-wrist-rest-tournament-edition-v2.jpg")
    if os.path.exists(src_wr):
        shutil.copy2(src_wr, dst_wr)
        print(f"-> Created {dst_wr}")

    # Work shirts
    for name in ["kc-work-shirt-grey-front", "kc-work-shirt-black-front", "kc-work-shirt-charcoal-back", "kc-work-shirt-model"]:
        s = os.path.join(PUB_PRODUCTS, f"{name}.jpg")
        d = os.path.join(PUB_PRODUCTS, f"{name}-v2.jpg")
        if os.path.exists(s):
            shutil.copy2(s, d)
            print(f"-> Created {d}")

    # Stickers
    src_st = os.path.join(PUB_PRODUCTS, "krown-stickers-realistic.jpg")
    dst_st = os.path.join(PUB_PRODUCTS, "kc-stickers-workbench-v2.jpg")
    if os.path.exists(src_st):
        shutil.copy2(src_st, dst_st)
        print(f"-> Created {dst_st}")

if __name__ == "__main__":
    redesign_axiom_hoodie_studio()
    redesign_axiom_hoodie_model()
    redesign_joggers_model_v3()
    cache_bust_remaining_flagships()
    print("\nAll redesigns and cache-busted flagships complete!")
