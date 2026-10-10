import os
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw

scratch_dir = r'C:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store'
prod_dir = os.path.join(scratch_dir, 'public', 'images', 'products')
brand_dir = os.path.join(scratch_dir, 'public', 'images', 'branding')

# Load official definitive K-Crown emblem
crown_path = os.path.join(brand_dir, 'official_definitive_crown_transparent.png')
crown_img = Image.open(crown_path).convert('RGBA')

print("Starting generation of photorealistic fixes...")

# ==============================================================================
# 1. FIX KROW N STREETWEAR SET (HOODIE + SWEATPANTS)
# ==============================================================================
print("\n[1/5] Processing KrowN Streetwear Set...")
orig_set_path = os.path.join(prod_dir, 'orig_streetwear_set.jpg')
im_set = Image.open(orig_set_path).convert('RGB')
arr_set = np.array(im_set).copy()

# The image has dimensions 1024x1024
# Clean circular badge and cartoon crown on hoodie chest:
# Center around y=405, x=400, radius 40
Y, X = np.ogrid[:1024, :1024]
dist_h = np.sqrt((X - 400)**2 + (Y - 405)**2)
mask_h = np.clip((42 - dist_h) / 8.0, 0, 1)[:, :, None]

# Donor fabric from clean upper chest fabric: y: 320..365, x: 375..425
donor_h = arr_set[320:365, 375:425]
donor_h_tile = np.tile(donor_h, (3, 3, 1))[:84, :84]
patch_h = arr_set[405-42:405+42, 400-42:400+42]
arr_set[405-42:405+42, 400-42:400+42] = (donor_h_tile * mask_h[405-42:405+42, 400-42:400+42] + patch_h * (1 - mask_h[405-42:405+42, 400-42:400+42])).astype(np.uint8)

# Clean sweatpants thigh:
# Center around y=440, x=870, radius 45
dist_p = np.sqrt((X - 870)**2 + (Y - 440)**2)
mask_p = np.clip((46 - dist_p) / 8.0, 0, 1)[:, :, None]

donor_p = arr_set[370:415, 845:895]
donor_p_tile = np.tile(donor_p, (3, 3, 1))[:92, :92]
patch_p = arr_set[440-46:440+46, 870-46:870+46]
arr_set[440-46:440+46, 870-46:870+46] = (donor_p_tile * mask_p[440-46:440+46, 870-46:870+46] + patch_p * (1 - mask_p[440-46:440+46, 870-46:870+46])).astype(np.uint8)

# Clean sweatpants fly/crotch area:
# Center around y=430, x=700, radius 35
dist_f = np.sqrt((X - 700)**2 + (Y - 430)**2)
mask_f = np.clip((35 - dist_f) / 8.0, 0, 1)[:, :, None]
donor_f = arr_set[350:390, 680:720]
donor_f_tile = np.tile(donor_f, (3, 3, 1))[:70, :70]
patch_f = arr_set[430-35:430+35, 700-35:700+35]
arr_set[430-35:430+35, 700-35:700+35] = (donor_f_tile * mask_f[430-35:430+35, 700-35:700+35] + patch_f * (1 - mask_f[430-35:430+35, 700-35:700+35])).astype(np.uint8)

clean_set_img = Image.fromarray(arr_set).convert('RGBA')

# Now apply ONE official metallic K-Crown emblem to hoodie chest
aspect = crown_img.height / crown_img.width
cw_h = 68
ch_h = int(cw_h * aspect)
crown_hoodie = crown_img.resize((cw_h, ch_h), Image.Resampling.LANCZOS)

# Subtle shadow for embroidery realism
shadow_h = Image.new('RGBA', (cw_h + 6, ch_h + 6), (0, 0, 0, 0))
shadow_mask = crown_hoodie.split()[3].point(lambda p: int(p * 0.45))
shadow_h.paste((10, 10, 10, 200), (3, 3), mask=shadow_mask)
shadow_h = shadow_h.filter(ImageFilter.GaussianBlur(1.5))

clean_set_img.paste(shadow_h, (366, 372), mask=shadow_h.split()[3])
clean_set_img.paste(crown_hoodie, (368, 370), mask=crown_hoodie.split()[3])

# Apply ONE official metallic K-Crown emblem to sweatpants upper left thigh
cw_p = 64
ch_p = int(cw_p * aspect)
crown_pants = crown_img.resize((cw_p, ch_p), Image.Resampling.LANCZOS)

