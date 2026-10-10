import os
import shutil

desktop_folder = os.path.join(os.path.expanduser('~/Desktop'), 'KrowN_Hat_Photos')
os.makedirs(desktop_folder, exist_ok=True)

brain_dir = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'

photos = [
    (r'C:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store\etsy_featured_photos\01_Richardson_112_Front_View.jpg', '01_Primary_Hat_Front_Clean.jpg'),
    (r'C:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store\etsy_featured_photos\01_Richardson_112_Hero_Workbench.jpg', '02_Workbench_Angle_Hero.jpg'),
    (os.path.join(brain_dir, 'krown_r112_male_model_1791569854721.jpg'), '03_Male_Model_Streetwear.jpg'),
    (os.path.join(brain_dir, 'krown_r112_female_model_1791569867729.jpg'), '04_Female_Model_Casual.jpg'),
    (os.path.join(brain_dir, 'krown_r112_patch_detail_1791569885457.jpg'), '05_Macro_Leather_Patch_Detail.jpg')
]

for src, name in photos:
    if os.path.exists(src):
        dst = os.path.join(desktop_folder, name)
        shutil.copy2(src, dst)
        print(f"Copied: {name}")

import subprocess
subprocess.run(['explorer.exe', desktop_folder])
print("Opened folder in Windows Explorer!")
