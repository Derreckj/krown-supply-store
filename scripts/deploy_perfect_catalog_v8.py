import os
import shutil
import math
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')
BRAIN_DIR = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'

os.makedirs(PROD_DIR, exist_ok=True)
os.makedirs(MASTERS_DIR, exist_ok=True)

def copy_and_record(src, dst_name):
    dst = os.path.join(PROD_DIR, dst_name)
    dst_m = os.path.join(MASTERS_DIR, dst_name)
    if isinstance(src, str):
        shutil.copy2(src, dst)
        shutil.copy2(src, dst_m)
    elif isinstance(src, Image.Image):
        src.save(dst, quality=96)
        src.save(dst_m, quality=96)
    print(f"Deployed: {dst_name}")

# =========================================================================
# 1. AXIOM HOODIE 01
# =========================================================================
def deploy_axiom_hoodie():
    print("\n--- Deploying Axiom Allegiance Heavyweight Hoodie (v8) ---")
    studio_src = os.path.join(BRAIN_DIR, 'axiom_hoodie_studio_front_1791592242763.jpg')
    model_src = os.path.join(BRAIN_DIR, 'axiom_hoodie_model_1791592259283.jpg')

    # v8 targets
    copy_and_record(studio_src, 'axiom-heavyweight-hoodie-studio-v8.jpg')
    copy_and_record(model_src, 'axiom-heavyweight-hoodie-model-v8.jpg')

    # Also overwrite old cached names so legacy URLs also serve the pristine photos
    copy_and_record(studio_src, 'axiom-heavyweight-hoodie-photoreal-v6.jpg')
    copy_and_record(studio_src, 'axiom-heavyweight-hoodie-studio.jpg')
    copy_and_record(studio_src, 'axiom-heavyweight-hoodie-v2.jpg')
    copy_and_record(studio_src, 'axiom-heavyweight-hoodie-v3.jpg')
    copy_and_record(model_src, 'axiom-heavyweight-hoodie-model-v6.jpg')
    copy_and_record(model_src, 'axiom-heavyweight-hoodie-model.jpg')

# =========================================================================
# 2. KROWN CONSTRUCTION SHAKER (kc-shaker-01)
# =========================================================================
def deploy_kc_shakers():
    print("\n--- Deploying KrowN Construction Workbench Shakers (v8) ---")
    tumbler_path = os.path.join(PROD_DIR, 'krown-construction-jobsite-tumbler.jpg')
    master = Image.open(tumbler_path).convert('RGB')
    arr_master = np.array(master, dtype=np.float32)

    # 1. High-Vis Safety Gold & Matte Black
    hv = arr_master.copy()
    for y in range(320, 600):
        for x in range(370, 660):
            r, g, b = hv[y, x]
            if r > 95 and g > 75 and b < 95 and (r > b + 25) and (g > b + 10):
                lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
                hv[y, x] = [
                    int(min(255, 255 * lum + 40)),
                    int(min(255, 205 * lum + 30)),
                    int(min(255, 30 * lum + 5))
                ]
    im_hv = Image.fromarray(hv.astype(np.uint8))

    # 2. Industrial Steel & Concrete Grey
    # Steel cylindrical body blending with laser-etched charcoal/gold seal
    steel_arr = arr_master.copy()
    np.random.seed(42)
    # Extract logo mask
    logo_mask = (arr_master[:, :, 0] > 95) & (arr_master[:, :, 1] > 75) & (arr_master[:, :, 2] < 95) & (arr_master[:, :, 0] > arr_master[:, :, 2] + 25)

    def get_bounds(y):
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

    for y in range(225, 855):
        xl, xr = get_bounds(y)
        bw = xr - xl
        noise_row = np.random.normal(0, 1.5, size=(1024,))
        for x in range(xl, xr):
            norm_x = (x - xl) / float(bw)
            cyl_light = 0.65 + 0.38 * math.sin(norm_x * math.pi) + 0.18 * math.exp(-((norm_x - 0.42)**2) / 0.035)
            r_val = np.clip(135 * cyl_light + noise_row[x], 0, 255)
            g_val = np.clip(140 * cyl_light + noise_row[x], 0, 255)
            b_val = np.clip(148 * cyl_light + noise_row[x], 0, 255)

            edge_dist = min(x - xl, xr - x, y - 225, 855 - y)
            w_blend = min(1.0, edge_dist / 6.0)

            # Keep logo area visible with etched contrast
            if logo_mask[y, x]:
                # laser etched dark titanium with gold luster
                steel_arr[y, x] = [35, 38, 42]
            else:
                steel_arr[y, x] = (1.0 - w_blend) * steel_arr[y, x] + w_blend * np.array([r_val, g_val, b_val])

    im_sc = Image.fromarray(steel_arr.astype(np.uint8))

    # 3. Tradesman Heavy-Duty Obsidian
    im_tb = master.copy()

    # Save v8 files
    copy_and_record(im_hv, 'kc-shaker-photoreal-v8.jpg')
    copy_and_record(im_sc, 'kc-shaker-steelcore-v8.jpg')
    copy_and_record(im_tb, 'kc-shaker-tradesman-v8.jpg')

    # Also overwrite old v6 files so any lingering requests get the clean workbench shots
    copy_and_record(im_hv, 'kc-shaker-photoreal-v6.jpg')
    copy_and_record(im_sc, 'kc-shaker-steelcore-v6.jpg')
    copy_and_record(im_tb, 'kc-shaker-tradesman-v6.jpg')

