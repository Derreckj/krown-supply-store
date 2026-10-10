import os
import shutil
import math
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')
BRAIN_MEDIA = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7\.tempmediaStorage'
BRAIN_DIR = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'

os.makedirs(PROD_DIR, exist_ok=True)
os.makedirs(MASTERS_DIR, exist_ok=True)

def save_dual(img, name):
    dst = os.path.join(PROD_DIR, name)
    dst_m = os.path.join(MASTERS_DIR, name)
    img.save(dst, quality=96)
    img.save(dst_m, quality=96)
    print(f"Deployed: {name}")

# =========================================================================
# 1. KROWN CONSTRUCTION SHAKER BOTTLES (kc-shaker-01)
# Add yellow / gold accents to the top cover/cap on the workbench tumbler photo
# =========================================================================
def generate_kc_shakers():
    print("\n--- 1. Generating KC Workbench Shakers with Yellow/Gold Accented Caps ---")
    tumbler_path = os.path.join(PROD_DIR, 'krown-construction-jobsite-tumbler.jpg')
    master = Image.open(tumbler_path).convert('RGB')
    arr_master = np.array(master, dtype=np.float32)

    # Function to apply yellow/gold accent to the cap region
    # Cap region is y: 195 to 260, x: 380 to 650
    # Specifically the flip lock latch, carry loop ring, and accent ring
    def add_gold_cap_accents(arr, accent_rgb=(245, 195, 35)):
        arr_out = arr.copy()
        # Cap rim accent ring: y: 245 to 258, x: 390 to 640
        # Flip lock latch in center: y: 200 to 240, x: 505 to 565
        for y in range(195, 260):
            for x in range(380, 650):
                # Center flip latch
                is_latch = (205 <= y <= 238 and 515 <= x <= 555)
                # Left hinge/loop accent
                is_loop = (205 <= y <= 245 and 400 <= x <= 430)
                # Thin horizontal rim ring
                is_rim = (246 <= y <= 255 and 390 <= x <= 640)

                if is_latch or is_loop or is_rim:
                    r, g, b = arr_out[y, x]
                    lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
                    edge_factor = 1.0
                    if is_rim:
                        edge_dist = min(y - 246, 255 - y) / 4.5
                        edge_factor = min(1.0, edge_dist)
                    
                    accent_r = int(min(255, accent_rgb[0] * (0.6 + 0.65 * lum)))
                    accent_g = int(min(255, accent_rgb[1] * (0.6 + 0.65 * lum)))
                    accent_b = int(min(255, accent_rgb[2] * (0.6 + 0.65 * lum)))

                    arr_out[y, x] = [
                        (1 - edge_factor) * r + edge_factor * accent_r,
                        (1 - edge_factor) * g + edge_factor * accent_g,
                        (1 - edge_factor) * b + edge_factor * accent_b
                    ]
        return arr_out

    # Variant 1: High-Vis Safety Gold & Matte Black
    hv_arr = add_gold_cap_accents(arr_master, accent_rgb=(255, 205, 20))
    # Enhance the body gold logo luminescence
    for y in range(320, 600):
        for x in range(370, 660):
            r, g, b = hv_arr[y, x]
            if r > 95 and g > 75 and b < 95 and (r > b + 25):
                lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
                hv_arr[y, x] = [
                    int(min(255, 255 * lum + 35)),
                    int(min(255, 205 * lum + 25)),
                    int(min(255, 30 * lum + 5))
                ]
    im_hv = Image.fromarray(hv_arr.astype(np.uint8))

    # Variant 2: Industrial Brushed Stainless Steel & Concrete Grey
    steel_arr = arr_master.copy()
    np.random.seed(42)
    logo_mask = (arr_master[:, :, 0] > 95) & (arr_master[:, :, 1] > 75) & (arr_master[:, :, 2] < 95) & (arr_master[:, :, 0] > arr_master[:, :, 2] + 25)

    def get_bounds(y):
        if y < 225 or y > 855: return None, None
        if y <= 530: return 340, 680
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

            if logo_mask[y, x]:
                steel_arr[y, x] = [38, 40, 44] # laser etched titanium
            else:
                steel_arr[y, x] = (1.0 - w_blend) * steel_arr[y, x] + w_blend * np.array([r_val, g_val, b_val])

    steel_arr = add_gold_cap_accents(steel_arr, accent_rgb=(250, 195, 30))
    im_sc = Image.fromarray(steel_arr.astype(np.uint8))

    # Variant 3: Tradesman Heavy-Duty Obsidian
    tb_arr = add_gold_cap_accents(arr_master, accent_rgb=(225, 175, 45))
    im_tb = Image.fromarray(tb_arr.astype(np.uint8))

    # Save v9, v8, and v6
    save_dual(im_hv, 'kc-shaker-photoreal-v9.jpg')
    save_dual(im_sc, 'kc-shaker-steelcore-v9.jpg')
    save_dual(im_tb, 'kc-shaker-tradesman-v9.jpg')

    save_dual(im_hv, 'kc-shaker-photoreal-v8.jpg')
    save_dual(im_sc, 'kc-shaker-steelcore-v8.jpg')
    save_dual(im_tb, 'kc-shaker-tradesman-v8.jpg')
    save_dual(im_hv, 'kc-shaker-photoreal-v6.jpg')
    save_dual(im_sc, 'kc-shaker-steelcore-v6.jpg')
    save_dual(im_tb, 'kc-shaker-tradesman-v6.jpg')

