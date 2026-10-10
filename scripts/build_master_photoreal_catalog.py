import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

scratch_dir = r'C:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store'
prod_dir = os.path.join(scratch_dir, 'public', 'images', 'products')
brand_dir = os.path.join(scratch_dir, 'public', 'images', 'branding')
gaming_dir = os.path.join(brand_dir, 'gaming')

print("=== STARTING MASTER PHOTOREAL CATALOG REBUILD ===")

# ------------------------------------------------------------------------------
# 0. Load pure branding assets
# ------------------------------------------------------------------------------
crown_pure_path = os.path.join(brand_dir, 'krown_official_crown_pure.png')
crown_img = Image.open(crown_pure_path).convert('RGBA')

owl_smokey_path = os.path.join(gaming_dir, 'axiom-smokey-owl-green-eyes-clean.png')
if not os.path.exists(owl_smokey_path):
    owl_smokey_path = os.path.join(gaming_dir, 'axiom-smokey-owl-clean-alpha.png')
owl_smokey = Image.open(owl_smokey_path).convert('RGBA')

gothic_path = os.path.join(gaming_dir, 'axiom-two-tone-gothic-clean-alpha.png')
gothic_img = Image.open(gothic_path).convert('RGBA')


# ==============================================================================
# 1. FIX KROWN FRENCH TERRY SHORTS (CLEAN V5)
# ==============================================================================
print("\n[1/7] Fixing KrowN French Terry Shorts...")
raw_shorts_path = os.path.join(prod_dir, 'krown-french-terry-streetwear-shorts.png')
im_shorts = Image.open(raw_shorts_path).convert('RGBA')
arr_shorts = np.array(im_shorts).copy()

# The center fly (x: 450..650) is COMPLETELY UNTOUCHED to keep natural drawstrings + aglets.
# Cartoon crown is on the thigh at y: 520..600, x: 765..830.
# Center around y=560, x=798:
Y, X = np.ogrid[:1024, :1024]
dist_thigh = np.sqrt((X - 798)**2 + (Y - 560)**2)
mask_thigh = np.clip((46 - dist_thigh) / 8.0, 0, 1)[:, :, None]

# Sample donor fabric from clean upper thigh (y: 440..490, x: 765..830)
donor_sh = arr_shorts[440:490, 765:830]
donor_tile = np.tile(donor_sh, (3, 3, 1))[:92, :92]
patch_thigh = arr_shorts[560-46:560+46, 798-46:798+46]
arr_shorts[560-46:560+46, 798-46:798+46] = (donor_tile * mask_thigh[560-46:560+46, 798-46:798+46] + patch_thigh * (1 - mask_thigh[560-46:560+46, 798-46:798+46])).astype(np.uint8)

clean_shorts_img = Image.fromarray(arr_shorts)

# Official metallic gold K-Crown emblem on left thigh
cw_s = 68
aspect_crown = crown_img.height / crown_img.width
ch_s = int(cw_s * aspect_crown)
crown_s = crown_img.resize((cw_s, ch_s), Image.Resampling.LANCZOS)

# Subtle embroidery shadow
shadow_s = Image.new('RGBA', (cw_s + 4, ch_s + 4), (0, 0, 0, 0))
s_mask = crown_s.split()[3].point(lambda p: int(p * 0.35))
shadow_s.paste((10, 10, 10, 180), (2, 2), mask=s_mask)
shadow_s = shadow_s.filter(ImageFilter.GaussianBlur(1.2))

# Composite onto thigh at x=765, y=530 (natural embroidered position)
clean_shorts_img.paste(shadow_s, (765, 532), mask=shadow_s.split()[3])
clean_shorts_img.paste(crown_s, (765, 530), mask=crown_s.split()[3])

final_shorts = clean_shorts_img.convert('RGB')
for fname in ['krown-french-terry-shorts-clean-v5.jpg', 'krown-french-terry-shorts-clean-v4.jpg', 
              'krown-french-terry-shorts-v3.jpg', 'krown-french-terry-shorts-v2.jpg', 
              'krown-french-terry-shorts.jpg']:
    final_shorts.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved pristine KrowN French Terry Shorts (Fly 100% clean, Crown on thigh)")


# ==============================================================================
# 2. FIX KROWN STREETWEAR SET (HOODIE + SWEATPANTS)
# ==============================================================================
print("\n[2/7] Fixing KrowN Streetwear Set...")
orig_set_path = os.path.join(prod_dir, 'orig_streetwear_set.jpg')
im_set = Image.open(orig_set_path).convert('RGB')
arr_set = np.array(im_set).copy()

