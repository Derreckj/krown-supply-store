import os
import shutil
from PIL import Image

def deploy_perfect_streetwear_set():
    source_img_path = 'test_final_masterpiece.jpg'
    clean_base_path = 'test_blank_perfect.jpg'
    clean_crown_path = 'final_clean_crown_pure_alpha.png'

    if not os.path.exists(source_img_path):
        raise FileNotFoundError(f"Missing {source_img_path}")

    prod_dir = 'public/images/products'
    masters_dir = 'public/images/products/masters'
    branding_dir = 'public/images/branding'

    os.makedirs(masters_dir, exist_ok=True)
    os.makedirs(branding_dir, exist_ok=True)

    # 1. Update branding crown to pure transparent alpha
    if os.path.exists(clean_crown_path):
        target_pure = os.path.join(branding_dir, 'krown_official_crown_pure.png')
        shutil.copy2(clean_crown_path, target_pure)
        print(f"Updated {target_pure}")

    # 2. Update base image so base never has rectangular artifacts
    if os.path.exists(clean_base_path):
        target_orig = os.path.join(prod_dir, 'orig_streetwear_set.jpg')
        shutil.copy2(clean_base_path, target_orig)
        shutil.copy2(clean_base_path, os.path.join(masters_dir, 'orig_streetwear_set.jpg'))
        print(f"Updated {target_orig} with pristine clean base")

    # 3. Target filenames to update with the new masterpiece
    targets = [
        'krown-streetwear-set-photoreal-v6.jpg',
        'krown-streetwear-set-clean-v5.jpg',
        'krown-streetwear-set-clean-v4.jpg',
        'krown-streetwear-set-black.jpg',
        'krown-streetwear-set-v2.jpg',
        'krown-streetwear-set-v3.jpg',
        'krown-supply-streetwear-set.jpg',
    ]

    for fname in targets:
        p_path = os.path.join(prod_dir, fname)
        m_path = os.path.join(masters_dir, fname)
        shutil.copy2(source_img_path, p_path)
        shutil.copy2(source_img_path, m_path)
        print(f"Updated {p_path} and master copy")

    print("\nSuccessfully deployed perfect blended streetwear set to all targets!")

if __name__ == '__main__':
    deploy_perfect_streetwear_set()
