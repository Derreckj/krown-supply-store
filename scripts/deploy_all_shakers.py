from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import os

# Base obsidian image we just perfected
base_obsidian = Image.open('test_krown_luxury_shaker_final.jpg').convert('RGB')
w, h = base_obsidian.size

prod_dir = 'public/images/products'

# 1. Save Obsidian Black master:
base_obsidian.save(os.path.join(prod_dir, 'krown-shaker-photoreal-v6.jpg'), quality=96)
base_obsidian.save(os.path.join(prod_dir, 'krown-shaker-obsidian-steel.jpg'), quality=96)
base_obsidian.save(os.path.join(prod_dir, 'krown-shaker-obsidian-tritan.jpg'), quality=96)
base_obsidian.save(os.path.join(prod_dir, 'krown-shaker-obsidian-steel-v2.jpg'), quality=96)

# 2. Create Brushed Steel edition:
# Increase luminance of bottle cylinder (x: 335 to 665, y: 140 to 830)
arr_steel = np.array(base_obsidian, dtype=np.float32)
for y in range(180, 830):
    for x in range(335, 665):
        # Brushed stainless steel has neutral silver tint + vertical hairline grain
        r, g, b = arr_steel[y, x]
        # Boost brightness into steel range (~110-155)
        lum = 0.299*r + 0.587*g + 0.114*b
        # Don't wash out the gold crown / gold text (gold has high R, low B)
        is_gold = (r > 120 and r > b * 1.35)
        if not is_gold:
            steel_lum = np.clip(lum * 2.8 + 60, 40, 190)
            arr_steel[y, x] = [steel_lum, steel_lum * 1.02, steel_lum * 1.05]

im_steel = Image.fromarray(arr_steel.astype(np.uint8), mode='RGB')
im_steel.save(os.path.join(prod_dir, 'krown-shaker-brushed-v6.jpg'), quality=96)
im_steel.save(os.path.join(prod_dir, 'krown-shaker-brushed-steel.jpg'), quality=96)
im_steel.save(os.path.join(prod_dir, 'krown-shaker-brushed-tritan.jpg'), quality=96)

# 3. Create Frosted Smoke edition:
arr_smoke = np.array(base_obsidian, dtype=np.float32)
for y in range(180, 830):
    for x in range(335, 665):
        r, g, b = arr_smoke[y, x]
        is_gold = (r > 120 and r > b * 1.35)
        if not is_gold:
            lum = 0.299*r + 0.587*g + 0.114*b
            smoke_lum = np.clip(lum * 1.6 + 25, 20, 120)
            arr_smoke[y, x] = [smoke_lum * 0.95, smoke_lum, smoke_lum * 1.05]

im_smoke = Image.fromarray(arr_smoke.astype(np.uint8), mode='RGB')
im_smoke.save(os.path.join(prod_dir, 'krown-shaker-smoke-v6.jpg'), quality=96)
im_smoke.save(os.path.join(prod_dir, 'krown-shaker-smoke-steel.jpg'), quality=96)
im_smoke.save(os.path.join(prod_dir, 'krown-shaker-smoke-tritan.jpg'), quality=96)

# 4. KrowN Construction Shakers:
# Ensure ALL variants of kc-shaker on disk use kc-shaker-photoreal-v6.jpg
im_kc = Image.open(os.path.join(prod_dir, 'kc-shaker-photoreal-v6.jpg')).convert('RGB')
im_kc.save(os.path.join(prod_dir, 'kc-shaker-steelcore-v6.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-tradesman-v6.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-jobsite-steel.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-jobsite-tritan.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-steelcore-steel.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-steelcore-tritan.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-highvis-steel.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-highvis-tritan.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-highvis-steel-v2.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-highvis-tritan-v3.jpg'), quality=96)
im_kc.save(os.path.join(prod_dir, 'kc-shaker-highvis-tritan-v4.jpg'), quality=96)

print("All KrowN Supply Co and KrowN Construction shakers updated across all variant files!")
