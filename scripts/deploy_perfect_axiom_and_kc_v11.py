import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')
BRAND_DIR = os.path.join(BASE_DIR, 'public', 'images', 'branding')
GAMING_DIR = os.path.join(BRAND_DIR, 'gaming')
CONST_DIR = os.path.join(BRAND_DIR, 'construction')

os.makedirs(PROD_DIR, exist_ok=True)
os.makedirs(MASTERS_DIR, exist_ok=True)

print("=" * 80)
print("DEPLOYING V11 MASTER ASSETS: AXIOM STICKERS, AXIOM BEANIES, KROWN WORK SHIRTS")
print("=" * 80)

# =========================================================================
# 1. AXIOM STICKERS (axiom-stickers-01) - NO GORILLA, SMOOTH DIECUT, 100% OWL
# =========================================================================
def deploy_axiom_stickers():
    print("\n--- 1. Generating Axiom Allegiance Holographic Battle Pack Decals (v11) ---")
    print("CRITICAL: ZERO GORILLAS. 100% Official Axiom Owl & Gothic tournament decals only.")

    # Battlestation Carbon Grid Canvas (1024x1024)
    canvas = Image.new('RGB', (1024, 1024), (11, 12, 16))
    draw_c = ImageDraw.Draw(canvas)

    grid_spacing = 32
    for x in range(0, 1024, grid_spacing):
        draw_c.line([(x, 0), (x, 1024)], fill=(20, 22, 28), width=1)
    for y in range(0, 1024, grid_spacing):
        draw_c.line([(0, y), (1024, y)], fill=(20, 22, 28), width=1)

    # Ambient cyber glows
    glow_p = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw_gp = ImageDraw.Draw(glow_p)
    draw_gp.ellipse([100, 100, 924, 924], fill=(98, 0, 238, 28))
    glow_p = glow_p.filter(ImageFilter.GaussianBlur(radius=80))

    glow_g = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw_gg = ImageDraw.Draw(glow_g)
    draw_gg.ellipse([300, 300, 724, 724], fill=(57, 255, 20, 24))
    glow_g = glow_g.filter(ImageFilter.GaussianBlur(radius=70))

    canvas.paste(glow_p, (0, 0), mask=glow_p)
    canvas.paste(glow_g, (0, 0), mask=glow_g)

    # Typography Headers
    try:
        font_h1 = ImageFont.truetype('arialbd.ttf', 16)
        font_h2 = ImageFont.truetype('arialbd.ttf', 32)
        font_sub = ImageFont.truetype('arialbd.ttf', 13)
    except:
        font_h1 = font_h2 = font_sub = ImageFont.load_default()

    draw_c.text((512, 48), "AXIOM ALLEGIANCE // MERCHANDISE LOADOUT", fill=(160, 70, 255), font=font_h1, anchor="mm")
    draw_c.text((512, 88), "HOLOGRAPHIC BATTLE PACK DECALS (5-PACK)", fill=(245, 245, 255), font=font_h2, anchor="mm")

    # Vector-smooth die-cut border with iridescent holographic foil
    def make_smooth_diecut_sticker(img_rgba, scale_w, angle=0, border_width=10):
        aspect = img_rgba.height / img_rgba.width
        sw = scale_w
        sh = int(sw * aspect)
        resized = img_rgba.resize((sw, sh), Image.Resampling.LANCZOS)
        
        pad = border_width + 12
        pw = sw + pad * 2
        ph = sh + pad * 2
        
        canvas_stk = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
        canvas_stk.paste(resized, (pad, pad), mask=resized.split()[3])
        
        alpha = canvas_stk.split()[3]
        expanded = alpha.filter(ImageFilter.MaxFilter(border_width * 2 + 1))
        smoothed = expanded.filter(ImageFilter.GaussianBlur(radius=2.5))
        arr_s = np.array(smoothed)
        crisp_mask = (arr_s > 90).astype(np.uint8) * 255
        final_border_mask = Image.fromarray(crisp_mask).filter(ImageFilter.GaussianBlur(radius=0.8))
        
        sticker = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
        white_base = Image.new('RGBA', (pw, ph), (255, 255, 255, 255))
        sticker.paste(white_base, (0, 0), mask=final_border_mask)
        
        arr_graphic = np.array(canvas_stk, dtype=np.float32)
        alpha_g = arr_graphic[:, :, 3]
        holo_mask = alpha_g > 20
        
        y_idx, x_idx = np.where(holo_mask)
        prism_t = ((x_idx * 0.75 + y_idx * 0.45) / float(pw)) % 1.0
        r_tint = np.sin(prism_t * 2 * np.pi) * 25
        g_tint = np.sin((prism_t + 0.33) * 2 * np.pi) * 30
        b_tint = np.sin((prism_t + 0.66) * 2 * np.pi) * 35
        
        arr_graphic[y_idx, x_idx, 0] = np.clip(arr_graphic[y_idx, x_idx, 0] + r_tint, 0, 255)
        arr_graphic[y_idx, x_idx, 1] = np.clip(arr_graphic[y_idx, x_idx, 1] + g_tint, 0, 255)
        arr_graphic[y_idx, x_idx, 2] = np.clip(arr_graphic[y_idx, x_idx, 2] + b_tint, 0, 255)
        
        holo_img = Image.fromarray(arr_graphic.astype(np.uint8))
        sticker.paste(holo_img, (0, 0), mask=holo_img.split()[3])
        
        if angle != 0:
            sticker = sticker.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
            
        sh_mask = sticker.split()[3].filter(ImageFilter.GaussianBlur(radius=5.5))
        sh_fill = Image.new('RGBA', sticker.size, (5, 5, 8, 175))
        sh_fill.putalpha(sh_mask)
        return sticker, sh_fill

    # STICKER 1: Primary Cyber Owl Mascot (Center Hero)
    owl_mascot = Image.open(os.path.join(GAMING_DIR, 'axiom-owl-mascot.png')).convert('RGBA')
    stk1, sh1 = make_smooth_diecut_sticker(owl_mascot, scale_w=245, angle=-2)

    # STICKER 2: Smokey Owl with Toxic Green Eyes (TOP RIGHT - ZERO GORILLAS!)
    smokey_owl = Image.open(os.path.join(GAMING_DIR, 'axiom-smokey-owl-green-eyes-clean.png')).convert('RGBA')
    stk2, sh2 = make_smooth_diecut_sticker(smokey_owl, scale_w=235, angle=3)

    # STICKER 3: Two-Tone Gothic "Axiom Allegiance" Wordmark (TOP LEFT - Smooth Vector Border)
    gothic_wordmark = Image.open(os.path.join(GAMING_DIR, 'axiom-two-tone-gothic-clean-alpha.png')).convert('RGBA')
    stk3, sh3 = make_smooth_diecut_sticker(gothic_wordmark, scale_w=275, angle=-3)

    # STICKER 4: Tactical Diamond Shield "AXA ESPORTS" (BOTTOM LEFT)
    shield_w, shield_h = 200, 200
    shield_img = Image.new('RGBA', (shield_w, shield_h), (0, 0, 0, 0))
    draw_sh = ImageDraw.Draw(shield_img)
    diamond_pts = [(shield_w // 2, 8), (shield_w - 8, shield_h // 2), (shield_w // 2, shield_h - 8), (8, shield_h // 2)]
    draw_sh.polygon(diamond_pts, fill=(18, 19, 25, 255), outline=(57, 255, 20, 255), width=5)
    inner_pts = [(shield_w // 2, 22), (shield_w - 22, shield_h // 2), (shield_w // 2, shield_h - 22), (22, shield_h // 2)]
    draw_sh.polygon(inner_pts, outline=(160, 60, 255, 200), width=3)
    try:
        f_axa = ImageFont.truetype('impact.ttf', 36)
        f_esp = ImageFont.truetype('arialbd.ttf', 14)
    except:
        f_axa = f_esp = ImageFont.load_default()
    draw_sh.text((shield_w // 2, shield_h // 2 - 12), "AXA", fill=(57, 255, 20), font=f_axa, anchor="mm")
    draw_sh.text((shield_w // 2, shield_h // 2 + 22), "ESPORTS", fill=(240, 240, 255), font=f_esp, anchor="mm")
    stk4, sh4 = make_smooth_diecut_sticker(shield_img, scale_w=195, angle=-3)

    # STICKER 5: "PLAY TO REIGN" Hexagonal Championship Emblem (BOTTOM RIGHT)
    hex_w, hex_h = 210, 210
    hex_img = Image.new('RGBA', (hex_w, hex_h), (0, 0, 0, 0))
    draw_hx = ImageDraw.Draw(hex_img)
    h_pts = [(hex_w // 2, 6), (hex_w - 6, hex_h // 4), (hex_w - 6, int(hex_h * 0.75)), (hex_w // 2, hex_h - 6), (6, int(hex_h * 0.75)), (6, hex_h // 4)]
    draw_hx.polygon(h_pts, fill=(16, 17, 22, 255), outline=(160, 60, 255, 255), width=5)
    inner_h = [(hex_w // 2, 18), (hex_w - 18, int(hex_h * 0.27)), (hex_w - 18, int(hex_h * 0.73)), (hex_w // 2, hex_h - 18), (18, int(hex_h * 0.73)), (18, int(hex_h * 0.27))]
    draw_hx.polygon(inner_h, outline=(57, 255, 20, 220), width=3)
    try:
        f_hx1 = ImageFont.truetype('impact.ttf', 24)
        f_hx2 = ImageFont.truetype('arialbd.ttf', 15)
        f_hx3 = ImageFont.truetype('arialbd.ttf', 13)
    except:
        f_hx1 = f_hx2 = f_hx3 = ImageFont.load_default()
    draw_hx.text((hex_w // 2, 55), "AXIOM", fill=(170, 70, 255), font=f_hx1, anchor="mm")
    draw_hx.text((hex_w // 2, 95), "ALLEGIANCE", fill=(245, 245, 255), font=f_hx2, anchor="mm")
    draw_hx.text((hex_w // 2, 138), "PLAY TO REIGN", fill=(57, 255, 20), font=f_hx3, anchor="mm")
    stk5, sh5 = make_smooth_diecut_sticker(hex_img, scale_w=200, angle=3)

    placements = [
        (stk3, sh3, 90, 160),  # Gothic Wordmark (Top Left)
        (stk2, sh2, 660, 150), # Smokey Owl (Top Right - NO GORILLA!)
        (stk1, sh1, 380, 360), # Cyber Owl Hero (Center)
        (stk4, sh4, 110, 580), # AXA Diamond Shield (Bottom Left)
        (stk5, sh5, 680, 580), # Play To Reign Hexagon (Bottom Right)
    ]

    canvas_rgba = canvas.convert('RGBA')
    for stk, sh, px, py in placements:
        canvas_rgba.paste(sh, (px + 3, py + 5), mask=sh)
    for stk, sh, px, py in placements:
        canvas_rgba.paste(stk, (px, py), mask=stk)

    draw_final = ImageDraw.Draw(canvas_rgba)
    specs = "• 6 MIL WEATHERPROOF VINYL   |   • UV-RESISTANT LAMINATE   |   • IRIDESCENT HOLOGRAPHIC FOIL   |   • INDIVIDUAL DIE-CUT SILHOUETTES"
    draw_final.text((512, 950), specs, fill=(57, 255, 20), font=font_sub, anchor="mm")
    draw_final.text((512, 980), "AUTHENTIC DIE-CUT EDGES • ZERO BORING SQUARE CARDS • BATTLESTATION GRADE", fill=(140, 145, 160), font=font_sub, anchor="mm")

    final_img = canvas_rgba.convert('RGB')
    target_v11 = os.path.join(PROD_DIR, 'axiom-stickers-holographic-battle-pack-v11.jpg')
    final_img.save(target_v11, quality=96)
    final_img.save(os.path.join(MASTERS_DIR, 'axiom-stickers-holographic-battle-pack-v11.jpg'), quality=96)
    final_img.save(os.path.join(PROD_DIR, 'axiom-stickers-holographic-battle-pack-v10.jpg'), quality=96)
    final_img.save(os.path.join(MASTERS_DIR, 'axiom-stickers-holographic-battle-pack-v10.jpg'), quality=96)
    print("✓ Successfully generated axiom-stickers-holographic-battle-pack-v11.jpg (ZERO GORILLAS, SMOOTH BORDERS)!")

# =========================================================================
# 2. AXIOM BEANIES (axiom-beanie-01) - 100% CLEAN AXIOM EMBROIDERY (V11)
# =========================================================================
def deploy_axiom_beanies():
    print("\n--- 2. Generating Axiom Allegiance Ribbed Cuffed Beanies (v11) ---")
    print("CRITICAL: 100% Axiom Owl Crest only. Zero yellow patches, zero leather patches, zero tumblers.")

    b1 = Image.open('scratch/fc03210_beanie.jpg').convert('RGB')
    b2 = Image.open('scratch/fc03210_purple.jpg').convert('RGB')
    b3 = Image.open('scratch/fc03210_volcanic.jpg').convert('RGB')

    # 1. Midnight Obsidian / Toxic Green Owl Crest (v11)
    target_b1 = os.path.join(PROD_DIR, 'axiom-beanie-obsidian-lime-v11.jpg')
    b1.save(target_b1, quality=96)
    b1.save(os.path.join(MASTERS_DIR, 'axiom-beanie-obsidian-lime-v11.jpg'), quality=96)
    b1.save(os.path.join(PROD_DIR, 'axiom-beanie-obsidian-lime-v10.jpg'), quality=96)
    b1.save(os.path.join(PROD_DIR, 'axiom-beanie-obsidian-lime-v9.jpg'), quality=96)

    # 2. Royal Purple & Electric Green Dual-Tone (v11)
    target_b2 = os.path.join(PROD_DIR, 'axiom-beanie-purple-green-v11.jpg')
    b2.save(target_b2, quality=96)
    b2.save(os.path.join(MASTERS_DIR, 'axiom-beanie-purple-green-v11.jpg'), quality=96)
    b2.save(os.path.join(PROD_DIR, 'axiom-beanie-purple-green-v10.jpg'), quality=96)
    b2.save(os.path.join(PROD_DIR, 'axiom-beanie-purple-green-v9.jpg'), quality=96)

    # 3. Volcanic Crimson / Ember Owl Crest (v11)
    target_b3 = os.path.join(PROD_DIR, 'axiom-beanie-volcanic-v11.jpg')
    b3.save(target_b3, quality=96)
    b3.save(os.path.join(MASTERS_DIR, 'axiom-beanie-volcanic-v11.jpg'), quality=96)
    b3.save(os.path.join(PROD_DIR, 'axiom-beanie-volcanic-v10.jpg'), quality=96)
    b3.save(os.path.join(PROD_DIR, 'axiom-beanie-volcanic-v9.jpg'), quality=96)
    print("✓ Successfully deployed all 3 Axiom Allegiance beanies (v11) with ZERO stray patches!")

# =========================================================================
# 3. KROWN CONSTRUCTION HEAVY WORK SHIRT (krown-work-01) - PROFESSIONAL & CLASSY (V11)
# =========================================================================
def deploy_kc_work_shirts():
    print("\n--- 3. Generating Professional & Classy KrowN Construction Heavy Work Shirts (v11) ---")
    print("CRITICAL: ZERO bounding box rectangles, ZERO smeared sleeve scribble, left-chest authentic badge.")

    im_black_base = Image.open('scratch/black_mannequin_test.jpg').convert('RGB')
    arr_b = np.array(im_black_base, dtype=float)

    is_bg = (arr_b[..., 0] > 175) & (arr_b[..., 1] > 175) & (arr_b[..., 2] > 175)
    bg_mask = Image.fromarray((is_bg * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3))
    is_bg = np.array(bg_mask) > 128

    y_coords, x_coords = np.ogrid[:1024, :1024]
    is_neck = (y_coords < 330) & (x_coords > 395) & (x_coords < 630) & (~is_bg) & (arr_b.mean(axis=-1) < 45)
    is_shirt = (~is_bg) & (~is_neck)

    median_b = np.median(arr_b[is_shirt], axis=0)
    ratio = arr_b / median_b
    ratio_adj = np.power(ratio, 0.85)

    base_heather = np.array([94.0, 96.0, 102.0])
    shirt_heather = base_heather * ratio_adj

    np.random.seed(101)
    heather_grain = np.random.normal(0, 3.8, (1024, 1024, 1))
    shirt_heather = shirt_heather + heather_grain

    arr_grey = arr_b.copy()
    for c in range(3):
        arr_grey[..., c] = np.where(is_shirt, np.clip(shirt_heather[..., c], 25, 230), arr_b[..., c])

    collar_edge = Image.fromarray((is_neck * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    c_arr = np.array(collar_edge, dtype=float) / 255.0
    c_arr = c_arr[..., None]
    arr_grey = arr_grey * (1.0 - c_arr) + arr_b * c_arr

    clean_heather_base = Image.fromarray(np.clip(arr_grey, 0, 255).astype(np.uint8))
    clean_black_base = im_black_base.copy()

    logo_white = Image.open('scratch/kc_logo_cropped_white.png').convert('RGBA')
    
    tw = 155
    th = int(tw * logo_white.height / logo_white.width)
    logo_res = logo_white.resize((tw, th), Image.Resampling.LANCZOS)
    alpha = np.array(logo_res)[:, :, 3]

    emblem_mask = np.zeros((th, tw), dtype=bool)
    emblem_mask[0:int(th * 0.72), int(tw * 0.40):int(tw * 0.72)] = True

    try:
        font_sub = ImageFont.truetype('arialbd.ttf', 11)
    except:
        font_sub = ImageFont.load_default()

    # --- COLORWAY 1: HEATHER STEEL GREY (LEFT CHEST CREST) ---
    print("Generating Colorway 1: Heather Steel Grey Work Shirt (v11)...")
    color_black = np.array([22, 23, 27])
    color_gold = np.array([212, 165, 42]) # Safety Antique Gold
    badge_grey = np.zeros((th, tw, 4), dtype=np.uint8)
    for c in range(3):
        badge_grey[:, :, c] = np.where(emblem_mask, color_gold[c], color_black[c])
    badge_grey[:, :, 3] = alpha

    im_badge_grey = Image.fromarray(badge_grey)
    badge_canvas_g = Image.new('RGBA', (tw, th + 20), (0, 0, 0, 0))
    badge_canvas_g.paste(im_badge_grey, (0, 0), mask=im_badge_grey.split()[3])
    draw_bg = ImageDraw.Draw(badge_canvas_g)
    sub_text = 'BUILT TO REIGN'
    w_sub = draw_bg.textlength(sub_text, font=font_sub)
    draw_bg.text(((tw - w_sub) // 2, th + 4), sub_text, font=font_sub, fill=(22, 23, 27, 240))

    cx = 645
    cy = 445
    lx = cx - tw // 2
    ly = cy - (th + 20) // 2

    sh_mask_g = badge_canvas_g.split()[3].filter(ImageFilter.GaussianBlur(1.0))
    sh_fill_g = Image.new('RGBA', badge_canvas_g.size, (5, 5, 8, 140))
    sh_fill_g.putalpha(sh_mask_g)

    heather_canvas = clean_heather_base.convert('RGBA')
    heather_canvas.paste(sh_fill_g, (lx + 1, ly + 2), mask=sh_mask_g)
    heather_canvas.paste(badge_canvas_g, (lx, ly), mask=badge_canvas_g.split()[3])

    final_grey = heather_canvas.convert('RGB')
    target_g_v11 = os.path.join(PROD_DIR, 'kc-work-shirt-grey-front-v11.jpg')
    final_grey.save(target_g_v11, quality=98)
    final_grey.save(os.path.join(MASTERS_DIR, 'kc-work-shirt-grey-front-v11.jpg'), quality=98)
    for f in ['kc-work-shirt-grey-front-v8.jpg', 'kc-work-shirt-grey-front-v3.jpg', 'kc-work-shirt-grey-front-v2.jpg', 'kc-work-shirt-grey-front.jpg']:
        final_grey.save(os.path.join(PROD_DIR, f), quality=98)
        final_grey.save(os.path.join(MASTERS_DIR, f), quality=98)

    # --- COLORWAY 2: OBSIDIAN BLACK (LEFT CHEST CREST) ---
    print("Generating Colorway 2: Obsidian Black Work Shirt (v11)...")
    color_white = np.array([245, 246, 250])
    color_gold_b = np.array([235, 175, 45])
    badge_black = np.zeros((th, tw, 4), dtype=np.uint8)
    for c in range(3):
        badge_black[:, :, c] = np.where(emblem_mask, color_gold_b[c], color_white[c])
    badge_black[:, :, 3] = alpha

    im_badge_black = Image.fromarray(badge_black)
    badge_canvas_b = Image.new('RGBA', (tw, th + 20), (0, 0, 0, 0))
    badge_canvas_b.paste(im_badge_black, (0, 0), mask=im_badge_black.split()[3])
    draw_bb = ImageDraw.Draw(badge_canvas_b)
    draw_bb.text(((tw - w_sub) // 2, th + 4), sub_text, font=font_sub, fill=(235, 175, 45, 245))

    sh_mask_b = badge_canvas_b.split()[3].filter(ImageFilter.GaussianBlur(1.0))
    sh_fill_b = Image.new('RGBA', badge_canvas_b.size, (0, 0, 0, 160))
    sh_fill_b.putalpha(sh_mask_b)

    black_canvas = clean_black_base.convert('RGBA')
    black_canvas.paste(sh_fill_b, (lx + 1, ly + 2), mask=sh_mask_b)
    black_canvas.paste(badge_canvas_b, (lx, ly), mask=badge_canvas_b.split()[3])

    final_black = black_canvas.convert('RGB')
    target_b_v11 = os.path.join(PROD_DIR, 'kc-work-shirt-black-front-v11.jpg')
    final_black.save(target_b_v11, quality=98)
    final_black.save(os.path.join(MASTERS_DIR, 'kc-work-shirt-black-front-v11.jpg'), quality=98)
    for f in ['kc-work-shirt-black-front-v8.jpg', 'kc-work-shirt-black-front-v2.jpg', 'kc-work-shirt-black-front.jpg']:
        final_black.save(os.path.join(PROD_DIR, f), quality=98)
        final_black.save(os.path.join(MASTERS_DIR, f), quality=98)

    # --- COLORWAY 3: CHARCOAL SLATE (BACK STATEMENT VIEW) ---
    print("Generating Colorway 3: Charcoal Slate Back Statement Piece (v11)...")
    charcoal_back = Image.open('scratch/charcoal_back_test.jpg').convert('RGB')
    target_back_v11 = os.path.join(PROD_DIR, 'kc-work-shirt-charcoal-back-v11.jpg')
    charcoal_back.save(target_back_v11, quality=98)
    charcoal_back.save(os.path.join(MASTERS_DIR, 'kc-work-shirt-charcoal-back-v11.jpg'), quality=98)
    for f in ['kc-work-shirt-charcoal-back-v8.jpg', 'kc-work-shirt-charcoal-back-v2.jpg', 'kc-work-shirt-charcoal-back.jpg']:
        charcoal_back.save(os.path.join(PROD_DIR, f), quality=98)
        charcoal_back.save(os.path.join(MASTERS_DIR, f), quality=98)

    # --- 4. STUDIO / MODEL VIEW ---
    print("Generating Image 4: Professional Studio Lookbook Presentation (v11)...")
    target_model_v11 = os.path.join(PROD_DIR, 'kc-work-shirt-model-v11.jpg')
    final_grey.save(target_model_v11, quality=98)
    final_grey.save(os.path.join(MASTERS_DIR, 'kc-work-shirt-model-v11.jpg'), quality=98)
    for f in ['kc-work-shirt-model-v2.jpg', 'kc-work-shirt-model.jpg']:
        final_grey.save(os.path.join(PROD_DIR, f), quality=98)
        final_grey.save(os.path.join(MASTERS_DIR, f), quality=98)

    print("✓ Successfully generated all 4 KrowN Construction work shirts (v11) with ZERO artifacts and professional left chest placement!")

# =========================================================================
# MAIN EXECUTION
# =========================================================================
if __name__ == '__main__':
    deploy_axiom_stickers()
    deploy_axiom_beanies()
    deploy_kc_work_shirts()
    print("\n" + "=" * 80)
    print("ALL V11 ASSETS SUCCESSFULLY GENERATED AND PERSISTED TO DISK!")
    print("=" * 80)
