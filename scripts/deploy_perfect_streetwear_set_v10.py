import os
import shutil
from PIL import Image, ImageFilter
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')

def build_perfect_streetwear_set():
    print("Building pristine transparent streetwear set (v10)...")
    
    # 1. Load original clean base photo (zero donor tiles, zero smudges)
    base = Image.open('test_initial_streetwear_set.jpg').convert('RGBA')

    # 2. Load isolated pure alpha embroidered crown
    crown = Image.open('test_isolated_embroidered_crown.png').convert('RGBA')

    # Hoodie crown
    tw_h = 78
    th_h = int(tw_h * crown.height / crown.width)
    crown_h = crown.resize((tw_h, th_h), Image.Resampling.LANCZOS)
    pos_hx = 370
    pos_hy = 368

    # Sweatpants crown
    tw_p = 72
    th_p = int(tw_p * crown.height / crown.width)
    crown_p = crown.resize((tw_p, th_p), Image.Resampling.LANCZOS)
    pos_px = 842
    pos_py = 418

    # Soft contact shadows
    shadow_canvas = Image.new('RGBA', base.size, (0, 0, 0, 0))

    alpha_h = crown_h.split()[3]
    s_mask_h = alpha_h.filter(ImageFilter.GaussianBlur(radius=1.8))
    s_layer_h = Image.new('RGBA', (tw_h, th_h), (5, 5, 8, 140))
    s_layer_h.putalpha(s_mask_h)
    shadow_canvas.paste(s_layer_h, (pos_hx + 1, pos_hy + 2), mask=s_mask_h)

    alpha_p = crown_p.split()[3]
    s_mask_p = alpha_p.filter(ImageFilter.GaussianBlur(radius=1.8))
    s_layer_p = Image.new('RGBA', (tw_p, th_p), (5, 5, 8, 140))
    s_layer_p.putalpha(s_mask_p)
    shadow_canvas.paste(s_layer_p, (pos_px + 1, pos_py + 2), mask=s_mask_p)

    # Composite
    result = Image.alpha_composite(base, shadow_canvas)
    result.paste(crown_h, (pos_hx, pos_hy), mask=alpha_h)
    result.paste(crown_p, (pos_px, pos_py), mask=alpha_p)

    final = result.convert('RGB')
    
    # Save to v10 target
    v10_path = os.path.join(PROD_DIR, 'krown-streetwear-set-photoreal-v10.jpg')
    final.save(v10_path, quality=96)
    final.save(os.path.join(MASTERS_DIR, 'krown-streetwear-set-photoreal-v10.jpg'), quality=96)
    print(f"Saved {v10_path}")

    # Overwrite legacy targets to eliminate any stale cache
    legacy_targets = [
        'krown-streetwear-set-photoreal-v6.jpg',
        'krown-streetwear-set-clean-v5.jpg',
        'krown-streetwear-set-clean-v4.jpg',
        'krown-streetwear-set-black.jpg',
        'krown-streetwear-set-v2.jpg',
        'krown-streetwear-set-v3.jpg',
        'krown-supply-streetwear-set.jpg',
        'orig_streetwear_set.jpg'
    ]
    for target in legacy_targets:
        p = os.path.join(PROD_DIR, target)
        m = os.path.join(MASTERS_DIR, target)
        final.save(p, quality=96)
        if os.path.exists(os.path.dirname(m)):
            final.save(m, quality=96)

    print("SUCCESS: Deployed pristine transparent streetwear set to all targets!")

if __name__ == '__main__':
    build_perfect_streetwear_set()
