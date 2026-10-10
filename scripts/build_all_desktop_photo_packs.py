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
        (os.path.join(pub_products, 'krown-r112-leather-patch-charcoal-black.jpg'), '01_Charcoal_Black_Honey_Leather_Patch.jpg'),
        (os.path.join(pub_products, 'krown-r112-leather-patch-heather-grey.jpg'), '02_Heather_Grey_Saddle_Leather_Patch.jpg'),
        (os.path.join(pub_products, 'krown-r112-leather-patch-obsidian-black.jpg'), '03_Obsidian_Black_Raw_Leather_Patch.jpg'),
        (os.path.join(pub_products, 'krown-r112-flagship-leather-patch-snapback.jpg'), '04_Primary_Hat_Front_Clean.jpg'),
        (os.path.join(pub_products, 'krown-r112-flagship-leather-patch-hero.jpg'), '05_Workbench_Angle_Hero.jpg'),
        (os.path.join(brain_dir, 'krown_r112_male_model_1791569854721.jpg'), '06_Male_Model_Streetwear.jpg'),
        (os.path.join(brain_dir, 'krown_r112_female_model_1791569867729.jpg'), '07_Female_Model_Casual.jpg'),
        (os.path.join(brain_dir, 'krown_r112_patch_detail_1791569885457.jpg'), '08_Macro_Leather_Patch_Detail.jpg'),
    ],
    '03_Cuffed_Beanie': [
        (os.path.join(pub_products, 'krown-beanie-since-2018.jpg'), '01_Primary_Beanie_Since_2018_Front.jpg'),
        (os.path.join(brain_dir, 'krown_beanie_model_1791570190810.jpg'), '02_Male_Model_Winter_Streetwear.jpg'),
        (os.path.join(pub_products, 'krown-beanie-studio-front.jpg'), '03_Studio_Front_Alt.jpg'),
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
    ],
    '07_Panoramic_Desk_Mat_32x16': [
        (os.path.join(pub_products, 'axiom-owl-desk-mat-photorealistic.jpg'), '01_Desk_Mat_Photorealistic_Battlestation.jpg'),
        (os.path.join(pub_products, 'axiom-owl-realistic-axa-face-desk-mat.jpg'), '02_Desk_Mat_Official_Axiom_Banner.jpg'),
        (os.path.join(etsy_packs, 'DESK_MAT_32x16', 'Photo_1_BattleStation_Perspective.jpg'), '03_Desk_Mat_Wide_Angle.jpg'),
        (os.path.join(etsy_packs, 'DESK_MAT_32x16', 'Photo_2_Gaming_Specs_Infographic.jpg'), '04_Desk_Mat_Specifications.jpg'),
    ],
    '08_Axiom_Richardson_112_Headwear': [
        (os.path.join(pub_products, 'axiom-r112-leather-patch-charcoal.jpg'), '01_R112_Leather_Patch_Charcoal_Front.jpg'),
        (os.path.join(pub_products, 'axiom-r112-leather-patch-purple.jpg'), '02_R112_Leather_Patch_Purple_Mesh.jpg'),
        (os.path.join(pub_products, 'axiom-r112-leather-patch-lime.jpg'), '03_R112_Leather_Patch_Toxic_Lime_Mesh.jpg'),
        (os.path.join(pub_products, 'axiom-r112-embroidered-black.jpg'), '04_R112_3D_Puff_Embroidered_Obsidian.jpg'),
        (os.path.join(pub_products, 'axiom-r112-embroidered-purple.jpg'), '05_R112_3D_Puff_Embroidered_Purple.jpg'),
        (os.path.join(pub_products, 'axiom-r112-embroidered-lime.jpg'), '06_R112_3D_Puff_Embroidered_Lime.jpg'),
        (os.path.join(pub_products, 'axiom-headwear-collection-showcase.jpg'), '07_Headwear_Collection_Showcase.jpg'),
        (os.path.join(pub_products, 'axiom-hat-model-lookbook-v2.jpg'), '08_Model_Lookbook_Snapback.jpg'),
    ],
    '09_Axiom_Vintage_Dad_Hats': [
        (os.path.join(pub_products, 'axiom-dad-hat-washed-black-v4.jpg'), '01_Vintage_Washed_Black_Dad_Hat_Owl_Only.jpg'),
        (os.path.join(pub_products, 'axiom-headwear-collection-showcase.jpg'), '02_Headwear_Showcase_Banner.jpg'),
        (os.path.join(pub_products, 'axiom-hat-model-lookbook-v2.jpg'), '03_Model_Wearing_Dad_Hat_Axiom_Apparel.jpg'),
    ],
    '10_Axiom_Pro_Shakers_Tritan_And_Steel': [
        (os.path.join(pub_products, 'axiom-shaker-signature-tritan-clean.jpg'), '01_Signature_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-signature-steel-clean.jpg'), '02_Signature_Pro_Double_Wall_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-stealth-tritan-clean.jpg'), '03_Stealth_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-stealth-steel-clean.jpg'), '04_Stealth_Pro_Double_Wall_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'axiom-shaker-bottles-4-editions.jpg'), '05_Shakers_4_Editions_Comparison.jpg'),
    ],
    '11_Axiom_Joggers_And_Fleece': [
        (os.path.join(pub_products, 'axiom-sweatpants-pro-model-v5.jpg'), '01_Pro_Heavyweight_450GSM_Model_Clean.jpg'),
        (os.path.join(pub_products, 'axiom-sweatpants-pro-heavyweight-studio.jpg'), '02_Pro_Heavyweight_Studio_Specs.jpg'),
        (os.path.join(pub_products, 'axiom-fleece-joggers-core-studio.jpg'), '03_Everyday_Fleece_Studio_Flat.jpg'),
        (os.path.join(pub_products, 'axiom-fleece-joggers-core-model.jpg'), '04_Everyday_Fleece_Creator_Model.jpg'),
    ],
    '12_Axiom_Hoodie_And_Crewneck': [
        (os.path.join(pub_products, 'axiom-heavyweight-hoodie-v3.jpg'), '01_Heavyweight_450GSM_Hoodie_Studio.jpg'),
        (os.path.join(pub_products, 'axiom-heavyweight-hoodie-model-v4.jpg'), '02_Heavyweight_Hoodie_Model_Lookbook.jpg'),
        (os.path.join(pub_products, 'axiom-crewneck-sweatshirt-studio.jpg'), '03_Official_Crewneck_Studio.jpg'),
        (os.path.join(pub_products, 'axiom-crewneck-sweatshirt-model.jpg'), '04_Official_Crewneck_Model_Lookbook.jpg'),
    ],
    '13_Axiom_Pro_Wrist_Rests': [
        (os.path.join(pub_products, 'axiom-keyboard-wrist-rest-clean-v4.jpg'), '01_Wrist_Rest_Tournament_Edition_3_Sizes.jpg'),
        (os.path.join(pub_products, 'axiom-keyboard-wrist-rest-setup-v3.jpg'), '02_Wrist_Rest_Stealth_Battlestation_Setup.jpg'),
    ],
    '14_Axiom_Ceramic_Gaming_Mugs': [
        (os.path.join(pub_products, 'axiom-mug-clean-photoreal-15oz-v3.jpg'), '01_Photoreal_Ceramic_Mug_15oz_Desk_Render.jpg'),
    ],
    '15_KrowN_Construction_Work_Shirt': [
        (os.path.join(pub_products, 'kc-work-shirt-grey-front-v3.jpg'), '01_Heather_Steel_Grey_Work_Shirt.jpg'),
        (os.path.join(pub_products, 'kc-work-shirt-black-front-v2.jpg'), '02_Obsidian_Black_Work_Shirt.jpg'),
        (os.path.join(pub_products, 'kc-work-shirt-charcoal-back-v2.jpg'), '03_Charcoal_Slate_Back_Statement.jpg'),
        (os.path.join(pub_products, 'kc-work-shirt-model-v2.jpg'), '04_Jobsite_Model_Lookbook.jpg'),
    ],
    '16_KrowN_Construction_Shakers': [
        (os.path.join(pub_products, 'kc-shaker-highvis-steel-v2.jpg'), '01_HighVis_Gold_Pro_Steel_26oz_V2.jpg'),
        (os.path.join(pub_products, 'kc-shaker-highvis-tritan-v4.jpg'), '02_HighVis_Gold_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'kc-shaker-steelcore-steel.jpg'), '03_SteelCore_Titanium_Pro_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'kc-shaker-steelcore-tritan.jpg'), '04_SteelCore_Titanium_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'kc-shaker-jobsite-steel.jpg'), '05_Jobsite_Tradesman_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'kc-shaker-jobsite-tritan.jpg'), '06_Jobsite_Tradesman_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'kc-shaker-bottles-3-editions.jpg'), '07_Construction_Shaker_Lineup.jpg'),
    ],
    '17_KrowN_Supply_Co_Shakers': [
        (os.path.join(pub_products, 'krown-shaker-obsidian-steel-v2.jpg'), '01_Obsidian_Gold_Crown_Pro_Steel_26oz_V2.jpg'),
        (os.path.join(pub_products, 'krown-shaker-obsidian-tritan.jpg'), '02_Obsidian_Gold_Crown_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'krown-shaker-smoke-steel.jpg'), '03_Frosted_Smoke_Gold_Pro_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'krown-shaker-smoke-tritan.jpg'), '04_Frosted_Smoke_Gold_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'krown-shaker-brushed-steel.jpg'), '05_Brushed_Steel_Crown_Pro_Steel_26oz.jpg'),
        (os.path.join(pub_products, 'krown-shaker-brushed-tritan.jpg'), '06_Brushed_Steel_Crown_Tritan_24oz.jpg'),
        (os.path.join(pub_products, 'krown-shaker-bottles-3-editions.jpg'), '07_Luxury_Shaker_Lineup.jpg'),
    ],
    '18_Official_Decal_Sticker_Packs': [
        (os.path.join(pub_products, 'axiom-stickers-holographic-battle-pack-v4.jpg'), '01_Axiom_Holographic_Decal_5Pack.jpg'),
        (os.path.join(pub_products, 'kc-stickers-workbench-v2.jpg'), '02_KrowN_Construction_Jobsite_Decal_5Pack.jpg'),
    ],
    '19_KrowN_Supply_Co_Luxury_Streetwear': [
        (os.path.join(pub_products, 'krown-streetwear-set-clean-v5.jpg'), '01_Premium_Streetwear_Hoodie_Sweatpants_Set_V2.jpg'),
        (os.path.join(pub_products, 'krown-french-terry-shorts-clean-v5.jpg'), '02_French_Terry_Heavyweight_Shorts_V2.jpg'),
        (os.path.join(pub_products, 'krown-dad-hat-washed-black.jpg'), '03_Vintage_Washed_Black_Dad_Hat.jpg'),
        (os.path.join(pub_products, 'krown-broken-rules-gold-tracksuit.jpg'), '04_Broken_Rules_Kintsugi_Gold_Tracksuit.jpg'),
    ]
}

total_copied = 0
for folder_name, items in categories.items():
    cat_dir = os.path.join(desktop_packs, folder_name)
    os.makedirs(cat_dir, exist_ok=True)
    for src, fname in items:
        if os.path.exists(src):
            dst = os.path.join(cat_dir, fname)
            shutil.copy2(src, dst)
            total_copied += 1
            print(f"[{folder_name}] Copied: {fname}")
        else:
            print(f"[{folder_name}] NOT FOUND: {src}")

print(f"\nSuccessfully populated Desktop Photo Packs: {total_copied} listing photos organized across {len(categories)} categories!")
