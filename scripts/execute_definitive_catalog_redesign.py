import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

scratch_dir = r'C:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store'
prod_dir = os.path.join(scratch_dir, 'public', 'images', 'products')
brand_dir = os.path.join(scratch_dir, 'public', 'images', 'branding')
const_dir = os.path.join(brand_dir, 'construction')
gaming_dir = os.path.join(brand_dir, 'gaming')
brain_dir = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'

print("=== STARTING DEFINITIVE PHOTOREAL CATALOG REDESIGN ===")

# ==============================================================================
# 0. PREPARE 100% PURE EMBLEMS (ZERO BLACK FRINGE / ZERO RECTANGULAR BOXES)
# ==============================================================================
print("\n[0/8] Preparing pure alpha branding assets...")
# A. Pure K-Crown (zero dark border)
crown_raw = Image.open(os.path.join(brand_dir, 'krown_official_crown_pure.png')).convert('RGBA')
arr_cr = np.array(crown_raw).copy()
alpha_cr = arr_cr[:, :, 3]
rgb_cr = arr_cr[:, :, :3]
# Strip any semi-transparent dark fringe pixels:
# If luminance is very low (< 45) and alpha < 240, make alpha = 0
lum = 0.299 * rgb_cr[:, :, 0] + 0.587 * rgb_cr[:, :, 1] + 0.114 * rgb_cr[:, :, 2]
bad_fringe = (lum < 48) & (alpha_cr < 240)
arr_cr[bad_fringe, 3] = 0
pure_crown_img = Image.fromarray(arr_cr)
pure_crown_img.save(os.path.join(brand_dir, 'krown_official_crown_pure.png'))
print("-> Cleaned K-Crown pure alpha mask")

# B. Gaming Assets
owl_smokey = Image.open(os.path.join(gaming_dir, 'axiom-smokey-owl-green-eyes-clean.png')).convert('RGBA')
gothic_img = Image.open(os.path.join(gaming_dir, 'axiom-two-tone-gothic-clean-alpha.png')).convert('RGBA')

# C. Construction Assets
kc_logo_black = Image.open(os.path.join(const_dir, 'Krown ConstructionPNG Black.PNG')).convert('RGBA')
kc_logo_white = Image.open(os.path.join(const_dir, 'KrownConstruction PNG white.PNG')).convert('RGBA')


# ==============================================================================
# 1. KROWN FRENCH TERRY SHORTS (CLEAN V6: ZERO BADGE ON FLY, CROWN ON THIGH)
# ==============================================================================
print("\n[1/8] Rebuilding KrowN French Terry Shorts (v6)...")
raw_shorts_path = os.path.join(prod_dir, 'krown-french-terry-streetwear-shorts.png')
im_shorts = Image.open(raw_shorts_path).convert('RGBA')
arr_sh = np.array(im_shorts).copy()

# The center fly (x: 450..650) is 100% UNTOUCHED (natural drawstrings + brass aglets intact).
# Thigh cartoon crown is at y: 520..600, x: 765..830. Center: y=560, x=798.
Y, X = np.ogrid[:1024, :1024]
dist_thigh = np.sqrt((X - 798)**2 + (Y - 560)**2)
mask_thigh = np.clip((46 - dist_thigh) / 8.0, 0, 1)[:, :, None]

donor_sh = arr_sh[440:490, 765:830]
donor_tile = np.tile(donor_sh, (3, 3, 1))[:92, :92]
patch_thigh = arr_sh[560-46:560+46, 798-46:798+46]
arr_sh[560-46:560+46, 798-46:798+46] = (donor_tile * mask_thigh[560-46:560+46, 798-46:798+46] + patch_thigh * (1 - mask_thigh[560-46:560+46, 798-46:798+46])).astype(np.uint8)

clean_shorts_img = Image.fromarray(arr_sh)

# Resize pure gold crown for thigh embroidery
aspect_crown = pure_crown_img.height / pure_crown_img.width
cw_s = 68
ch_s = int(cw_s * aspect_crown)
cr_s = pure_crown_img.resize((cw_s, ch_s), Image.Resampling.LANCZOS)

