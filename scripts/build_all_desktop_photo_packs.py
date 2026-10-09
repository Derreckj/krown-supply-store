import os
import shutil

desktop_packs = os.path.join(os.path.expanduser('~/Desktop'), 'KrowN_Listing_Photo_Packs')
os.makedirs(desktop_packs, exist_ok=True)

brain_dir = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'
scratch_dir = r'C:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store'
pub_products = os.path.join(scratch_dir, 'public', 'images', 'products')
etsy_packs = os.path.join(scratch_dir, 'etsy_store_assets', '02_LISTING_PHOTO_PACKS')

categories = {
    '01_Heavyweight_Hoodie_480GSM': [
        (os.path.join(brain_dir, 'krown_hoodie_studio_front_1791570097217.jpg'), '01_Primary_Hoodie_Studio_Front.jpg'),
        (os.path.join(brain_dir, 'krown_hoodie_male_model_1791570118463.jpg'), '02_Male_Model_Streetwear.jpg'),
        (os.path.join(brain_dir, 'krown_hoodie_female_model_1791570141338.jpg'), '03_Female_Model_Streetwear.jpg'),
        (os.path.join(etsy_packs, 'HOODIE_480GSM', 'Photo_1_Front_Chest_Gold_Crest.jpg'), '04_Mannequin_Chest_Crest.jpg'),
        (os.path.join(etsy_packs, 'HOODIE_480GSM', 'Photo_2_Back_Official_KrowN_Statement.jpg'), '05_Back_Statement.jpg'),
    ],
    '02_Richardson_112_Hat': [
        (os.path.join(scratch_dir, 'etsy_featured_photos', '01_Richardson_112_Front_View.jpg'), '01_Primary_Hat_Front_Clean.jpg'),
        (os.path.join(scratch_dir, 'etsy_featured_photos', '01_Richardson_112_Hero_Workbench.jpg'), '02_Workbench_Angle_Hero.jpg'),
        (os.path.join(brain_dir, 'krown_r112_male_model_1791569854721.jpg'), '03_Male_Model_Streetwear.jpg'),
        (os.path.join(brain_dir, 'krown_r112_female_model_1791569867729.jpg'), '04_Female_Model_Casual.jpg'),
        (os.path.join(brain_dir, 'krown_r112_patch_detail_1791569885457.jpg'), '05_Macro_Leather_Patch_Detail.jpg'),
    ],
    '03_Cuffed_Beanie': [
        (os.path.join(brain_dir, 'krown_beanie_studio_front_1791570168479.jpg'), '01_Primary_Beanie_Studio_Front.jpg'),
        (os.path.join(brain_dir, 'krown_beanie_model_1791570190810.jpg'), '02_Male_Model_Winter_Streetwear.jpg'),
    ],
    '04_Comfort_Colors_1717_Tee': [
        (os.path.join(pub_products, 'krown-supply-comfort-colors-1717-tee.jpg'), '01_Primary_Tee_Mannequin_Front.jpg'),
    ],
    '05_Jobsite_Tumbler_20OZ': [
        (os.path.join(etsy_packs, 'TUMBLER_20OZ', 'Photo_1_Front_Laser_Gold_Crest.jpg'), '01_Primary_Tumbler_Front.jpg'),
        (os.path.join(etsy_packs, 'TUMBLER_20OZ', 'Photo_2_Alternative_Angle.jpg'), '02_Tumbler_Alternative_Angle.jpg'),
        (os.path.join(etsy_packs, 'TUMBLER_20OZ', 'Photo_3_Jobsite_Specifications_Infographic.jpg'), '03_Tumbler_Jobsite_Specs.jpg'),
    ],
    '06_AXA_Esports_Jersey': [
        (os.path.join(pub_products, 'axa-pro-jersey-home.jpg'), '01_Primary_Jersey_Home.jpg'),
        (os.path.join(pub_products, 'axa-pro-jersey-home-back.jpg'), '02_Jersey_Home_Back.jpg'),
        (os.path.join(pub_products, 'axa-pro-jersey-away.jpg'), '03_Jersey_Away_Front.jpg'),
        (os.path.join(pub_products, 'axa-pro-jersey-away-back.jpg'), '04_Jersey_Away_Back.jpg'),
        (os.path.join(pub_products, 'axa-pro-jersey-championship-back.jpg'), '05_Jersey_Championship_Back.jpg'),
        (os.path.join(pub_products, 'axa-pro-jersey-stealth.jpg'), '06_Jersey_Stealth_Front.jpg'),
        (os.path.join(pub_products, 'axa-pro-jersey-stealth-back.jpg'), '07_Jersey_Stealth_Back.jpg'),
        (os.path.join(scratch_dir, 'public', 'images', 'branding', 'gaming', 'axiom-owl-quote-frame.jpg'), '08_Axiom_Creed_Motto_Badge.jpg'),
    ],
    '07_Panoramic_Desk_Mat_32x16': [
        (os.path.join(etsy_packs, 'DESK_MAT_32x16', 'Photo_1_BattleStation_Perspective.jpg'), '01_Primary_Desk_Mat_Battlestation.jpg'),
        (os.path.join(etsy_packs, 'DESK_MAT_32x16', 'Photo_2_Gaming_Specs_Infographic.jpg'), '02_Desk_Mat_Specifications.jpg'),
    ]
}

for folder_name, items in categories.items():
    cat_dir = os.path.join(desktop_packs, folder_name)
    os.makedirs(cat_dir, exist_ok=True)
    for src, fname in items:
        if os.path.exists(src):
            dst = os.path.join(cat_dir, fname)
            shutil.copy2(src, dst)
            print(f"[{folder_name}] Copied: {fname}")

# Also copy primary images directly into public/images/products
pub_map = {
    os.path.join(brain_dir, 'krown_hoodie_studio_front_1791570097217.jpg'): 'krown-hoodie-studio-front.jpg',
    os.path.join(brain_dir, 'krown_hoodie_male_model_1791570118463.jpg'): 'krown-hoodie-male-model.jpg',
    os.path.join(brain_dir, 'krown_hoodie_female_model_1791570141338.jpg'): 'krown-hoodie-female-model.jpg',
    os.path.join(brain_dir, 'krown_beanie_studio_front_1791570168479.jpg'): 'krown-beanie-studio-front.jpg',
    os.path.join(brain_dir, 'krown_beanie_model_1791570190810.jpg'): 'krown-beanie-model.jpg',
}

for src, fname in pub_map.items():
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(pub_products, fname))
        print(f"[public/images/products] Copied: {fname}")

import subprocess
subprocess.run(['explorer.exe', desktop_packs])
print("\nAll photo packs generated and opened on Desktop!")
