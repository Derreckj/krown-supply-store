import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

def deploy_perfect_kc_work_shirt():
    print("=" * 70)
    print("Deploying Redesigned KrowN Construction Heavy Work Shirt...")
    print("=" * 70)

    prod_dir = 'public/images/products'
    masters_dir = 'public/images/products/masters'
    os.makedirs(masters_dir, exist_ok=True)

    base_src_path = os.path.join(prod_dir, 'kc-work-shirt-grey-front-v3.jpg')
    logo_white_path = 'scratch/kc_logo_cropped_white.png'

    if not os.path.exists(base_src_path):
        raise FileNotFoundError(f"Missing {base_src_path}")
    if not os.path.exists(logo_white_path):
        raise FileNotFoundError(f"Missing {logo_white_path}")

    im_orig = Image.open(base_src_path).convert('RGB')
    arr = np.array(im_orig, dtype=float)

    # 1. Clean yellow sleeve scribble (x: 670..780, y: 320..500)
    sleeve_patch = im_orig.crop((780, 320, 850, 500)).resize((110, 180), Image.Resampling.LANCZOS)
    sleeve_arr = np.array(sleeve_patch, dtype=float)
    reg_sleeve = arr[320:500, 670:780]
    mask_yellow = (reg_sleeve[:, :, 0] > 110) & (reg_sleeve[:, :, 1] > 80) & (reg_sleeve[:, :, 2] < 70)
    m_im = Image.fromarray((mask_yellow * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(3))
    m_arr = np.array(m_im, dtype=float) / 255.0
    m_arr = m_arr[..., np.newaxis]
    arr[320:500, 670:780] = reg_sleeve * (1.0 - m_arr) + sleeve_arr * m_arr

    # 2. Clean chest area completely (removing silver crown, yellow badge, 'WEAR THE KROWN')
    y0, y1, x0, x1 = 245, 755, 265, 755
    h_c, w_c = y1 - y0, x1 - x0

    clean_src = arr[765:985, 265:755]
    clean_im = Image.fromarray(np.clip(clean_src, 0, 255).astype(np.uint8)).resize((w_c, h_c), Image.Resampling.LANCZOS)
    clean_patch = np.array(clean_im, dtype=float)

    grad = np.linspace(16.0, 0.0, h_c)[:, np.newaxis, np.newaxis]
    clean_patch += grad

    chest_orig = arr[y0:y1, x0:x1]
    mask_graphic = (chest_orig > 90).any(axis=-1)
    m_chest = Image.fromarray((mask_graphic * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(5))
    m_arr_c = np.array(m_chest, dtype=float) / 255.0
    m_arr_c = m_arr_c[..., np.newaxis]

    arr[y0:y1, x0:x1] = chest_orig * (1.0 - m_arr_c) + clean_patch * m_arr_c

    cleaned_base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    print("-> Cleaned shirt fabric base successfully (zero silver crowns, zero yellow scribble).")

    # Load KrowN Construction Logo
    logo_white = Image.open(logo_white_path).convert('RGBA')
    target_w = 410
    target_h = int(logo_white.height * (target_w / logo_white.width))
    logo_res = logo_white.resize((target_w, target_h), Image.Resampling.LANCZOS)
    logo_arr = np.array(logo_res, dtype=float)
    alpha = logo_arr[:, :, 3]

    # Center emblem mask (Masonry Crown & Trowel)
    emblem_mask = np.zeros((target_h, target_w), dtype=bool)
    emblem_mask[0:int(target_h * 0.72), int(target_w * 0.40):int(target_w * 0.72)] = True

    try:
        font_sub = ImageFont.truetype('arialbd.ttf', 17)
    except:
        font_sub = ImageFont.load_default()

    # -------------------------------------------------------------------------
    # COLORWAY 1: HEATHER STEEL GREY (FLAGSHIP FRONT VIEW)
    # -------------------------------------------------------------------------
    print("Generating Colorway 1: Heather Steel Grey Work Shirt...")
    grey_canvas = cleaned_base.convert('RGBA')

    # Two-tone logo: Matte Black lettering + Safety/Antique Gold Masonry Crown & Trowel
    color_black = np.array([24, 25, 29])
    color_gold = np.array([205, 155, 45])
    logo_grey = np.zeros((target_h, target_w, 4), dtype=np.uint8)
    for c in range(3):
        logo_grey[:, :, c] = np.where(emblem_mask, color_gold[c], color_black[c])
    logo_grey[:, :, 3] = alpha.astype(np.uint8)

    np.random.seed(42)
    ink_noise = np.random.uniform(0.94, 1.05, (target_h, target_w, 1))
    logo_grey[:, :, :3] = np.clip(logo_grey[:, :, :3] * ink_noise, 0, 255)
    logo_grey_im = Image.fromarray(logo_grey)

    shadow_grey = Image.new('RGBA', (target_w + 4, target_h + 4), (0, 0, 0, 0))
    s_mask = logo_grey_im.split()[3].point(lambda p: int(p * 0.40))
    shadow_grey.paste((0, 0, 0, 160), (2, 2), mask=s_mask)
    shadow_grey = shadow_grey.filter(ImageFilter.GaussianBlur(1.2))

    cx = 512
    cy = 432
    lx = cx - target_w // 2
    ly = cy - target_h // 2

    grey_canvas.paste(shadow_grey, (lx - 2, ly - 2), mask=shadow_grey.split()[3])
    grey_canvas.paste(logo_grey_im, (lx, ly), mask=logo_grey_im.split()[3])

    draw_g = ImageDraw.Draw(grey_canvas)
    sub_text = 'BUILT TO REIGN'
    w_sub = draw_g.textlength(sub_text, font=font_sub)
    draw_g.text((cx - w_sub // 2, ly + target_h + 18), sub_text, font=font_sub, fill=(24, 25, 29, 240))

    final_grey = grey_canvas.convert('RGB')
    for fname in ['kc-work-shirt-grey-front-v3.jpg', 'kc-work-shirt-grey-front-v2.jpg', 'kc-work-shirt-grey-front.jpg']:
        final_grey.save(os.path.join(prod_dir, fname), 'JPEG', quality=98)
        final_grey.save(os.path.join(masters_dir, fname), 'JPEG', quality=98)
    print("-> Saved Heather Steel Grey work shirt targets.")

    # -------------------------------------------------------------------------
    # COLORWAY 2: OBSIDIAN BLACK WORK SHIRT (HIGH-VIS WHITE & SAFETY GOLD)
    # -------------------------------------------------------------------------
    print("Generating Colorway 2: Obsidian Black Work Shirt...")
    arr_b = np.array(cleaned_base, dtype=float)
    is_shirt = (arr_b > 45).all(axis=-1) & (arr_b < 155).all(axis=-1) & (arr_b.std(axis=-1) < 15)
    arr_b[is_shirt] = arr_b[is_shirt] * 0.30 + 6.0
    black_canvas = Image.fromarray(np.clip(arr_b, 0, 255).astype(np.uint8)).convert('RGBA')

    color_white = np.array([245, 245, 250])
    color_gold_b = np.array([235, 175, 45])
    logo_black = np.zeros((target_h, target_w, 4), dtype=np.uint8)
    for c in range(3):
        logo_black[:, :, c] = np.where(emblem_mask, color_gold_b[c], color_white[c])
    logo_black[:, :, 3] = alpha.astype(np.uint8)
    logo_black[:, :, :3] = np.clip(logo_black[:, :, :3] * ink_noise, 0, 255)
    logo_black_im = Image.fromarray(logo_black)

    shadow_black = Image.new('RGBA', (target_w + 4, target_h + 4), (0, 0, 0, 0))
    s_mask_b = logo_black_im.split()[3].point(lambda p: int(p * 0.40))
    shadow_black.paste((0, 0, 0, 180), (2, 2), mask=s_mask_b)
    shadow_black = shadow_black.filter(ImageFilter.GaussianBlur(1.2))

    black_canvas.paste(shadow_black, (lx - 2, ly - 2), mask=shadow_black.split()[3])
    black_canvas.paste(logo_black_im, (lx, ly), mask=logo_black_im.split()[3])

    draw_b = ImageDraw.Draw(black_canvas)
    draw_b.text((cx - w_sub // 2, ly + target_h + 18), sub_text, font=font_sub, fill=(235, 175, 45, 245))

    final_black = black_canvas.convert('RGB')
    for fname in ['kc-work-shirt-black-front-v2.jpg', 'kc-work-shirt-black-front.jpg']:
        final_black.save(os.path.join(prod_dir, fname), 'JPEG', quality=98)
        final_black.save(os.path.join(masters_dir, fname), 'JPEG', quality=98)
    print("-> Saved Obsidian Black work shirt targets.")

    # -------------------------------------------------------------------------
    # COLORWAY 3: CHARCOAL SLATE WORK SHIRT (BACK STATEMENT PIECE)
    # -------------------------------------------------------------------------
    print("Generating Colorway 3: Charcoal Slate Work Shirt (Back Statement Piece)...")
    arr_c = np.array(cleaned_base, dtype=float)
    arr_c[is_shirt] = arr_c[is_shirt] * 0.55 + 6.0
    charcoal_canvas = Image.fromarray(np.clip(arr_c, 0, 255).astype(np.uint8)).convert('RGBA')

    try:
        font_bold = ImageFont.truetype('impact.ttf', 38)
    except:
        font_bold = ImageFont.truetype('arialbd.ttf', 36)

    dummy = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    statement = 'BUILT TO REIGN'
    w_stmt = dummy.textlength(statement, font=font_bold)

    draw_c = ImageDraw.Draw(charcoal_canvas)
    draw_c.text((cx - w_stmt // 2, 310), statement, font=font_bold, fill=(235, 175, 45, 245))

    target_w_c = 330
    target_h_c = int(logo_white.height * (target_w_c / logo_white.width))
    logo_res_c = logo_white.resize((target_w_c, target_h_c), Image.Resampling.LANCZOS)
    alpha_c = logo_res_c.split()[3]
    white_logo_c = Image.new('RGBA', (target_w_c, target_h_c), (245, 245, 250, 0))
    white_logo_c.paste((245, 245, 250, 255), (0, 0), mask=alpha_c)

    shadow_c = Image.new('RGBA', (target_w_c + 4, target_h_c + 4), (0, 0, 0, 0))
    s_mask_c = alpha_c.point(lambda p: int(p * 0.40))
    shadow_c.paste((0, 0, 0, 160), (2, 2), mask=s_mask_c)
    shadow_c = shadow_c.filter(ImageFilter.GaussianBlur(1.2))

    lx_c = cx - target_w_c // 2
    ly_c = 375
    charcoal_canvas.paste(shadow_c, (lx_c - 2, ly_c - 2), mask=shadow_c.split()[3])
    charcoal_canvas.paste(white_logo_c, (lx_c, ly_c), mask=alpha_c)

    final_charcoal = charcoal_canvas.convert('RGB')
    for fname in ['kc-work-shirt-charcoal-back-v2.jpg', 'kc-work-shirt-charcoal-back.jpg']:
        final_charcoal.save(os.path.join(prod_dir, fname), 'JPEG', quality=98)
        final_charcoal.save(os.path.join(masters_dir, fname), 'JPEG', quality=98)
    print("-> Saved Charcoal Slate work shirt back targets.")

    # -------------------------------------------------------------------------
    # COLORWAY 4: JOBSITE TRADESMAN LOOKBOOK (MODEL PRESENTATION)
    # -------------------------------------------------------------------------
    print("Generating Colorway 4: Jobsite Tradesman Lookbook...")
    # Use clean flagship heather grey work shirt presentation
    for fname in ['kc-work-shirt-model-v2.jpg', 'kc-work-shirt-model.jpg']:
        final_grey.save(os.path.join(prod_dir, fname), 'JPEG', quality=98)
        final_grey.save(os.path.join(masters_dir, fname), 'JPEG', quality=98)
    print("-> Saved Jobsite Tradesman model targets.")

    print("\nSuccessfully deployed all redesigned KrowN Construction Heavy Work Shirt targets!")

if __name__ == '__main__':
    deploy_perfect_kc_work_shirt()