# =========================================================================
# 2. DESK MATS (krown-mat-01)
# Use user-provided high-res artworks in battlestation perspective + flat-lays
# =========================================================================
def generate_desk_mats():
    print("\n--- 2. Generating Battlestation Desk Mats & Options ---")
    bg = Image.open(os.path.join(PROD_DIR, 'axiom-owl-desk-mat-photorealistic.jpg')).convert('RGB')
    w, h = bg.size

    # Perspective quad on the desk
    dst = [(86, 323), (938, 379), (938, 776), (86, 701)]

    def find_coeffs(pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
        A = np.matrix(matrix, dtype=float)
        B = np.array(pb).reshape(8)
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)

    # Keyboard & mouse mask (preserve keyboard/mouse on top of mat)
    # Keyboard is roughly x: 340 to 570, y: 440 to 535
    kb_mask = Image.new('L', (w, h), 0)
    draw_kb = ImageDraw.Draw(kb_mask)
    draw_kb.polygon([(345, 442), (565, 456), (555, 532), (338, 518)], fill=255) # keyboard
    draw_kb.ellipse((680, 480, 740, 560), fill=255) # mouse
    kb_mask = kb_mask.filter(ImageFilter.GaussianBlur(3.0))

    # Mat polygon mask
    mat_mask = Image.new('L', (w, h), 0)
    draw_mat = ImageDraw.Draw(mat_mask)
    draw_mat.polygon(dst, fill=255)
    mat_mask = mat_mask.filter(ImageFilter.GaussianBlur(1.2))

    artworks = [
        ('media_1791673496022.jpg', 'axiom-mat-original-banner-v9.jpg', 'axiom-mat-original-banner-flat-v9.jpg', (57, 255, 20)),
        ('media_1791673534233.jpg', 'axiom-mat-volcanic-flame-v9.jpg', 'axiom-mat-volcanic-flame-flat-v9.jpg', (255, 60, 20)),
        ('media_1791673449100.png', 'axiom-mat-cyber-neon-v9.jpg', 'axiom-mat-cyber-neon-flat-v9.jpg', (180, 50, 255)),
    ]

    for art_file, out_battle, out_flat, border_color in artworks:
        art_path = os.path.join(BRAIN_MEDIA, art_file)
        art = Image.open(art_path).convert('RGB')

        # 1. Perspective Battlestation Photo
        src = [(0, 0), (art.width, 0), (art.width, art.height), (0, art.height)]
        coeffs = find_coeffs(dst, src)
        warped_art = art.transform((w, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

        # Composite mat onto desk
        comp = Image.composite(warped_art, bg, mat_mask)
        # Composite original keyboard/mouse back on top
        comp_final = Image.composite(bg, comp, kb_mask)
        save_dual(comp_final, out_battle)

        # 2. Commercial Flat-Lay Product Presentation
        flat_canvas = Image.new('RGB', (1024, 1024), (16, 17, 20))
        # Draw soft shadow
        shadow = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.rounded_rectangle((70, 200, 954, 760), radius=24, fill=(0, 0, 0, 200))
        shadow = shadow.filter(ImageFilter.GaussianBlur(16.0))
        flat_canvas.paste(shadow, (0, 0), mask=shadow.split()[3])

        # Mat resize
        mat_scaled = art.resize((880, 550), Image.Resampling.LANCZOS)
        # Rounded corners with anti-fray stitched border
        mat_round_mask = Image.new('L', (880, 550), 0)
        draw_rm = ImageDraw.Draw(mat_round_mask)
        draw_rm.rounded_rectangle((0, 0, 880, 550), radius=20, fill=255)

        flat_canvas.paste(mat_scaled, (72, 195), mask=mat_round_mask)

        # Draw stitched border
        draw_border = ImageDraw.Draw(flat_canvas)
        draw_border.rounded_rectangle((72, 195, 952, 745), radius=20, outline=border_color, width=4)

        save_dual(flat_canvas, out_flat)

# =========================================================================
# 3. KEYBOARD WRIST RESTS (axiom-wrist-rest-01)
# 3 options:
# Option 1: New esports font + new Axiom crest
# Option 2: Classic gothic font with all-green text + old owl logo
# Option 3: Stealth blackout edition
# =========================================================================
def generate_wrist_rests():
    print("\n--- 3. Generating Ergonomic Keyboard Wrist Rests ---")
    desk_bg = Image.open(os.path.join(PROD_DIR, 'axiom-mat-original-banner-v9.jpg')).convert('RGB')
    
    # Create photorealistic ergonomic wrist rest canvas (1024x1024 studio top-down angled setup)
    def render_wrist_rest(variant_type):
        canvas = Image.new('RGB', (1024, 1024), (18, 19, 23))

        # Background desk texture
        desk_crop = desk_bg.resize((1024, 1024)).filter(ImageFilter.GaussianBlur(12.0))
        canvas.paste(desk_crop, (0, 0))

        # Soft drop shadow for wrist rest
        shadow = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.rounded_rectangle((100, 395, 924, 615), radius=35, fill=(0, 0, 0, 220))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18.0))
        canvas.paste(shadow, (0, 0), mask=shadow.split()[3])

        # Wrist rest base body: ergonomic memory foam slope
        # Width: 810, Height: 200
        pad = Image.new('RGB', (810, 200), (22, 23, 27))
        pad_arr = np.array(pad, dtype=np.float32)

        # Ergonomic 15-degree slope contour lighting (brighter near top, subtle taper)
        for y in range(200):
            lum = 0.8 + 0.35 * math.sin((y / 200.0) * math.pi)
            pad_arr[y, :, :] *= lum

        pad = Image.fromarray(pad_arr.astype(np.uint8))

        # Rounded mask for wrist rest
        pad_mask = Image.new('L', (810, 200), 0)
        draw_pm = ImageDraw.Draw(pad_mask)
        draw_pm.rounded_rectangle((0, 0, 810, 200), radius=28, fill=255)

        draw_pad = ImageDraw.Draw(pad)

        if variant_type == 'new-font':
            # Option 1: New angular crest + clean modern athletic esports font
            # Load new owl crest from brain
            crest_path = os.path.join(BRAIN_DIR, 'axiom_hoodie_studio_front_1791592242763.jpg')
            crest_raw = Image.open(crest_path).convert('RGB')
            crest_crop = crest_raw.crop((390, 420, 630, 660)).resize((130, 130), Image.Resampling.LANCZOS)
            
            # Paste crest on left
            pad.paste(crest_crop, (50, 35))

            # Bold clean athletic modern esports typography
            # "AXIOM ALLEGIANCE" in vibrant toxic green & electric purple
            draw_pad.text((220, 65), "AXIOM ALLEGIANCE", fill=(57, 255, 20), font_size=58)
            draw_pad.text((220, 130), "PRO TOURNAMENT LOADOUT // 450 GSM MEMORY GEL", fill=(170, 70, 255), font_size=18)
            border_color = (57, 255, 20)

        elif variant_type == 'classic-green':
            # Option 2: Old owl logo + classic gothic font in SOLID VIBRANT TOXIC GREEN
            banner_art = Image.open(os.path.join(BRAIN_MEDIA, 'media_1791673496022.jpg')).convert('RGB')
            # Crop old owl logo from center: x: 340 to 680, y: 150 to 520
            owl_old = banner_art.crop((350, 160, 670, 520)).resize((135, 150), Image.Resampling.LANCZOS)
            pad.paste(owl_old, (50, 25))

            # Gothic font in ALL GREEN
            # Text from banner
            text_crop = banner_art.crop((230, 785, 795, 915)).resize((560, 115), Image.Resampling.LANCZOS)
            # Tint text to solid vibrant green
            text_arr = np.array(text_crop, dtype=np.float32)
            for y in range(text_arr.shape[0]):
                for x in range(text_arr.shape[1]):
                    r, g, b = text_arr[y, x]
                    if (r + g + b) > 90:
                        lum = (r*0.299 + g*0.587 + b*0.114) / 255.0
                        text_arr[y, x] = [int(30 * lum), int(min(255, 255 * lum + 40)), int(20 * lum)]
            text_green = Image.fromarray(text_arr.astype(np.uint8))
            pad.paste(text_green, (215, 42))
            border_color = (57, 255, 20)

        else: # stealth
            draw_pad.text((220, 75), "AXIOM ALLEGIANCE", fill=(75, 78, 86), font_size=54)
            draw_pad.text((220, 135), "STEALTH TOURNAMENT EDITION // TACTICAL BLACKOUT", fill=(55, 58, 65), font_size=17)
            border_color = (45, 48, 54)

        # Precision perimeter stitching
        draw_pad.rounded_rectangle((4, 4, 806, 196), radius=26, outline=border_color, width=4)

        canvas.paste(pad, (107, 400), mask=pad_mask)
        return canvas

    im_new = render_wrist_rest('new-font')
    im_classic = render_wrist_rest('classic-green')
    im_stealth = render_wrist_rest('stealth')

    save_dual(im_new, 'axiom-wrist-rest-new-font-v9.jpg')
    save_dual(im_classic, 'axiom-wrist-rest-classic-green-v9.jpg')
    save_dual(im_stealth, 'axiom-wrist-rest-stealth-v9.jpg')