shadow_p = Image.new('RGBA', (cw_p + 6, ch_p + 6), (0, 0, 0, 0))
shadow_mask_p = crown_pants.split()[3].point(lambda p: int(p * 0.45))
shadow_p.paste((10, 10, 10, 200), (3, 3), mask=shadow_mask_p)
shadow_p = shadow_p.filter(ImageFilter.GaussianBlur(1.5))

clean_set_img.paste(shadow_p, (838, 417), mask=shadow_p.split()[3])
clean_set_img.paste(crown_pants, (840, 415), mask=crown_pants.split()[3])

final_set = clean_set_img.convert('RGB')
final_set_path = os.path.join(prod_dir, 'krown-streetwear-set-clean-v5.jpg')
final_set.save(final_set_path, quality=95)
# Also overwrite v4, v3, v2, black, and main file to prevent any cached/stale reference
for fname in ['krown-streetwear-set-clean-v4.jpg', 'krown-streetwear-set-v3.jpg', 'krown-streetwear-set-v2.jpg', 'krown-streetwear-set-black.jpg', 'krown-supply-streetwear-set.jpg']:
    final_set.save(os.path.join(prod_dir, fname), quality=95)
print("Saved clean KrowN Streetwear Set (v5 and synced)")


# ==============================================================================
# 2. FIX KROW N FRENCH TERRY SHORTS (CLEAN V5 WITH OFFICIAL CROWN)
# ==============================================================================
print("\n[2/5] Processing KrowN French Terry Shorts...")
raw_shorts_path = os.path.join(prod_dir, 'krown-french-terry-streetwear-shorts.png')
im_shorts = Image.open(raw_shorts_path).convert('RGB')
arr_shorts = np.array(im_shorts).copy()

# The raw shorts has dimensions 1024x1024
# Clean the thigh badge/cartoon crown at y=520..610, x=500..600:
ys, xs = np.ogrid[:1024, :1024]
dist_sh = np.sqrt((xs - 550)**2 + (ys - 565)**2)
mask_sh = np.clip((48 - dist_sh) / 8.0, 0, 1)[:, :, None]

donor_sh = arr_shorts[430:480, 520:580]
donor_sh_tile = np.tile(donor_sh, (3, 3, 1))[:96, :96]
patch_sh = arr_shorts[565-48:565+48, 550-48:550+48]
arr_shorts[565-48:565+48, 550-48:550+48] = (donor_sh_tile * mask_sh[565-48:565+48, 550-48:550+48] + patch_sh * (1 - mask_sh[565-48:565+48, 550-48:550+48])).astype(np.uint8)

clean_shorts_img = Image.fromarray(arr_shorts).convert('RGBA')

# Now apply official metallic K-Crown emblem
cw_s = 76
ch_s = int(cw_s * aspect)
crown_shorts = crown_img.resize((cw_s, ch_s), Image.Resampling.LANCZOS)

shadow_s = Image.new('RGBA', (cw_s + 6, ch_s + 6), (0, 0, 0, 0))
s_mask = crown_shorts.split()[3].point(lambda p: int(p * 0.45))
shadow_s.paste((10, 10, 10, 200), (3, 3), mask=s_mask)
shadow_s = shadow_s.filter(ImageFilter.GaussianBlur(1.5))

clean_shorts_img.paste(shadow_s, (510, 528), mask=shadow_s.split()[3])
clean_shorts_img.paste(crown_shorts, (512, 526), mask=crown_shorts.split()[3])

final_shorts = clean_shorts_img.convert('RGB')
final_shorts_path = os.path.join(prod_dir, 'krown-french-terry-shorts-clean-v5.jpg')
final_shorts.save(final_shorts_path, quality=95)
for fname in ['krown-french-terry-shorts-clean-v4.jpg', 'krown-french-terry-shorts-v3.jpg', 'krown-french-terry-shorts-v2.jpg', 'krown-french-terry-shorts.jpg']:
    final_shorts.save(os.path.join(prod_dir, fname), quality=95)
print("Saved clean KrowN French Terry Shorts (v5 and synced)")


# ==============================================================================
# 3. BUILD PHOTOREALISTIC KROW N CONSTRUCTION SHAKERS (ZERO AXIOM / ZERO GAMER DESK)
# ==============================================================================
print("\n[3/5] Building photorealistic KrowN Construction Shakers...")
# Master 3-editions lineup studio shot: kc-shaker-bottles-3-editions.jpg (1200x716)
im_kc3 = Image.open(os.path.join(prod_dir, 'kc-shaker-bottles-3-editions.jpg')).convert('RGB')