# Subtle shadow
sh_s = Image.new('RGBA', (cw_s + 4, ch_s + 4), (0, 0, 0, 0))
s_mask = cr_s.split()[3].point(lambda p: int(p * 0.35))
sh_s.paste((10, 10, 10, 180), (2, 2), mask=s_mask)
sh_s = sh_s.filter(ImageFilter.GaussianBlur(1.2))

clean_shorts_img.paste(sh_s, (765, 532), mask=sh_s.split()[3])
clean_shorts_img.paste(cr_s, (765, 530), mask=cr_s.split()[3])

shorts_v6_path = os.path.join(prod_dir, 'krown-french-terry-shorts-photoreal-v6.jpg')
clean_shorts_img.convert('RGB').save(shorts_v6_path, quality=96)
# Also sync older versions for any external legacy link
for fname in ['krown-french-terry-shorts-clean-v5.jpg', 'krown-french-terry-shorts-clean-v4.jpg', 'krown-french-terry-shorts.jpg']:
    clean_shorts_img.convert('RGB').save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved krown-french-terry-shorts-photoreal-v6.jpg (Fly 100% untouched, Thigh crown clean)")


# ==============================================================================
# 2. KROWN STREETWEAR SET (CLEAN V6: ZERO RECTANGULAR BOXES, ZERO SMUDGES)
# ==============================================================================
print("\n[2/8] Rebuilding KrowN Streetwear Set (v6)...")
orig_set_path = os.path.join(prod_dir, 'orig_streetwear_set.jpg')
im_set = Image.open(orig_set_path).convert('RGB')
arr_set = np.array(im_set).copy()

# 1. Clean dark smudge on pants crotch/fly: y=430, x=700, radius 38
dist_smudge = np.sqrt((X - 700)**2 + (Y - 430)**2)
mask_smudge = np.clip((38 - dist_smudge) / 8.0, 0, 1)[:, :, None]
donor_smudge = arr_set[340:380, 780:820]
donor_smudge_tile = np.tile(donor_smudge, (3, 3, 1))[:76, :76]
patch_smudge = arr_set[430-38:430+38, 700-38:700+38]
arr_set[430-38:430+38, 700-38:700+38] = (donor_smudge_tile * mask_smudge[430-38:430+38, 700-38:700+38] + patch_smudge * (1 - mask_smudge[430-38:430+38, 700-38:700+38])).astype(np.uint8)

# 2. Clean hoodie chest: y=405, x=400, radius 40
dist_h = np.sqrt((X - 400)**2 + (Y - 405)**2)
mask_h = np.clip((42 - dist_h) / 8.0, 0, 1)[:, :, None]
donor_h = arr_set[320:365, 375:425]
donor_h_tile = np.tile(donor_h, (3, 3, 1))[:84, :84]
patch_h = arr_set[405-42:405+42, 400-42:400+42]
arr_set[405-42:405+42, 400-42:400+42] = (donor_h_tile * mask_h[405-42:405+42, 400-42:400+42] + patch_h * (1 - mask_h[405-42:405+42, 400-42:400+42])).astype(np.uint8)

# 3. Clean sweatpants thigh: y=440, x=870, radius 44
dist_p = np.sqrt((X - 870)**2 + (Y - 440)**2)
mask_p = np.clip((44 - dist_p) / 8.0, 0, 1)[:, :, None]
donor_p = arr_set[370:415, 845:895]
donor_p_tile = np.tile(donor_p, (3, 3, 1))[:88, :88]
patch_p = arr_set[440-44:440+44, 870-44:870+44]
arr_set[440-44:440+44, 870-44:870+44] = (donor_p_tile * mask_p[440-44:440+44, 870-44:870+44] + patch_p * (1 - mask_p[440-44:440+44, 870-44:870+44])).astype(np.uint8)

clean_set_img = Image.fromarray(arr_set).convert('RGBA')