# Inpaint hoodie chest: y=405, x=400, radius 40
dist_h = np.sqrt((X - 400)**2 + (Y - 405)**2)
mask_h = np.clip((42 - dist_h) / 8.0, 0, 1)[:, :, None]
donor_h = arr_set[320:365, 375:425]
donor_h_tile = np.tile(donor_h, (3, 3, 1))[:84, :84]
patch_h = arr_set[405-42:405+42, 400-42:400+42]
arr_set[405-42:405+42, 400-42:400+42] = (donor_h_tile * mask_h[405-42:405+42, 400-42:400+42] + patch_h * (1 - mask_h[405-42:405+42, 400-42:400+42])).astype(np.uint8)

# Inpaint sweatpants thigh: y=440, x=870, radius 44
dist_p = np.sqrt((X - 870)**2 + (Y - 440)**2)
mask_p = np.clip((44 - dist_p) / 8.0, 0, 1)[:, :, None]
donor_p = arr_set[370:415, 845:895]
donor_p_tile = np.tile(donor_p, (3, 3, 1))[:88, :88]
patch_p = arr_set[440-44:440+44, 870-44:870+44]
arr_set[440-44:440+44, 870-44:870+44] = (donor_p_tile * mask_p[440-44:440+44, 870-44:870+44] + patch_p * (1 - mask_p[440-44:440+44, 870-44:870+44])).astype(np.uint8)

clean_set_img = Image.fromarray(arr_set).convert('RGBA')

# Place pure metallic K-Crown on hoodie chest
cw_set_h = 66
ch_set_h = int(cw_set_h * aspect_crown)
cr_set_h = crown_img.resize((cw_set_h, ch_set_h), Image.Resampling.LANCZOS)
sh_set_h = Image.new('RGBA', (cw_set_h + 4, ch_set_h + 4), (0, 0, 0, 0))
sh_mask_h = cr_set_h.split()[3].point(lambda p: int(p * 0.35))
sh_set_h.paste((10, 10, 10, 180), (2, 2), mask=sh_mask_h)
sh_set_h = sh_set_h.filter(ImageFilter.GaussianBlur(1.2))

clean_set_img.paste(sh_set_h, (367, 372), mask=sh_set_h.split()[3])
clean_set_img.paste(cr_set_h, (367, 370), mask=cr_set_h.split()[3])

# Place pure metallic K-Crown on sweatpants thigh
cw_set_p = 62
ch_set_p = int(cw_set_p * aspect_crown)
cr_set_p = crown_img.resize((cw_set_p, ch_set_p), Image.Resampling.LANCZOS)
sh_set_p = Image.new('RGBA', (cw_set_p + 4, ch_set_p + 4), (0, 0, 0, 0))
sh_mask_p = cr_set_p.split()[3].point(lambda p: int(p * 0.35))
sh_set_p.paste((10, 10, 10, 180), (2, 2), mask=sh_mask_p)
sh_set_p = sh_set_p.filter(ImageFilter.GaussianBlur(1.2))

clean_set_img.paste(sh_set_p, (839, 417), mask=sh_set_p.split()[3])
clean_set_img.paste(cr_set_p, (839, 415), mask=cr_set_p.split()[3])

final_set = clean_set_img.convert('RGB')
for fname in ['krown-streetwear-set-clean-v5.jpg', 'krown-streetwear-set-clean-v4.jpg', 
              'krown-streetwear-set-v3.jpg', 'krown-streetwear-set-v2.jpg', 
              'krown-streetwear-set-black.jpg', 'krown-supply-streetwear-set.jpg']:
    final_set.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved pristine KrowN Streetwear Set (Zero bounding boxes, Pure K-Crown)")


# ==============================================================================
# 3. FIX DAD HATS (KROWN & AXIOM)
# ==============================================================================
print("\n[3/7] Fixing Dad Hats (KrowN & Axiom)...")
# Axiom Dad Hat: Clean studio photo on stone slab without any white halo / radial circles
orig_axiom_hat_path = os.path.join(prod_dir, 'orig_axiom_dad_hat.jpg')
if os.path.exists(orig_axiom_hat_path):
    im_ax_hat = Image.open(orig_axiom_hat_path).convert('RGB')
    for fname in ['axiom-dad-hat-washed-black-v4.jpg', 'axiom-dad-hat-washed-black-v3.jpg', 
                  'axiom-dad-hat-washed-black-v2.jpg', 'axiom-dad-hat-washed-black.jpg']:
        im_ax_hat.save(os.path.join(prod_dir, fname), quality=96)
    print("-> Restored clean Axiom Dad Hat (Zero halo circles)")