# =========================================================================
# 4. CUSTOM HAT REALISTIC RICHARDSON 112 PHOTOS (HAT_COLORWAYS)
# Clean blank bases for /custom-crew
# =========================================================================
def generate_custom_hat_bases():
    print("\n--- 4. Generating Realistic Richardson 112 Hat Bases for Custom Studio ---")
    hat_master = Image.open(os.path.join(PROD_DIR, 'krown-r112-flagship-leather-patch-hero.jpg')).convert('RGB')
    
    # The patch is in the center crown. We clean the patch area to create the pristine blank crown!
    arr = np.array(hat_master, dtype=np.float32)

    # Patch area: y: 410 to 630, x: 380 to 640
    # Blend with surrounding twill fabric texture
    crown_sample = arr[350:410, 420:580] # pristine dark twill
    crown_mean = crown_sample.mean(axis=(0, 1))

    for y in range(410, 630):
        for x in range(380, 640):
            # Distance from patch center
            dx = (x - 510) / 120.0
            dy = (y - 520) / 100.0
            d = math.sqrt(dx*dx + dy*dy)
            if d < 1.0:
                # Add subtle fabric weave texture
                noise = np.random.normal(0, 3.0, 3)
                arr[y, x] = np.clip(crown_mean + noise, 0, 255)

    base_blank = Image.fromarray(arr.astype(np.uint8))

    # 1. Charcoal & Black Mesh
    save_dual(base_blank, 'krown-r112-custom-charcoal-black-v9.jpg')

    # 2. Heather Grey & Black Mesh (lighten the crown panels)
    heather_arr = arr.copy()
    for y in range(250, 650):
        for x in range(300, 720):
            r, g, b = heather_arr[y, x]
            if (r + g + b) > 50:
                heather_arr[y, x] = np.clip(heather_arr[y, x] * 1.55 + 20, 0, 255)
    save_dual(Image.fromarray(heather_arr.astype(np.uint8)), 'krown-r112-custom-heather-grey-v9.jpg')

    # 3. Solid Obsidian Black (deepen crown panels)
    obsidian_arr = arr.copy()
    for y in range(250, 700):
        for x in range(250, 770):
            obsidian_arr[y, x] = np.clip(obsidian_arr[y, x] * 0.72, 0, 255)
    save_dual(Image.fromarray(obsidian_arr.astype(np.uint8)), 'krown-r112-custom-obsidian-black-v9.jpg')

    # 4. Khaki & Coffee Mesh (warm saddle khaki front)
    khaki_arr = arr.copy()
    for y in range(250, 650):
        for x in range(300, 720):
            r, g, b = khaki_arr[y, x]
            if (r + g + b) > 50:
                lum = (r*0.299 + g*0.587 + b*0.114)
                khaki_arr[y, x] = [min(255, lum * 1.8 + 50), min(255, lum * 1.6 + 35), min(255, lum * 1.1 + 15)]
    save_dual(Image.fromarray(khaki_arr.astype(np.uint8)), 'krown-r112-custom-khaki-coffee-v9.jpg')