# Place pure metallic K-Crown on hoodie chest
cw_sh_h = 66
ch_sh_h = int(cw_sh_h * aspect_crown)
cr_sh_h = pure_crown_img.resize((cw_sh_h, ch_sh_h), Image.Resampling.LANCZOS)
sh_set_h = Image.new('RGBA', (cw_sh_h + 4, ch_sh_h + 4), (0, 0, 0, 0))
sh_mask_h = cr_sh_h.split()[3].point(lambda p: int(p * 0.35))
sh_set_h.paste((10, 10, 10, 180), (2, 2), mask=sh_mask_h)
sh_set_h = sh_set_h.filter(ImageFilter.GaussianBlur(1.2))

clean_set_img.paste(sh_set_h, (367, 372), mask=sh_set_h.split()[3])
clean_set_img.paste(cr_sh_h, (367, 370), mask=cr_sh_h.split()[3])

# Place pure metallic K-Crown on sweatpants thigh
cw_sh_p = 62
ch_sh_p = int(cw_sh_p * aspect_crown)
cr_sh_p = pure_crown_img.resize((cw_sh_p, ch_sh_p), Image.Resampling.LANCZOS)
sh_set_p = Image.new('RGBA', (cw_sh_p + 4, ch_sh_p + 4), (0, 0, 0, 0))
sh_mask_p = cr_sh_p.split()[3].point(lambda p: int(p * 0.35))
sh_set_p.paste((10, 10, 10, 180), (2, 2), mask=sh_mask_p)
sh_set_p = sh_set_p.filter(ImageFilter.GaussianBlur(1.2))

clean_set_img.paste(sh_set_p, (839, 417), mask=sh_set_p.split()[3])
clean_set_img.paste(cr_sh_p, (839, 415), mask=cr_sh_p.split()[3])

set_v6_path = os.path.join(prod_dir, 'krown-streetwear-set-photoreal-v6.jpg')
clean_set_img.convert('RGB').save(set_v6_path, quality=96)
for fname in ['krown-streetwear-set-clean-v5.jpg', 'krown-streetwear-set-clean-v4.jpg', 'krown-streetwear-set-black.jpg', 'krown-supply-streetwear-set.jpg']:
    clean_set_img.convert('RGB').save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved krown-streetwear-set-photoreal-v6.jpg (Zero rectangular boxes, Zero smudges)")


# ==============================================================================
# 3. DAD HATS (CLEAN V6: ZERO HALO CIRCLES, ZERO HOODIE MODELS IN HAT LISTING)
# ==============================================================================
print("\n[3/8] Rebuilding Dad Hats (v6)...")
# Axiom Dad Hat: Clean stone slab photo without any radial halos
orig_ax_hat_path = os.path.join(prod_dir, 'orig_axiom_dad_hat.jpg')
im_ax_hat = Image.open(orig_ax_hat_path).convert('RGB')
ax_hat_v6_path = os.path.join(prod_dir, 'axiom-dad-hat-photoreal-v6.jpg')
im_ax_hat.save(ax_hat_v6_path, quality=96)
for fname in ['axiom-dad-hat-washed-black-v4.jpg', 'axiom-dad-hat-washed-black-v3.jpg', 'axiom-dad-hat-washed-black.jpg']:
    im_ax_hat.save(os.path.join(prod_dir, fname), quality=96)

# KrowN Dad Hat: Clean embroidered gold K-Crown on twill
kr_hat_raw = Image.open(os.path.join(prod_dir, 'krown-dad-hat-washed-black.jpg')).convert('RGB')
arr_kh = np.array(kr_hat_raw).copy()
dist_kh = np.sqrt((X - 512)**2 + (Y - 440)**2)
mask_kh = np.clip((62 - dist_kh) / 10.0, 0, 1)[:, :, None]
donor_kh = arr_kh[340:390, 480:540]
donor_kh_tile = np.tile(donor_kh, (3, 3, 1))[:124, :124]
patch_kh = arr_kh[440-62:440+62, 512-62:512+62]
arr_kh[440-62:440+62, 512-62:512+62] = (donor_kh_tile * mask_kh[440-62:440+62, 512-62:512+62] + patch_kh * (1 - mask_kh[440-62:440+62, 512-62:512+62])).astype(np.uint8)