def make_studio_square(bottle_crop, target_size=1024):
    bw, bh = bottle_crop.size
    arr_b = np.array(bottle_crop)
    # Background color calculation:
    edge_cols = np.concatenate([arr_b[0, :], arr_b[-1, :], arr_b[:, 0], arr_b[:, -1]], axis=0)
    bg_col = edge_cols.mean(axis=0).astype(int)
    
    Y, X = np.ogrid[:target_size, :target_size]
    dist = np.sqrt((X - target_size//2)**2 + (Y - target_size//2)**2)
    max_d = np.sqrt(2 * (target_size//2)**2)
    factor = 1.0 - 0.35 * (dist / max_d)
    bg_canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    for c in range(3):
        bg_canvas[:, :, c] = np.clip(bg_col[c] * factor, 12, 255).astype(np.uint8)
    canvas = Image.fromarray(bg_canvas)
    
    # Scale bottle to fit nicely:
    new_h = 860
    new_w = int(bw * (new_h / bh))
    bottle_scaled = bottle_crop.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Soft border feathering on left/right edges of bottle crop:
    bottle_rgba = bottle_scaled.convert('RGBA')
    arr_brgba = np.array(bottle_rgba)
    feather_w = 20
    alpha_mask = np.ones((new_h, new_w), dtype=np.float32)
    for x in range(feather_w):
        alpha_mask[:, x] = float(x) / feather_w
        alpha_mask[:, new_w - 1 - x] = float(x) / feather_w
    arr_brgba[:, :, 3] = (arr_brgba[:, :, 3] * alpha_mask).astype(np.uint8)
    bottle_feathered = Image.fromarray(arr_brgba)
    
    ox = (target_size - new_w) // 2
    oy = (target_size - new_h) // 2
    canvas.paste(bottle_feathered, (ox, oy), mask=bottle_feathered.split()[3])
    return canvas

# Edition 1: High-Vis Safety Gold & Matte Black
kc_crop_b1 = im_kc3.crop((100, 30, 470, 700))
kc_hero_b1 = make_studio_square(kc_crop_b1)
kc_b1_path = os.path.join(prod_dir, 'kc-shaker-highvis-tritan-v4.jpg')
kc_hero_b1.save(kc_b1_path, quality=95)
# Overwrite previous broken paths
kc_hero_b1.save(os.path.join(prod_dir, 'kc-shaker-highvis-tritan-v3.jpg'), quality=95)
kc_hero_b1.save(os.path.join(prod_dir, 'kc-shaker-highvis-tritan.jpg'), quality=95)
kc_hero_b1.save(os.path.join(prod_dir, 'kc-shaker-highvis-steel.jpg'), quality=95)
kc_hero_b1.save(os.path.join(prod_dir, 'kc-shaker-highvis-steel-v2.jpg'), quality=95)

# Edition 2: Industrial SteelCore Titanium Double-Wall Stainless Steel
kc_crop_b2 = im_kc3.crop((420, 30, 780, 700))
kc_hero_b2 = make_studio_square(kc_crop_b2)
kc_hero_b2.save(os.path.join(prod_dir, 'kc-shaker-steelcore-steel.jpg'), quality=95)
kc_hero_b2.save(os.path.join(prod_dir, 'kc-shaker-steelcore-tritan.jpg'), quality=95)

# Edition 3: Jobsite Tradesman Heavy Duty (Blackout & Slate)
kc_crop_b3 = im_kc3.crop((730, 30, 1100, 700))
kc_hero_b3 = make_studio_square(kc_crop_b3)
kc_hero_b3.save(os.path.join(prod_dir, 'kc-shaker-jobsite-steel.jpg'), quality=95)
kc_hero_b3.save(os.path.join(prod_dir, 'kc-shaker-jobsite-tritan.jpg'), quality=95)
print("Saved photorealistic KrowN Construction Shakers (3 editions)")


# ==============================================================================
# 4. BUILD PHOTOREALISTIC KROW N SUPPLY CO. LUXURY SHAKERS (ZERO FLAT BOX STICKER)
# ==============================================================================
print("\n[4/5] Building photorealistic KrowN Supply Co. Luxury Shakers...")
im_kr3 = Image.open(os.path.join(prod_dir, 'krown-shaker-bottles-3-editions.jpg')).convert('RGB')

# Edition 1: Matte Obsidian Black & Antique Gold Crown
kr_crop_b1 = im_kr3.crop((100, 30, 470, 700))
kr_hero_b1 = make_studio_square(kr_crop_b1)
kr_hero_b1.save(os.path.join(prod_dir, 'krown-shaker-obsidian-tritan.jpg'), quality=95)
kr_hero_b1.save(os.path.join(prod_dir, 'krown-shaker-obsidian-steel.jpg'), quality=95)
kr_hero_b1.save(os.path.join(prod_dir, 'krown-shaker-obsidian-steel-v2.jpg'), quality=95)

# Edition 2: Frosted Smoke Tritan & Polished Gold Crown
kr_crop_b2 = im_kr3.crop((420, 30, 780, 700))
kr_hero_b2 = make_studio_square(kr_crop_b2)
kr_hero_b2.save(os.path.join(prod_dir, 'krown-shaker-smoke-steel.jpg'), quality=95)
kr_hero_b2.save(os.path.join(prod_dir, 'krown-shaker-smoke-tritan.jpg'), quality=95)

# Edition 3: Raw Brushed Steel & Minimal Crown Monogram
kr_crop_b3 = im_kr3.crop((730, 30, 1100, 700))
kr_hero_b3 = make_studio_square(kr_crop_b3)
kr_hero_b3.save(os.path.join(prod_dir, 'krown-shaker-brushed-steel.jpg'), quality=95)
kr_hero_b3.save(os.path.join(prod_dir, 'krown-shaker-brushed-tritan.jpg'), quality=95)
print("Saved photorealistic KrowN Supply Co. Luxury Shakers (3 editions)")


# ==============================================================================
# 5. FIX AXIOM DAD HAT (DARK STUDIO BLEND - ELIMINATE WHITE SQUARE BOX)
# ==============================================================================
print("\n[5/5] Processing Axiom Dad Hat (eliminating harsh white box)...")
dad_hat_path = os.path.join(prod_dir, 'axiom-dad-hat-washed-black-v3.jpg')
im_hat = Image.open(dad_hat_path).convert('RGB')
arr_hat = np.array(im_hat).copy()

# The dad hat is on a stone slab in the center. The surrounding margin is bright [230..245]
# Let's segment the stone slab and hat:
# Stone slab and hat have darker pixels: (R < 195) or (G < 195) or (B < 195)
is_subject = (arr_hat[:, :, 0] < 205) | (arr_hat[:, :, 1] < 205) | (arr_hat[:, :, 2] < 205)

# Create a clean dark studio vignette background (#121418)
Y_h, X_h = np.ogrid[:1024, :1024]
dist_h = np.sqrt((X_h - 512)**2 + (Y_h - 512)**2)
max_dh = np.sqrt(2 * 512**2)
factor_h = 1.0 - 0.4 * (dist_h / max_dh)
dark_bg = np.zeros((1024, 1024, 3), dtype=np.float32)
dark_bg[:, :, 0] = 18 * factor_h
dark_bg[:, :, 1] = 20 * factor_h
dark_bg[:, :, 2] = 24 * factor_h

# Radial transition: stone slab is inside a circle of radius ~360 from (512, 530)
cy_hat, cx_hat = 525, 512
slab_dist = np.sqrt((X_h - cx_hat)**2 + (Y_h - cy_hat)**2)

# Inside slab_dist < 320 is the hat + stone slab
# Between 320 and 420, smoothly vignette the stone slab edges into the dark studio background:
alpha_blend = np.clip((410 - slab_dist) / 90.0, 0, 1)[:, :, None]

# Blend:
arr_hat_f = arr_hat.astype(np.float32)
blended_hat = (arr_hat_f * alpha_blend + dark_bg * (1 - alpha_blend)).astype(np.uint8)

final_hat = Image.fromarray(blended_hat)
final_hat_path = os.path.join(prod_dir, 'axiom-dad-hat-washed-black-v4.jpg')
final_hat.save(final_hat_path, quality=95)
for fname in ['axiom-dad-hat-washed-black-v3.jpg', 'axiom-dad-hat-washed-black-v2.jpg', 'axiom-dad-hat-washed-black.jpg']:
    final_hat.save(os.path.join(prod_dir, fname), quality=95)
print("Saved clean Axiom Dad Hat with seamless dark studio blend (v4 and synced)")

print("\nALL PHOTOREALISTIC FIXES COMPLETE!")