# =========================================================================
# 3. KROWN SUPPLY CO LUXURY SHAKER (krown-shaker-01)
# =========================================================================
def deploy_krown_shakers():
    print("\n--- Deploying KrowN Supply Co. Luxury Shakers (v8) ---")
    tumbler_path = os.path.join(PROD_DIR, 'krown-construction-jobsite-tumbler.jpg')
    master = Image.open(tumbler_path).convert('RGB')
    arr_master = np.array(master, dtype=np.float32)

    # Clean the tumbler logo and apply the official luxury KrowN Crown monogram
    crown_logo_path = os.path.join(BRAIN_DIR, 'krown-definitive-logo-1024.jpg')
    crown_img = Image.open(crown_logo_path).convert('RGBA')

    # Extract crown monogram
    crown_arr = np.array(crown_img)
    mask = (crown_arr[:, :, 0] > 70) | (crown_arr[:, :, 1] > 70)
    crown_arr[:, :, 3] = (mask * 255).astype(np.uint8)
    crown_clean = Image.fromarray(crown_arr).resize((180, 180), Image.Resampling.LANCZOS)

    # 1. Matte Obsidian Black with Antique Gold Crown
    obsidian_base = master.copy()
    # Clean old logo area on obsidian_base
    for y in range(340, 600):
        for x in range(380, 650):
            r, g, b = obsidian_base.getpixel((x, y))
            if r > 90 and g > 70:
                obsidian_base.putpixel((x, y), (26, 28, 32))
    obsidian_base.paste(crown_clean, (422, 390), mask=crown_clean.split()[3])

    # 2. Frosted Smoke
    smoke_base = obsidian_base.copy()
    enhancer = ImageEnhance.Brightness(smoke_base)
    smoke_base = enhancer.enhance(1.2)

    # 3. Raw Brushed Steel
    steel_path = os.path.join(PROD_DIR, 'kc-shaker-steelcore-v8.jpg')
    brushed_base = Image.open(steel_path).convert('RGB')
    # Put gold crown on brushed steel
    brushed_base.paste(crown_clean, (422, 390), mask=crown_clean.split()[3])

    copy_and_record(obsidian_base, 'krown-shaker-photoreal-v8.jpg')
    copy_and_record(smoke_base, 'krown-shaker-smoke-v8.jpg')
    copy_and_record(brushed_base, 'krown-shaker-brushed-v8.jpg')

    copy_and_record(obsidian_base, 'krown-shaker-photoreal-v6.jpg')
    copy_and_record(smoke_base, 'krown-shaker-smoke-v6.jpg')
    copy_and_record(brushed_base, 'krown-shaker-brushed-v6.jpg')

# =========================================================================
# 4. AXIOM PRO JOGGERS (axiom-sweatpants-pro)
# =========================================================================
def deploy_axiom_joggers():
    print("\n--- Deploying Axiom Pro Joggers (v8) ---")
    model_src = os.path.join(PROD_DIR, 'axiom-sweatpants-pro-photoreal-v6.jpg')
    studio_src = os.path.join(PROD_DIR, 'axiom-sweatpants-pro-heavyweight-studio.jpg')

    copy_and_record(model_src, 'axiom-sweatpants-pro-model-v8.jpg')
    copy_and_record(studio_src, 'axiom-sweatpants-pro-studio-v8.jpg')

# =========================================================================
# 5. KROWN CONSTRUCTION WORK SHIRT (krown-work-01)
# =========================================================================
def deploy_kc_work_shirt():
    print("\n--- Deploying KrowN Construction Heavy Work Shirt (v8) ---")
    grey_src = os.path.join(PROD_DIR, 'kc-work-shirt-grey-front-v3.jpg')
    black_src = os.path.join(PROD_DIR, 'kc-work-shirt-black-front-v2.jpg')
    back_src = os.path.join(PROD_DIR, 'kc-work-shirt-charcoal-back-v2.jpg')

    copy_and_record(grey_src, 'kc-work-shirt-grey-front-v8.jpg')
    copy_and_record(black_src, 'kc-work-shirt-black-front-v8.jpg')
    copy_and_record(back_src, 'kc-work-shirt-charcoal-back-v8.jpg')

if __name__ == '__main__':
    deploy_axiom_hoodie()
    deploy_kc_shakers()
    deploy_krown_shakers()
    deploy_axiom_joggers()
    deploy_kc_work_shirt()
    print("\nAll catalog targets successfully generated and deployed to v8!")