clean_kh = Image.fromarray(arr_kh).convert('RGBA')
cw_kh = 94
ch_kh = int(cw_kh * aspect_crown)
cr_kh = pure_crown_img.resize((cw_kh, ch_kh), Image.Resampling.LANCZOS)
sh_kh = Image.new('RGBA', (cw_kh + 4, ch_kh + 4), (0, 0, 0, 0))
sh_m_kh = cr_kh.split()[3].point(lambda p: int(p * 0.40))
sh_kh.paste((10, 10, 10, 200), (2, 2), mask=sh_m_kh)
sh_kh = sh_kh.filter(ImageFilter.GaussianBlur(1.5))
clean_kh.paste(sh_kh, (512 - cw_kh//2, 440 - ch_kh//2 + 2), mask=sh_kh.split()[3])
clean_kh.paste(cr_kh, (512 - cw_kh//2, 440 - ch_kh//2), mask=cr_kh.split()[3])

kr_hat_v6_path = os.path.join(prod_dir, 'krown-dad-hat-photoreal-v6.jpg')
clean_kh.convert('RGB').save(kr_hat_v6_path, quality=96)
clean_kh.convert('RGB').save(os.path.join(prod_dir, 'krown-dad-hat-washed-black.jpg'), quality=96)
print("-> Saved dad hats v6 (Axiom & Krown pristine studio stone shots)")


# ==============================================================================
# 4. REDESIGNED AXIOM 450 GSM HEAVYWEIGHT HOODIE (STUDIO & MODEL LOOKBOOK)
# ==============================================================================
print("\n[4/8] Redesigning Axiom Heavyweight Streetwear Hoodie (v6)...")
# Base: Genuine heavyweight studio French Terry hoodie on hanger
hoodie_base_raw = Image.open(os.path.join(prod_dir, 'krown-supply-premium-hoodie-front.jpg')).convert('RGBA')

# 1. Clean Owl Mascot Chest Emblem
owl_w_h = 240
owl_h_h = int(owl_smokey.height * (owl_w_h / owl_smokey.width))
owl_resized = owl_smokey.resize((owl_w_h, owl_h_h), Image.Resampling.LANCZOS)

# Soft realistic embroidery shadow
sh_owl = Image.new('RGBA', (owl_w_h + 6, owl_h_h + 6), (0, 0, 0, 0))
sh_owl_mask = owl_resized.split()[3].point(lambda p: int(p * 0.40))
sh_owl.paste((12, 12, 15, 200), (3, 3), mask=sh_owl_mask)
sh_owl = sh_owl.filter(ImageFilter.GaussianBlur(1.5))

cx_chest = (1024 - owl_w_h) // 2
cy_chest = 460
hoodie_base_raw.paste(sh_owl, (cx_chest, cy_chest + 2), mask=sh_owl.split()[3])
hoodie_base_raw.paste(owl_resized, (cx_chest, cy_chest), mask=owl_resized.split()[3])

# 2. Clean Gothic Two-Tone "AXIOM ALLEGIANCE" down the right sleeve
# Rotate -90 degrees so text runs vertically down forearm
gothic_vert = gothic_img.rotate(-90, expand=True, resample=Image.Resampling.BICUBIC)
gw_sl = 48
gh_sl = int(gothic_vert.height * (gw_sl / gothic_vert.width))
gothic_sl = gothic_vert.resize((gw_sl, gh_sl), Image.Resampling.LANCZOS)

sh_sl = Image.new('RGBA', (gw_sl + 4, gh_sl + 4), (0, 0, 0, 0))
sh_sl_mask = gothic_sl.split()[3].point(lambda p: int(p * 0.35))
sh_sl.paste((10, 10, 10, 180), (2, 2), mask=sh_sl_mask)
sh_sl = sh_sl.filter(ImageFilter.GaussianBlur(1.2))

# Position on right forearm sleeve (our right: x: 745..795, y: 460..740)
sx = 750
sy = 480
hoodie_base_raw.paste(sh_sl, (sx, sy + 2), mask=sh_sl.split()[3])
hoodie_base_raw.paste(gothic_sl, (sx, sy), mask=gothic_sl.split()[3])

# 3. Add dipped dual-tone metal aglet accents to the drawstrings
# The drawstrings in this base hang at x ~ 485 and x ~ 538, y ~ 370..430
ag_draw = ImageDraw.Draw(hoodie_base_raw)
# Left cord aglet tip: Royal Purple
ag_draw.rounded_rectangle([482, 420, 488, 436], radius=2, fill=(138, 43, 226, 240), outline=(100, 30, 170, 255))
# Right cord aglet tip: Toxic Neon Green
ag_draw.rounded_rectangle([535, 420, 541, 436], radius=2, fill=(57, 255, 20, 240), outline=(40, 180, 15, 255))

ax_hoodie_v6_path = os.path.join(prod_dir, 'axiom-heavyweight-hoodie-photoreal-v6.jpg')
hoodie_base_raw.convert('RGB').save(ax_hoodie_v6_path, quality=96)
hoodie_base_raw.convert('RGB').save(os.path.join(prod_dir, 'axiom-heavyweight-hoodie-v3.jpg'), quality=96)

# 4. Urban Male Model Lookbook Photo for Axiom Hoodie
model_hoodie_raw = Image.open(os.path.join(prod_dir, 'krown-hoodie-male-model.jpg')).convert('RGBA')
# Composite the Axiom Owl chest crest onto the model
owl_m_w = 175
owl_m_h = int(owl_smokey.height * (owl_m_w / owl_smokey.width))
owl_m_res = owl_smokey.resize((owl_m_w, owl_m_h), Image.Resampling.LANCZOS)

sh_m = Image.new('RGBA', (owl_m_w + 4, owl_m_h + 4), (0, 0, 0, 0))
sh_m_mask = owl_m_res.split()[3].point(lambda p: int(p * 0.40))
sh_m.paste((10, 10, 10, 200), (2, 2), mask=sh_m_mask)
sh_m = sh_m.filter(ImageFilter.GaussianBlur(1.5))

# Chest center on male model: x ~ 425, y ~ 450
model_hoodie_raw.paste(sh_m, (425, 452), mask=sh_m.split()[3])
model_hoodie_raw.paste(owl_m_res, (425, 450), mask=owl_m_res.split()[3])

ax_model_v6_path = os.path.join(prod_dir, 'axiom-heavyweight-hoodie-model-v6.jpg')
model_hoodie_raw.convert('RGB').save(ax_model_v6_path, quality=96)
model_hoodie_raw.convert('RGB').save(os.path.join(prod_dir, 'axiom-heavyweight-hoodie-model-v4.jpg'), quality=96)
model_hoodie_raw.convert('RGB').save(os.path.join(prod_dir, 'axiom-heavyweight-hoodie-model.jpg'), quality=96)
print("-> Saved redesigned Axiom Hoodie (Studio front v6 & Urban Lookbook Model v6)")


# ==============================================================================
# 5. AXIOM PRO JOGGERS (CLEAN V6: ZERO GREEN SPRAY SQUARE ON WALL, PURPLE & LIME LEG)
# ==============================================================================
print("\n[5/8] Rebuilding Axiom Pro Heavyweight Joggers (v6)...")
clean_jogger_path = os.path.join(brain_dir, 'axiom_pro_joggers_clean_1791592187560.jpg')
im_jogger = Image.open(clean_jogger_path).convert('RGBA')

# The wall behind the model's hand in this clean photo is natural gray loft concrete (ZERO bright green square!).
# Now apply clean Royal Purple & Toxic Neon Green "AXIOM ALLEGIANCE" down the left leg naturally
# The left leg (model's right leg, our left/center) runs down from y: 360 to y: 550, angled at approx ~22 degrees
# Render two-tone vertical typography
try:
    f_leg = ImageFont.truetype("arialbd.ttf", 30)
except:
    f_leg = ImageFont.load_default()

leg_text_img = Image.new('RGBA', (340, 50), (0, 0, 0, 0))
lt_draw = ImageDraw.Draw(leg_text_img)
# Two-tone: "AXIOM" in Royal Purple, "ALLEGIANCE" in Toxic Neon Green
lt_draw.text((10, 8), "AXIOM", font=f_leg, fill=(160, 60, 255, 240))
w_ax = lt_draw.textlength("AXIOM ", font=f_leg)
lt_draw.text((10 + w_ax, 8), "ALLEGIANCE", font=f_leg, fill=(57, 255, 20, 240))

# Rotate along the natural leg angle (-70 degrees)
leg_text_rot = leg_text_img.rotate(-68, expand=True, resample=Image.Resampling.BICUBIC)

# Subtle shadow
sh_leg = Image.new('RGBA', (leg_text_rot.width + 4, leg_text_rot.height + 4), (0, 0, 0, 0))
sh_leg_m = leg_text_rot.split()[3].point(lambda p: int(p * 0.35))
sh_leg.paste((5, 5, 5, 180), (2, 2), mask=sh_leg_m)
sh_leg = sh_leg.filter(ImageFilter.GaussianBlur(1.2))

# Position down the sweatpants leg (x: 440..540, y: 350..550)
im_jogger.paste(sh_leg, (452, 357), mask=sh_leg.split()[3])
im_jogger.paste(leg_text_rot, (450, 355), mask=leg_text_rot.split()[3])

jogger_v6_path = os.path.join(prod_dir, 'axiom-sweatpants-pro-photoreal-v6.jpg')
im_jogger.convert('RGB').save(jogger_v6_path, quality=96)
for fname in ['axiom-sweatpants-pro-model-v5.jpg', 'axiom-sweatpants-pro-model-v4.jpg', 'axiom-sweatpants-pro-model.jpg']:
    im_jogger.convert('RGB').save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved axiom-sweatpants-pro-photoreal-v6.jpg (Zero green square on wall, Two-tone Purple & Lime leg)")


# ==============================================================================
# 6. REDESIGNED SHAKERS (KROWN CONSTRUCTION & KROWN SUPPLY CO - 100% STUDIO)
# ==============================================================================
print("\n[6/8] Redesigning Shakers (KrowN Construction & KrowN Supply Co)...")

def render_master_studio_shaker(brand_mode, edition_color, edition_name):
    W, H = 1024, 1024
    
    if brand_mode == "KrowN Construction":
        # Industrial workshop concrete surface
        canvas = Image.new("RGBA", (W, H), (22, 23, 27, 255))
        c_draw = ImageDraw.Draw(canvas)
        
        # Warm golden workshop studio rim lighting
        for r in range(750, 0, -8):
            alpha = int(32 * (1.0 - r / 750.0))
            c_draw.ellipse([640 - r, 360 - r * 0.7, 640 + r, 360 + r * 0.7], fill=(52, 40, 18, alpha))
            
        c_draw.line([(0, 810), (W, 810)], fill=(36, 38, 44, 255), width=2)
        c_draw.rectangle([0, 812, W, H], fill=(16, 17, 20, 255))
        
    else: # KrowN Supply Co.
        # Luxury dark obsidian pedestal
        canvas = Image.new("RGBA", (W, H), (14, 15, 18, 255))
        c_draw = ImageDraw.Draw(canvas)
        
        for r in range(700, 0, -8):
            alpha = int(30 * (1.0 - r / 700.0))
            c_draw.ellipse([512 - r, 330 - r * 0.7, 512 + r, 330 + r * 0.7], fill=(48, 38, 16, alpha))
            
        c_draw.line([(0, 810), (W, 810)], fill=(30, 32, 38, 255), width=2)
        c_draw.rectangle([0, 812, W, H], fill=(10, 11, 14, 255))

    # Base clean shaker bottle geometry: (axiom-shaker-stealth-steel-clean.jpg, 768x1376)
    base_src = os.path.join(prod_dir, 'axiom-shaker-stealth-steel-clean.jpg')
    im_base = Image.open(base_src).convert('RGBA')
    bottle_crop = im_base.crop((195, 110, 575, 1220))
    
    target_bh = 700
    target_bw = int(bottle_crop.width * (target_bh / bottle_crop.height))
    bottle_scaled = bottle_crop.resize((target_bw, target_bh), Image.Resampling.LANCZOS)
    arr_b = np.array(bottle_scaled).copy()
    
    # Body coloring based on edition:
    if "highvis" in edition_color or "gold" in edition_color:
        body_col = [22, 23, 26]
        accent_col = (235, 180, 40)
    elif "steel" in edition_color or "titanium" in edition_color:
        body_col = [55, 58, 64]
        accent_col = (200, 205, 215)
    elif "smoke" in edition_color:
        body_col = [32, 34, 38]
        accent_col = (212, 175, 55)
    else: # obsidian black
        body_col = [18, 19, 22]
        accent_col = (212, 175, 55) if brand_mode == "KrowN Supply Co." else (235, 180, 40)
        
    for x_i in range(target_bw):
        t = x_i / float(target_bw)
        factor = 0.85 + 0.35 * math.sin(t * math.pi)
        arr_b[260:550, x_i, :3] = np.clip(np.array(body_col) * factor, 10, 255).astype(np.uint8)
        
    bottle_cleaned = Image.fromarray(arr_b)
    
    # Soft accent tint on lid silicone band
    arr_lid = np.array(bottle_cleaned)
    for y_i in range(130, 180):
        alpha_t = 0.32 * math.sin(((y_i - 130) / 50.0) * math.pi)
        for c in range(3):
            arr_lid[y_i, :, c] = np.clip(arr_lid[y_i, :, c] * (1 - alpha_t) + accent_col[c] * alpha_t, 0, 255).astype(np.uint8)
    bottle_cleaned = Image.fromarray(arr_lid)
    
    cx_b = target_bw // 2
    cy_b = 405
    
    if brand_mode == "KrowN Construction":
        # Official KrowN Construction brand insignia
        # Scale kc_logo_white to fit cleanly on front of bottle
        kc_target_w = int(target_bw * 0.62)
        kc_target_h = int(kc_logo_white.height * (kc_target_w / kc_logo_white.width))
        kc_res = kc_logo_white.resize((kc_target_w, kc_target_h), Image.Resampling.LANCZOS)
        
        # Tint slightly golden/safety-gold for high-vis edition or clean crisp white
        if "highvis" in edition_color:
            arr_kc = np.array(kc_res).copy()
            # Golden tint
            arr_kc[arr_kc[:, :, 3] > 50, 0] = 245
            arr_kc[arr_kc[:, :, 3] > 50, 1] = 195
            arr_kc[arr_kc[:, :, 3] > 50, 2] = 45
            kc_res = Image.fromarray(arr_kc)
            
        sh_kc = Image.new('RGBA', (kc_target_w + 4, kc_target_h + 4), (0, 0, 0, 0))
        sh_kc_m = kc_res.split()[3].point(lambda p: int(p * 0.40))
        sh_kc.paste((10, 10, 10, 200), (2, 2), mask=sh_kc_m)
        sh_kc = sh_kc.filter(ImageFilter.GaussianBlur(1.2))
        
        bx = cx_b - kc_target_w // 2
        by = cy_b - kc_target_h // 2
        bottle_cleaned.paste(sh_kc, (bx, by + 2), mask=sh_kc.split()[3])
        bottle_cleaned.paste(kc_res, (bx, by), mask=kc_res.split()[3])
        
    else: # KrowN Supply Co.
        # Official pure metallic gold 3D K-Crown
        cr_w = int(target_bw * 0.52)
        cr_h = int(cr_w * aspect_crown)
        cr_shk = pure_crown_img.resize((cr_w, cr_h), Image.Resampling.LANCZOS)
        
        sh_cr = Image.new('RGBA', (cr_w + 4, cr_h + 4), (0, 0, 0, 0))
        sh_cr_m = cr_shk.split()[3].point(lambda p: int(p * 0.40))
        sh_cr.paste((10, 10, 10, 200), (2, 2), mask=sh_cr_m)
        sh_cr = sh_cr.filter(ImageFilter.GaussianBlur(1.5))
        
        bx = cx_b - cr_w // 2
        by = cy_b - cr_h // 2
        bottle_cleaned.paste(sh_cr, (bx, by + 2), mask=sh_cr.split()[3])
        bottle_cleaned.paste(cr_shk, (bx, by), mask=cr_shk.split()[3])
        
    # Ground shadow on studio workbench
    pos_x = (W - target_bw) // 2
    pos_y = 810 - target_bh
    
    shadow_floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow_floor).ellipse([pos_x - 30, 800, pos_x + target_bw + 30, 830], fill=(0, 0, 0, 230))
    shadow_floor = shadow_floor.filter(ImageFilter.GaussianBlur(14))
    
    canvas.paste(shadow_floor, (0, 0), mask=shadow_floor.split()[3])
    canvas.paste(bottle_cleaned, (pos_x, pos_y), mask=bottle_cleaned.split()[3])
    
    return canvas.convert('RGB')

# 1. KrowN Construction Shakers (3 clean editions)
im_kc_hv = render_master_studio_shaker("KrowN Construction", "highvis", "High-Vis Safety Gold")
im_kc_ti = render_master_studio_shaker("KrowN Construction", "steel", "Industrial Titanium Steel")
im_kc_ob = render_master_studio_shaker("KrowN Construction", "obsidian", "Tradesman Obsidian Black")

im_kc_hv.save(os.path.join(prod_dir, 'kc-shaker-photoreal-v6.jpg'), quality=96)
im_kc_ti.save(os.path.join(prod_dir, 'kc-shaker-steelcore-v6.jpg'), quality=96)
im_kc_ob.save(os.path.join(prod_dir, 'kc-shaker-tradesman-v6.jpg'), quality=96)

# Sync all old KC shaker filenames so any cache/links immediately pick up the clean renders
for fname in ['kc-shaker-highvis-tritan-v4.jpg', 'kc-shaker-highvis-tritan-v3.jpg', 'kc-shaker-highvis-tritan.jpg', 
              'kc-shaker-highvis-steel-v2.jpg', 'kc-shaker-highvis-steel.jpg']:
    im_kc_hv.save(os.path.join(prod_dir, fname), quality=96)
for fname in ['kc-shaker-steelcore-steel.jpg', 'kc-shaker-steelcore-tritan.jpg']:
    im_kc_ti.save(os.path.join(prod_dir, fname), quality=96)
for fname in ['kc-shaker-jobsite-steel.jpg', 'kc-shaker-jobsite-tritan.jpg']:
    im_kc_ob.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved KrowN Construction Shakers v6 (All 3 editions 100% studio, Zero gaming desks)")

# 2. KrowN Supply Co Shakers (3 clean editions)
im_kr_ob = render_master_studio_shaker("KrowN Supply Co.", "obsidian", "Matte Obsidian Black")
im_kr_sm = render_master_studio_shaker("KrowN Supply Co.", "smoke", "Frosted Smoke")
im_kr_st = render_master_studio_shaker("KrowN Supply Co.", "steel", "Raw Brushed Steel")

im_kr_ob.save(os.path.join(prod_dir, 'krown-shaker-photoreal-v6.jpg'), quality=96)
im_kr_sm.save(os.path.join(prod_dir, 'krown-shaker-smoke-v6.jpg'), quality=96)
im_kr_st.save(os.path.join(prod_dir, 'krown-shaker-brushed-v6.jpg'), quality=96)

for fname in ['krown-shaker-obsidian-steel-v2.jpg', 'krown-shaker-obsidian-steel.jpg', 'krown-shaker-obsidian-tritan.jpg']:
    im_kr_ob.save(os.path.join(prod_dir, fname), quality=96)
for fname in ['krown-shaker-smoke-steel.jpg', 'krown-shaker-smoke-tritan.jpg']:
    im_kr_sm.save(os.path.join(prod_dir, fname), quality=96)
for fname in ['krown-shaker-brushed-steel.jpg', 'krown-shaker-brushed-tritan.jpg']:
    im_kr_st.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved KrowN Supply Co Shakers v6 (All 3 editions 100% studio luxury, Pure gold crown)")

print("\n=== ALL ASSETS REBUILT TO V6 QUALITY ===")