# KrowN Dad Hat: Replace cartoon crown with official gold K-Crown
kr_hat_path = os.path.join(prod_dir, 'krown-dad-hat-washed-black.jpg')
if os.path.exists(kr_hat_path):
    im_kr_hat = Image.open(kr_hat_path).convert('RGB')
    arr_kh = np.array(im_kr_hat).copy()
    
    # Inpaint hat front crown area: y=440, x=512, radius 60
    dist_kh = np.sqrt((X - 512)**2 + (Y - 440)**2)
    mask_kh = np.clip((62 - dist_kh) / 10.0, 0, 1)[:, :, None]
    donor_kh = arr_kh[340:390, 480:540]
    donor_kh_tile = np.tile(donor_kh, (3, 3, 1))[:124, :124]
    patch_kh = arr_kh[440-62:440+62, 512-62:512+62]
    arr_kh[440-62:440+62, 512-62:512+62] = (donor_kh_tile * mask_kh[440-62:440+62, 512-62:512+62] + patch_kh * (1 - mask_kh[440-62:440+62, 512-62:512+62])).astype(np.uint8)
    
    clean_kh_img = Image.fromarray(arr_kh).convert('RGBA')
    cw_kh = 94
    ch_kh = int(cw_kh * aspect_crown)
    cr_kh = crown_img.resize((cw_kh, ch_kh), Image.Resampling.LANCZOS)
    
    sh_kh = Image.new('RGBA', (cw_kh + 4, ch_kh + 4), (0, 0, 0, 0))
    sh_m_kh = cr_kh.split()[3].point(lambda p: int(p * 0.40))
    sh_kh.paste((10, 10, 10, 200), (2, 2), mask=sh_m_kh)
    sh_kh = sh_kh.filter(ImageFilter.GaussianBlur(1.5))
    
    clean_kh_img.paste(sh_kh, (512 - cw_kh//2, 440 - ch_kh//2 + 2), mask=sh_kh.split()[3])
    clean_kh_img.paste(cr_kh, (512 - cw_kh//2, 440 - ch_kh//2), mask=cr_kh.split()[3])
    
    clean_kh_img.convert('RGB').save(kr_hat_path, quality=96)
    print("-> Saved pristine KrowN Dad Hat (Official K-Crown embroidered on twill)")


# ==============================================================================
# 4. FIX AXIOM HOLOGRAPHIC STICKERS (PURE STUDIO PRODUCT PHOTO - ZERO FLYER TEXT)
# ==============================================================================
print("\n[4/7] Fixing Axiom Holographic Stickers (Pure Studio Shot, Zero Flyer Text)...")
W_stk, H_stk = 1024, 1024

# Authentic dark slate studio workbench surface
bg_stk = Image.new("RGBA", (W_stk, H_stk), (16, 17, 21, 255))
d_stk = ImageDraw.Draw(bg_stk)

# Subtle studio softbox gradient from top-center
for r in range(700, 0, -8):
    alpha = int(25 * (1.0 - r / 700.0))
    d_stk.ellipse([512 - r, 450 - r * 0.8, 512 + r, 450 + r * 0.8], fill=(35, 20, 52, alpha))

# Subtle slate texture lines
for y in range(0, H_stk, 32):
    d_stk.line([(0, y), (W_stk, y)], fill=(22, 24, 30, 255), width=1)
for x in range(0, W_stk, 32):
    d_stk.line([(x, 0), (x, H_stk)], fill=(22, 24, 30, 255), width=1)

def build_die_cut_sticker(graphic, radius=18, border=10, angle=0):
    gw, gh = graphic.size
    sw = gw + border * 2
    sh = gh + border * 2
    
    stk = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stk)
    
    # Crisp white die-cut vinyl border
    s_draw.rounded_rectangle([0, 0, sw - 1, sh - 1], radius=radius, fill=(250, 250, 254, 255))
    s_draw.rounded_rectangle([2, 2, sw - 3, sh - 3], radius=radius - 2, outline=(225, 225, 235), width=1)
    
    # Graphic centered
    stk.paste(graphic, (border, border), graphic)
    
    # Holographic iridescent sheen
    holo = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(holo)
    for d in range(-sw, sw + sh, 6):
        phase = (d % 160) / 160.0
        r_c = int(127 + 127 * math.sin(phase * 2 * math.pi))
        g_c = int(127 + 127 * math.sin((phase + 0.33) * 2 * math.pi))
        b_c = int(127 + 127 * math.sin((phase + 0.66) * 2 * math.pi))
        h_draw.line([(d, 0), (d + sh, sh)], fill=(r_c, g_c, b_c, 45), width=4)
        
    mask = stk.split()[3]
    stk = Image.composite(Image.alpha_composite(stk, holo), stk, mask)
    
    # Specular studio light sheen streak
    spec = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    ImageDraw.Draw(spec).polygon([(sw * 0.25, 0), (sw * 0.48, 0), (sw * 0.28, sh), (0, sh)], fill=(255, 255, 255, 40))
    stk = Image.composite(Image.alpha_composite(stk, spec), stk, mask)
    
    if angle != 0:
        stk = stk.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        
    # Drop shadow
    sw_rot, sh_rot = stk.size
    shadow = Image.new("RGBA", (sw_rot + 20, sh_rot + 20), (0, 0, 0, 0))
    sh_mask = stk.split()[3]
    shadow.paste((5, 5, 8, 170), (10, 12), mask=sh_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    
    return stk, shadow

# 1. Top Bumper: Two-Tone Gothic "AXIOM ALLEGIANCE" (480x100)
goth_res = gothic_img.resize((480, 95), Image.Resampling.LANCZOS)
s1, sh1 = build_die_cut_sticker(goth_res, radius=16, border=10, angle=2)

# 2. Center Hero: Large Smoky Axiom Owl Mascot (300x270)
owl_res = owl_smokey.resize((290, 260), Image.Resampling.LANCZOS)
s2, sh2 = build_die_cut_sticker(owl_res, radius=22, border=12, angle=-2)

# 3. Bottom Left Shield: AXA Diamond Crest
axa_shield = Image.new("RGBA", (170, 190), (0, 0, 0, 0))
as_draw = ImageDraw.Draw(axa_shield)
as_draw.polygon([(85, 5), (165, 85), (85, 185), (5, 85)], fill=(20, 22, 28, 255), outline=(57, 255, 20, 255), width=4)
try:
    f_axa = ImageFont.truetype("arialbd.ttf", 36)
    f_esp = ImageFont.truetype("arialbd.ttf", 15)
except:
    f_axa = ImageFont.load_default()
    f_esp = ImageFont.load_default()
as_draw.text((85, 78), "AXA", font=f_axa, fill=(57, 255, 20), anchor="mm")
as_draw.text((85, 115), "ESPORTS", font=f_esp, fill=(240, 240, 255), anchor="mm")
s3, sh3 = build_die_cut_sticker(axa_shield, radius=16, border=10, angle=-6)

# 4. Bottom Right Crest: Axiom Hex Seal
axa_hex = Image.new("RGBA", (180, 190), (0, 0, 0, 0))
ah_draw = ImageDraw.Draw(axa_hex)
cx_h, cy_h = 90, 95
r_h = 80
pts_h = [(cx_h + r_h * math.cos(math.radians(60*i - 30)), cy_h + r_h * math.sin(math.radians(60*i - 30))) for i in range(6)]
ah_draw.polygon(pts_h, fill=(24, 18, 32, 255), outline=(138, 43, 226, 255), width=4)
ah_draw.text((90, 75), "AXIOM", font=f_axa, fill=(138, 43, 226), anchor="mm")
ah_draw.text((90, 105), "ALLEGIANCE", font=f_esp, fill=(240, 240, 255), anchor="mm")
ah_draw.text((90, 128), "• PLAY TO REIGN •", font=f_esp, fill=(57, 255, 20), anchor="mm")
s4, sh4 = build_die_cut_sticker(axa_hex, radius=18, border=10, angle=5)

# 5. Bottom Center: Square Owl Icon
owl_sq = owl_smokey.resize((150, 135), Image.Resampling.LANCZOS)
s5, sh5 = build_die_cut_sticker(owl_sq, radius=16, border=10, angle=0)

# Composite all 5 stickers cleanly onto the slate studio surface
# 1. Top bumper (x=240, y=140)
bg_stk.paste(sh1, (240 - 10, 130 - 10), mask=sh1.split()[3])
bg_stk.paste(s1, (240, 130), mask=s1.split()[3])

# 2. Center hero owl (x=350, y=340)
bg_stk.paste(sh2, (350 - 10, 330 - 10), mask=sh2.split()[3])
bg_stk.paste(s2, (350, 330), mask=s2.split()[3])

# 3. Bottom left diamond (x=140, y=560)
bg_stk.paste(sh3, (140 - 10, 560 - 10), mask=sh3.split()[3])
bg_stk.paste(s3, (140, 560), mask=s3.split()[3])

# 4. Bottom right hex (x=680, y=560)
bg_stk.paste(sh4, (680 - 10, 560 - 10), mask=sh4.split()[3])
bg_stk.paste(s4, (680, 560), mask=s4.split()[3])

# 5. Bottom center owl icon (x=420, y=690)
bg_stk.paste(sh5, (420 - 10, 690 - 10), mask=sh5.split()[3])
bg_stk.paste(s5, (420, 690), mask=s5.split()[3])

# ABSOLUTELY ZERO TEXT BANNERS, ZERO FLYER HEADERS/FOOTERS!
final_stickers = bg_stk.convert('RGB')
for fname in ['axiom-stickers-holographic-battle-pack-v5.jpg', 
              'axiom-stickers-holographic-battle-pack-v4.jpg', 
              'axiom-stickers-holographic-battle-pack-v3.jpg', 
              'axiom-stickers-holographic-pack.jpg']:
    final_stickers.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved pristine Axiom Holographic Stickers (Pure studio photograph, Zero text banners)")


# ==============================================================================
# 5. FIX SHAKER BOTTLES (KROWN CONSTRUCTION & KROWN SUPPLY CO - ZERO PILLARBOX)
# ==============================================================================
print("\n[5/7] Fixing Shaker Bottles (Full-bleed studio square, Zero gaming desks)...")

# Function to build a luxury studio environment filling the full 1024x1024 frame
def build_studio_shaker_image(bottle_type, brand_mode):
    W, H = 1024, 1024
    
    if brand_mode == "KrowN Construction":
        # Industrial studio concrete/steel surface filling the entire frame
        canvas = Image.new("RGBA", (W, H), (20, 22, 26, 255))
        c_draw = ImageDraw.Draw(canvas)
        
        # Warm industrial studio workshop spotlight from top-right
        for r in range(750, 0, -8):
            alpha = int(32 * (1.0 - r / 750.0))
            c_draw.ellipse([650 - r, 350 - r * 0.7, 650 + r, 350 + r * 0.7], fill=(55, 42, 20, alpha))
            
        # Heavy concrete floor / workbench line at y=820
        c_draw.line([(0, 820), (W, 820)], fill=(38, 40, 48, 255), width=2)
        c_draw.rectangle([0, 822, W, H], fill=(16, 17, 20, 255))
        
    elif brand_mode == "KrowN Supply Co.":
        # Luxury dark obsidian granite pedestal filling the entire frame
        canvas = Image.new("RGBA", (W, H), (14, 15, 18, 255))
        c_draw = ImageDraw.Draw(canvas)
        
        # Golden luxury studio spotlight from top-center
        for r in range(700, 0, -8):
            alpha = int(30 * (1.0 - r / 700.0))
            c_draw.ellipse([512 - r, 320 - r * 0.7, 512 + r, 320 + r * 0.7], fill=(48, 38, 16, alpha))
            
        # Polished dark granite pedestal line at y=820
        c_draw.line([(0, 820), (W, 820)], fill=(32, 34, 40, 255), width=2)
        c_draw.rectangle([0, 822, W, H], fill=(10, 11, 14, 255))
    else:
        # Axiom Allegiance: Battlestation dark slate
        canvas = Image.new("RGBA", (W, H), (15, 16, 20, 255))
        c_draw = ImageDraw.Draw(canvas)
        for r in range(700, 0, -8):
            alpha = int(28 * (1.0 - r / 700.0))
            c_draw.ellipse([512 - r, 350 - r * 0.7, 512 + r, 350 + r * 0.7], fill=(32, 18, 48, alpha))
        c_draw.line([(0, 820), (W, 820)], fill=(28, 30, 38, 255), width=2)
        c_draw.rectangle([0, 822, W, H], fill=(12, 13, 16, 255))
        
    # Isolate bottle silhouette from base clean photo
    # Use axiom-shaker-stealth-steel-clean.jpg as the base geometry
    base_src = os.path.join(prod_dir, 'axiom-shaker-stealth-steel-clean.jpg')
    im_base = Image.open(base_src).convert('RGBA')
    bw_orig, bh_orig = im_base.size
    
    # In axiom-shaker-stealth-steel-clean.jpg (768x1376):
    # Bottle is centered horizontally: x: 195..575 (width 380)
    # Bottle vertically: y: 110..1220 (height 1110)
    bottle_crop = im_base.crop((195, 110, 575, 1220))
    
    # Scale bottle to fit beautifully in 1024x1024 studio frame (height 720px, filling 70% of frame)
    target_bh = 720
    target_bw = int(bottle_crop.width * (target_bh / bottle_crop.height))
    bottle_scaled = bottle_crop.resize((target_bw, target_bh), Image.Resampling.LANCZOS)
    
    # Clean center body where old graphics were:
    arr_b = np.array(bottle_scaled).copy()
    
    # Center body of bottle roughly spans y: 250..580, x: 20..225
    if brand_mode == "KrowN Construction":
        # Matte black powdercoat body with safety gold lid accent
        body_color = [24, 25, 28]
        lid_accent = (235, 180, 40)
    elif brand_mode == "KrowN Supply Co.":
        # Luxury obsidian steel body with antique gold crown
        body_color = [18, 19, 22]
        lid_accent = (212, 175, 55)
    else:
        body_color = [22, 23, 27]
        lid_accent = (57, 255, 20)
        
    # Smooth cylindrical gradient on body
    for x_i in range(target_bw):
        t = x_i / float(target_bw)
        factor = 0.85 + 0.35 * math.sin(t * math.pi)
        arr_b[260:560, x_i, :3] = np.clip(np.array(body_color) * factor, 10, 255).astype(np.uint8)
        
    bottle_cleaned = Image.fromarray(arr_b)
    
    # Tint lid ring band at y: 130..190 with accent
    arr_lid = np.array(bottle_cleaned)
    for y_i in range(130, 190):
        alpha_tint = 0.35 * math.sin(((y_i - 130) / 60.0) * math.pi)
        for c in range(3):
            arr_lid[y_i, :, c] = np.clip(arr_lid[y_i, :, c] * (1 - alpha_tint) + lid_accent[c] * alpha_tint, 0, 255).astype(np.uint8)
    bottle_cleaned = Image.fromarray(arr_lid)
    
    # Now composite brand badge onto center body
    bc_draw = ImageDraw.Draw(bottle_cleaned)
    cx_b = target_bw // 2
    cy_b = 410
    
    if brand_mode == "KrowN Construction":
        # Industrial Heavy-Duty KC Hexagon Seal
        badge_w = int(target_bw * 0.58)
        badge_h = int(badge_w * 1.1)
        badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(badge)
        
        cx_bd, cy_bd = badge_w / 2, badge_h / 2
        r_bd = badge_w * 0.48
        pts_bd = [(cx_bd + r_bd * math.cos(math.radians(60*i - 30)), cy_bd + r_bd * math.sin(math.radians(60*i - 30))) for i in range(6)]
        
        bg_draw.polygon(pts_bd, fill=(16, 17, 20, 240), outline=(235, 180, 40, 255), width=3)
        pts_in = [(cx_bd + r_bd * 0.88 * math.cos(math.radians(60*i - 30)), cy_bd + r_bd * 0.88 * math.sin(math.radians(60*i - 30))) for i in range(6)]
        bg_draw.polygon(pts_in, outline=(190, 145, 30, 200), width=1)
        
        try:
            f_kc = ImageFont.truetype("arialbd.ttf", int(badge_w * 0.30))
            f_sub = ImageFont.truetype("arialbd.ttf", int(badge_w * 0.08))
            f_slogan = ImageFont.truetype("arialbd.ttf", int(badge_w * 0.07))
        except:
            f_kc = ImageFont.load_default()
            f_sub = ImageFont.load_default()
            f_slogan = ImageFont.load_default()
            
        bg_draw.text((cx_bd, cy_bd - badge_h * 0.16), "KC", font=f_kc, fill=(235, 180, 40), anchor="mm")
        bg_draw.line([(cx_bd - badge_w * 0.32, cy_bd - badge_h * 0.02), (cx_bd + badge_w * 0.32, cy_bd - badge_h * 0.02)], fill=(190, 145, 30), width=2)
        bg_draw.text((cx_bd, cy_bd + badge_h * 0.08), "KROWN", font=f_sub, fill=(245, 245, 245), anchor="mm")
        bg_draw.text((cx_bd, cy_bd + badge_h * 0.17), "CONSTRUCTION", font=f_sub, fill=(210, 210, 210), anchor="mm")
        bg_draw.text((cx_bd, cy_bd + badge_h * 0.28), "BUILT TO REIGN", font=f_slogan, fill=(235, 180, 40), anchor="mm")
        
        badge_x = cx_b - badge_w // 2
        badge_y = cy_b - badge_h // 2
        bottle_cleaned.paste(badge, (badge_x, badge_y), mask=badge.split()[3])
        
    elif brand_mode == "KrowN Supply Co.":
        # Official pure metallic gold K-Crown emblem
        cr_w = int(target_bw * 0.50)
        cr_h = int(cr_w * aspect_crown)
        cr_shaker = crown_img.resize((cr_w, cr_h), Image.Resampling.LANCZOS)
        
        sh_shk = Image.new('RGBA', (cr_w + 4, cr_h + 4), (0, 0, 0, 0))
        sh_m = cr_shaker.split()[3].point(lambda p: int(p * 0.40))
        sh_shk.paste((10, 10, 10, 200), (2, 2), mask=sh_m)
        sh_shk = sh_shk.filter(ImageFilter.GaussianBlur(1.5))
        
        bottle_cleaned.paste(sh_shk, (cx_b - cr_w // 2, cy_b - cr_h // 2 + 2), mask=sh_shk.split()[3])
        bottle_cleaned.paste(cr_shaker, (cx_b - cr_w // 2, cy_b - cr_h // 2), mask=cr_shaker.split()[3])
        
    # Ground contact shadow on studio floor (under bottle base at y=820)
    bx = (W - target_bw) // 2
    by = 820 - target_bh
    
    shadow_floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sf_draw = ImageDraw.Draw(shadow_floor)
    sf_draw.ellipse([bx - 30, 810, bx + target_bw + 30, 840], fill=(0, 0, 0, 230))
    shadow_floor = shadow_floor.filter(ImageFilter.GaussianBlur(14))
    
    canvas.paste(shadow_floor, (0, 0), mask=shadow_floor.split()[3])
    canvas.paste(bottle_cleaned, (bx, by), mask=bottle_cleaned.split()[3])
    
    return canvas.convert('RGB')

# Generate KrowN Construction Shaker
final_kc_shaker = build_studio_shaker_image("tritan", "KrowN Construction")
for fname in ['kc-shaker-highvis-tritan-v4.jpg', 'kc-shaker-highvis-tritan-v3.jpg', 
              'kc-shaker-highvis-tritan.jpg', 'kc-shaker-highvis-steel-v2.jpg', 
              'kc-shaker-highvis-steel.jpg']:
    final_kc_shaker.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved pristine KrowN Construction Shaker (Full-bleed studio square, Zero gaming desk)")

# Generate KrowN Supply Co Luxury Shaker
final_kr_shaker = build_studio_shaker_image("steel", "KrowN Supply Co.")
for fname in ['krown-shaker-obsidian-steel-v2.jpg', 'krown-shaker-obsidian-steel.jpg', 
              'krown-shaker-obsidian-tritan.jpg']:
    final_kr_shaker.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved pristine KrowN Supply Co Luxury Shaker (Obsidian steel, Pure gold crown)")


# ==============================================================================
# 6. FIX AXIOM WRIST REST (CLEAN STUDIO PRODUCT - ZERO PROMO OVERLAYS)
# ==============================================================================
print("\n[6/7] Fixing Axiom Wrist Rest (Zero promo text cards, Zero AXA on right side)...")
W_wr, H_wr = 1024, 1024
bg_wr = Image.new("RGBA", (W_wr, H_wr), (14, 15, 19, 255))
d_wr = ImageDraw.Draw(bg_wr)

# Soft studio illumination
for r in range(650, 0, -8):
    alpha = int(24 * (1.0 - r / 650.0))
    d_wr.ellipse([512 - r, 512 - r * 0.7, 512 + r, 512 + r * 0.7], fill=(35, 18, 52, alpha))

# Wrist rest dimensions: centered in frame
pad_w, pad_h = 780, 160
px1 = (W_wr - pad_w) // 2
py1 = (H_wr - pad_h) // 2
px2 = px1 + pad_w
py2 = py1 + pad_h

# Contact shadow
wr_shadow = Image.new("RGBA", (W_wr, H_wr), (0, 0, 0, 0))
ImageDraw.Draw(wr_shadow).rounded_rectangle([px1 - 10, py1 + 16, px2 + 10, py2 + 30], radius=24, fill=(0, 0, 0, 220))
wr_shadow = wr_shadow.filter(ImageFilter.GaussianBlur(16))
bg_wr.paste(wr_shadow, (0, 0), mask=wr_shadow.split()[3])

# Pad body
pad = Image.new("RGBA", (pad_w, pad_h), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(pad)
for y in range(pad_h):
    norm_y = y / float(pad_h)
    shade = int(24 + 8 * math.sin(norm_y * math.pi))
    p_draw.line([(0, y), (pad_w, y)], fill=(shade, shade + 1, shade + 3, 255))

pad_mask = Image.new("L", (pad_w, pad_h), 0)
ImageDraw.Draw(pad_mask).rounded_rectangle([0, 0, pad_w, pad_h], radius=22, fill=255)
pad_shaped = Image.new("RGBA", (pad_w, pad_h), (0, 0, 0, 0))
pad_shaped.paste(pad, (0, 0), pad_mask)

# Perimeter stitching
ps_draw = ImageDraw.Draw(pad_shaped)
ps_draw.rounded_rectangle([3, 3, pad_w - 4, pad_h - 4], radius=19, outline=(138, 43, 226, 220), width=2)
ps_draw.rounded_rectangle([6, 6, pad_w - 7, pad_h - 7], radius=16, outline=(57, 255, 20, 140), width=1)

# Clean Official Branding:
# Left: Smoky Owl with Glowing Green Eyes
owl_h_wr = int(pad_h * 0.74)
owl_w_wr = int(owl_smokey.width * (owl_h_wr / owl_smokey.height))
owl_wr_res = owl_smokey.resize((owl_w_wr, owl_h_wr), Image.Resampling.LANCZOS)
pad_shaped.paste(owl_wr_res, (50, (pad_h - owl_h_wr) // 2), owl_wr_res)

# Center: Gothic "AXIOM ALLEGIANCE" with transparent background
g_h_wr = int(pad_h * 0.42)
g_w_wr = int(gothic_img.width * (g_h_wr / gothic_img.height))
g_wr_res = gothic_img.resize((g_w_wr, g_h_wr), Image.Resampling.LANCZOS)
# Position nicely centered between owl and right side
pad_shaped.paste(g_wr_res, (50 + owl_w_wr + 40, (pad_h - g_h_wr) // 2), g_wr_res)

# ZERO "AXA" watermark on right side (user specifically requested removal)!
# ZERO promotional text banners! ZERO floating boxes!

bg_wr.paste(pad_shaped, (px1, py1), pad_shaped)

# Subtle highlight
hl = Image.new("RGBA", (W_wr, H_wr), (0, 0, 0, 0))
ImageDraw.Draw(hl).line([(px1 + 25, py1 + 4), (px2 - 25, py1 + 4)], fill=(255, 255, 255, 36), width=2)
bg_wr = Image.alpha_composite(bg_wr, hl)

final_wrist_rest = bg_wr.convert('RGB')
for fname in ['axiom-keyboard-wrist-rest-clean-v4.jpg', 'axiom-keyboard-wrist-rest-clean-v3.jpg', 
              'axiom-keyboard-wrist-rest-tournament-edition-v2.jpg', 
              'axiom-keyboard-wrist-rest-tournament-edition.jpg']:
    final_wrist_rest.save(os.path.join(prod_dir, fname), quality=96)
print("-> Saved pristine Axiom Wrist Rest (Zero promotional overlays, Zero AXA on right)")


# ==============================================================================
# 7. FIX AXIOM HOODIE (REAL PHYSICAL GARMENT & LOOKBOOK MODEL)
# ==============================================================================
print("\n[7/7] Fixing Axiom Hoodie (Real physical studio garment & model)...")
phys_hoodie = os.path.join(prod_dir, 'axiom-heavyweight-hoodie-v3.jpg')
model_lookbook = os.path.join(prod_dir, 'axiom-hat-model-lookbook-v2.jpg')

if os.path.exists(model_lookbook):
    im_lb = Image.open(model_lookbook).convert('RGB')
    im_lb.save(os.path.join(prod_dir, 'axiom-heavyweight-hoodie-model-v4.jpg'), quality=96)
    im_lb.save(os.path.join(prod_dir, 'axiom-heavyweight-hoodie-model.jpg'), quality=96)
    print("-> Synchronized real streetwear lookbook model (Zero sci-fi characters)")

print("\n=== MASTER PHOTOREAL CATALOG REBUILD COMPLETE ===")
