import os
import shutil
import math
import numpy as np
from PIL import Image, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')

os.makedirs(PROD_DIR, exist_ok=True)
os.makedirs(MASTERS_DIR, exist_ok=True)

def save_all_targets(img, basename):
    for ver in ['v10', 'v9', 'v8', 'v6']:
        fname = f"{basename}-{ver}.jpg"
        img.save(os.path.join(PROD_DIR, fname), quality=96)
        img.save(os.path.join(MASTERS_DIR, fname), quality=96)
        print(f"Saved: {fname}")

def fix_kc_shakers():
    print("\n--- Fixing KC Shakers: 100% Photorealistic, Zero Artificial Rectangles ---")
    tumbler_20oz_path = os.path.join(PROD_DIR, 'krown-construction-jobsite-tumbler.jpg')
    tumbler_32oz_path = os.path.join(PROD_DIR, 'krown-construction-jobsite-tumbler-32oz.jpg')

    # 1. High-Vis Safety Gold & Matte Black
    # Use the clean 20oz master with rich gold KrowN Construction emblem on matte black
    im_hv = Image.open(tumbler_20oz_path).convert('RGB')
    arr_hv = np.array(im_hv, dtype=np.float32)
    # Enhance the gold logo vibrance smoothly
    for y in range(320, 600):
        for x in range(370, 660):
            r, g, b = arr_hv[y, x]
            if r > 95 and g > 75 and b < 95 and (r > b + 25):
                lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
                arr_hv[y, x] = [
                    int(min(255, 255 * lum + 35)),
                    int(min(255, 205 * lum + 25)),
                    int(min(255, 30 * lum + 5))
                ]
    im_hv_clean = Image.fromarray(arr_hv.astype(np.uint8))
    save_all_targets(im_hv_clean, 'kc-shaker-photoreal')

    # 2. Industrial Brushed Stainless Steel & Concrete Grey
    # Brushed double-wall stainless steel body with laser-etched KrowN Construction emblem
    master_clean = Image.open(tumbler_20oz_path).convert('RGB')
    arr_master = np.array(master_clean, dtype=np.float32)
    steel_arr = arr_master.copy()
    np.random.seed(42)
    logo_mask = (arr_master[:, :, 0] > 95) & (arr_master[:, :, 1] > 75) & (arr_master[:, :, 2] < 95) & (arr_master[:, :, 0] > arr_master[:, :, 2] + 25)

    def get_bounds(y):
        if y < 240 or y > 855: return None, None
        if y <= 530: return 340, 680
        elif y <= 600:
            t = (y - 530) / 70.0
            return int(340 + t * 25), int(680 - t * 25)
        else:
            t = (y - 600) / 255.0
            return int(365 + t * 7), int(655 - t * 5)

    for y in range(240, 855):
        xl, xr = get_bounds(y)
        bw = xr - xl
        noise_row = np.random.normal(0, 1.2, size=(1024,))
        for x in range(xl, xr):
            norm_x = (x - xl) / float(bw)
            cyl_light = 0.65 + 0.38 * math.sin(norm_x * math.pi) + 0.18 * math.exp(-((norm_x - 0.42)**2) / 0.035)
            r_val = np.clip(135 * cyl_light + noise_row[x], 0, 255)
            g_val = np.clip(140 * cyl_light + noise_row[x], 0, 255)
            b_val = np.clip(148 * cyl_light + noise_row[x], 0, 255)

            edge_dist = min(x - xl, xr - x, y - 240, 855 - y)
            w_blend = min(1.0, edge_dist / 6.0)

            if logo_mask[y, x]:
                steel_arr[y, x] = [38, 40, 44] # laser etched titanium
            else:
                steel_arr[y, x] = (1.0 - w_blend) * steel_arr[y, x] + w_blend * np.array([r_val, g_val, b_val])

    im_sc_clean = Image.fromarray(steel_arr.astype(np.uint8))
    save_all_targets(im_sc_clean, 'kc-shaker-steelcore')

    # 3. Tradesman Heavy-Duty Obsidian
    # Use the clean 32oz heavy-duty tumbler master with zero alterations!
    im_tb_clean = Image.open(tumbler_32oz_path).convert('RGB')
    save_all_targets(im_tb_clean, 'kc-shaker-tradesman')

    print("\nAll KC Shaker targets fixed and deployed with zero artificial rectangles!")

if __name__ == '__main__':
    fix_kc_shakers()