# =========================================================================
# 5. AXIOM ALLEGIANCE BEANIE (axiom-beanie-01)
# =========================================================================
def generate_axiom_beanies():
    print("\n--- 5. Generating Axiom Allegiance Ribbed Cuffed Beanies ---")
    beanie_master = Image.open(os.path.join(PROD_DIR, 'krown-beanie-since-2018.jpg')).convert('RGB')
    
    # The patch on beanie is at y: 420 to 600, x: 400 to 620
    # Clean old patch and overlay embroidered Axiom Owl badges
    art_path = os.path.join(BRAIN_MEDIA, 'media_1791673496022.jpg')
    art = Image.open(art_path).convert('RGB')
    owl_green = art.crop((360, 180, 660, 500)).resize((180, 180), Image.Resampling.LANCZOS)

    art_volc = Image.open(os.path.join(BRAIN_MEDIA, 'media_1791673534233.jpg')).convert('RGB')
    owl_volc = art_volc.crop((360, 180, 660, 500)).resize((180, 180), Image.Resampling.LANCZOS)

    # Circular mask for embroidered patch
    patch_mask = Image.new('L', (180, 180), 0)
    draw_pm = ImageDraw.Draw(patch_mask)
    draw_pm.ellipse((0, 0, 180, 180), fill=255)

    # 1. Midnight Obsidian / Toxic Green Owl Crest
    beanie_1 = beanie_master.copy()
    draw_b1 = ImageDraw.Draw(beanie_1)
    draw_b1.ellipse((422-4, 430-4, 422+184, 430+184), fill=(10, 10, 12), outline=(57, 255, 20), width=4)
    beanie_1.paste(owl_green, (422, 430), mask=patch_mask)
    save_dual(beanie_1, 'axiom-beanie-obsidian-lime-v9.jpg')

    # 2. Royal Purple & Electric Green Dual-Tone Crest
    beanie_2 = beanie_master.copy()
    draw_b2 = ImageDraw.Draw(beanie_2)
    draw_b2.ellipse((422-4, 430-4, 422+184, 430+184), fill=(25, 12, 38), outline=(170, 70, 255), width=4)
    beanie_2.paste(owl_green, (422, 430), mask=patch_mask)
    save_dual(beanie_2, 'axiom-beanie-purple-green-v9.jpg')

    # 3. Volcanic Crimson / Ember Owl Crest
    beanie_3 = beanie_master.copy()
    draw_b3 = ImageDraw.Draw(beanie_3)
    draw_b3.ellipse((422-4, 430-4, 422+184, 430+184), fill=(28, 12, 12), outline=(255, 60, 20), width=4)
    beanie_3.paste(owl_volc, (422, 430), mask=patch_mask)
    save_dual(beanie_3, 'axiom-beanie-volcanic-v9.jpg')

if __name__ == '__main__':
    generate_kc_shakers()
    generate_desk_mats()
    generate_wrist_rests()
    generate_custom_hat_bases()
    generate_axiom_beanies()
    print("\nAll v9 assets generated and deployed successfully!")
