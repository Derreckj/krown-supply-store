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
    ],
    '08_Axiom_Richardson_112_Headwear': [
        (os.path.join(pub_products, 'axiom-r112-leather-patch-charcoal.jpg'), '01_R112_Leather_Patch_Charcoal_Front.jpg'),
        (os.path.join(pub_products, 'axiom-r112-leather-patch-purple.jpg'), '02_R112_Leather_Patch_Purple_Mesh.jpg'),
        (os.path.join(pub_products, 'axiom-r112-leather-patch-lime.jpg'), '03_R112_Leather_Patch_Toxic_Lime_Mesh.jpg'),
        (os.path.join(pub_products, 'axiom-r112-embroidered-black.jpg'), '04_R112_3D_Puff_Embroidered_Obsidian.jpg'),
        (os.path.join(pub_products, 'axiom-r112-embroidered-purple.jpg'), '05_R112_3D_Puff_Embroidered_Purple.jpg'),
        (os.path.join(pub_products, 'axiom-r112-embroidered-lime.jpg'), '06_R112_3D_Puff_Embroidered_Lime.jpg'),
        (os.path.join(pub_products, 'axiom-headwear-collection-showcase.jpg'), '07_Headwear_Collection_Showcase.jpg'),
        (os.path.join(pub_products, 'axiom-hat-model-lookbook.jpg'), '08_Model_Lookbook_Snapback.jpg'),
    ],
    '09_Axiom_Vintage_Dad_Hats': [
        (os.path.join(pub_products, 'axiom-dad-hat-washed-black.jpg'), '01_Vintage_Washed_Black_Dad_Hat.jpg'),
        (os.path.join(pub_products, 'axiom-headwear-collection-showcase.jpg'), '02_Headwear_Showcase_Banner.jpg'),
        (os.path.join(pub_products, 'axiom-hat-model-lookbook.jpg'), '03_Model_Wearing_Dad_Hat.jpg'),
    ],
    '10_Axiom_Pro_Shakers_Tritan_And_Steel': [
        (os.path.join(pub_products, 'axiom-shaker-signature-tritan-clean.jpg'), '01_Signature_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-signature-steel-clean.jpg'), '02_Signature_Pro_Double_Wall_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-stealth-tritan-clean.jpg'), '03_Stealth_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-stealth-steel-clean.jpg'), '04_Stealth_Pro_Double_Wall_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-bottles-4-editions.jpg'), '05_Shakers_4_Editions_Comparison.jpg'),
    ],
    '11_Axiom_Joggers_And_Fleece': [
        (os.path.join(pub_products, 'axiom-sweatpants-pro-model-clean.jpg'), '01_Pro_Heavyweight_450GSM_Model_Clean.jpg'),
        (os.path.join(pub_products, 'axiom-sweatpants-pro-heavyweight-studio.jpg'), '02_Pro_Heavyweight_Studio_Specs.jpg'),
        (os.path.join(pub_products, 'axiom-fleece-joggers-core-studio.jpg'), '03_Everyday_Fleece_Studio_Flat.jpg'),
        (os.path.join(pub_products, 'axiom-fleece-joggers-core-model.jpg'), '04_Everyday_Fleece_Creator_Model.jpg'),
    ],
    '12_Axiom_Hoodie_And_Crewneck': [
        (os.path.join(pub_products, 'axiom-heavyweight-hoodie-studio.jpg'), '01_Heavyweight_450GSM_Hoodie_Studio.jpg'),
        (os.path.join(pub_products, 'axiom-heavyweight-hoodie-model.jpg'), '02_Heavyweight_Hoodie_Model_Lookbook.jpg'),
        (os.path.join(pub_products, 'axiom-crewneck-sweatshirt-studio.jpg'), '03_Official_Crewneck_Studio.jpg'),
        (os.path.join(pub_products, 'axiom-crewneck-sweatshirt-model.jpg'), '04_Official_Crewneck_Model_Lookbook.jpg'),
    ],
    '13_Axiom_Pro_Wrist_Rests': [
        (os.path.join(pub_products, 'axiom-keyboard-wrist-rest-tournament-edition.jpg'), '01_Wrist_Rest_Tournament_Edition_3_Sizes.jpg'),
        (os.path.join(pub_products, 'axiom-keyboard-wrist-rest-stealth-setup.jpg'), '02_Wrist_Rest_Stealth_Battlestation_Setup.jpg'),
    ],
    '14_Axiom_Ceramic_Gaming_Mugs': [
        (os.path.join(pub_products, 'axiom-mug-smokey-crest-15oz.png'), '01_Smokey_Crest_Gothic_Mug_15oz.png'),
        (os.path.join(pub_products, 'axiom-owl-gamer-mug-15oz.png'), '02_Two_Tone_Mascot_Quote_Mug_15oz.png'),
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
