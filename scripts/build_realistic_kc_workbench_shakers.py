import os
import math
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')

# Load the master workbench photograph (the tumbler that the user loves)
master = Image.open('test_commit_88c_kc.jpg').convert('RGB')
arr_master = np.array(master, dtype=np.float32)

# Load isolated gold logo
logo_rgba = Image.open('test_kc_isolated_logo_v2.png').convert('RGBA')

# Bottle silhouette function
def get_bottle_bounds(y):
    if y < 225 or y > 855:
        return None, None
    if y <= 530:
        return 340, 680
    elif y <= 600:
        t = (y - 530) / 70.0
        return int(340 + t * 25), int(680 - t * 25)
    else:
        t = (y - 600) / 255.0
        return int(365 + t * 7), int(655 - t * 5)

# -------------------------------------------------------------------------
# VARIANT 1: High-Vis Safety Gold & Matte Black
# -------------------------------------------------------------------------
def make_highvis():
    # Take master, boost the gold logo vibrance and luminescence to High-Vis Safety Gold
    hv = arr_master.copy()
    for y in range(300, 620):
        for x in range(340, 680):
            r, g, b = hv[y, x]
            # Detect gold logo
            if r > 90 and g > 70 and b < 90 and (r > b + 20) and (g > b + 10):
                lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
                # Vibrant high-vis safety gold
                hv[y, x] = [
                    int(min(255, 245 * lum + 35)),
                    int(min(255, 200 * lum + 25)),
                    int(min(255, 30 * lum + 5))
                ]
    return Image.fromarray(hv.astype(np.uint8))

# -------------------------------------------------------------------------
# VARIANT 2: Industrial Steel & Concrete Grey
# -------------------------------------------------------------------------
def make_steelcore():
    steel_arr = arr_master.copy()
    np.random.seed(42)

    for y in range(225, 855):
        xl, xr = get_bottle_bounds(y)
        bw = xr - xl
        noise_row = np.random.normal(0, 1.6, size=(1024,))
        for x in range(xl, xr):
            norm_x = (x - xl) / float(bw)
            cyl_light = 0.65 + 0.38 * math.sin(norm_x * math.pi) + 0.18 * math.exp(-((norm_x - 0.42)**2) / 0.035)
            
            # Industrial brushed steel / titanium tone
            r_val = np.clip(132 * cyl_light + noise_row[x], 0, 255)
            g_val = np.clip(136 * cyl_light + noise_row[x], 0, 255)
            b_val = np.clip(144 * cyl_light + noise_row[x], 0, 255)
            
            edge_dist = min(x - xl, xr - x, y - 225, 855 - y)
            w_blend = min(1.0, edge_dist / 6.0)
            steel_arr[y, x] = (1.0 - w_blend) * steel_arr[y, x] + w_blend * np.array([r_val, g_val, b_val])

    steel_base = Image.fromarray(steel_arr.astype(np.uint8))
    
    # Overlay the high-contrast laser-etched / gold logo
    # Position of logo in master was x: 345, y: 310
    logo_np = np.array(logo_rgba, dtype=np.float32)
    # Give logo on steel a bold high-contrast laser-etched appearance (deep charcoal with gold bevel)
    logo_etched = np.zeros_like(logo_np)
    alpha = logo_np[:, :, 3] / 255.0
    logo_etched[:, :, 0] = (200 * alpha).astype(np.uint8)
    logo_etched[:, :, 1] = (165 * alpha).astype(np.uint8)
    logo_etched[:, :, 2] = (35 * alpha).astype(np.uint8)
    logo_etched[:, :, 3] = logo_np[:, :, 3].astype(np.uint8)
    
    logo_etched_img = Image.fromarray(logo_etched.astype(np.uint8), mode='RGBA')
    
    # Soft drop shadow for engraving
    shadow_mask = logo_etched_img.split()[3].filter(ImageFilter.GaussianBlur(radius=2.0))
    shadow_layer = Image.new('RGBA', logo_etched_img.size, (15, 18, 22, 190))
    shadow_layer.putalpha(shadow_mask)
    
    steel_base = steel_base.convert('RGBA')
    steel_base.paste(shadow_layer, (345 + 1, 310 + 2), mask=shadow_mask)
    steel_base.paste(logo_etched_img, (345, 310), mask=logo_etched_img.split()[3])
    
    return steel_base.convert('RGB')

# -------------------------------------------------------------------------
# VARIANT 3: Tradesman Heavy-Duty Obsidian
# -------------------------------------------------------------------------
def make_tradesman():
    # Master is already the perfect tradesman heavy-duty obsidian with rich antique bronze-gold
    return Image.fromarray(arr_master.astype(np.uint8))

if __name__ == '__main__':
    im_hv = make_highvis()
    im_sc = make_steelcore()
    im_tb = make_tradesman()

    im_hv.save('test_kc_highvis_final.jpg', quality=96)
    im_sc.save('test_kc_steelcore_final.jpg', quality=96)
    im_tb.save('test_kc_tradesman_final.jpg', quality=96)
    print("All 3 KC workbench shaker images generated!")
