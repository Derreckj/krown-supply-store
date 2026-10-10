from PIL import Image, ImageFilter
import numpy as np
import os

prod_dir = 'public/images/products'

# Load the sleeve images
front_sleeve = Image.open(os.path.join(prod_dir, 'axiom-arm-sleeve-3d-front.png')).convert('RGBA')
back_sleeve = Image.open(os.path.join(prod_dir, 'axiom-arm-sleeve-3d-back.png')).convert('RGBA')

# Backdrop: clean dark charcoal studio canvas 1024x1024 with subtle center spotlight
W, H = 1024, 1024

def make_studio_sleeve(sleeve_img, out_name):
    canvas = Image.new('RGB', (W, H), (14, 15, 18))
    # Subtle radial gradient spotlight
    y, x = np.mgrid[0:H, 0:W]
    dist = np.sqrt((x - 512)**2 + (y - 512)**2)
    spot = np.clip(1.0 - dist / 650.0, 0.0, 1.0)
    bg_arr = np.zeros((H, W, 3), dtype=np.uint8)
    for c, val in enumerate([18, 19, 24]):
        bg_arr[:, :, c] = np.clip(val + spot * 24, 0, 255).astype(np.uint8)
        
    bg_img = Image.fromarray(bg_arr, mode='RGB').convert('RGBA')
    
    # Scale sleeve to height ~ 820
    target_h = 820
    aspect = sleeve_img.width / sleeve_img.height
    target_w = int(target_h * aspect)
    sleeve_scaled = sleeve_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    pos_x = (W - target_w) // 2
    pos_y = (H - target_h) // 2
    
    # Soft ambient drop shadow
    shadow_mask = sleeve_scaled.split()[3].filter(ImageFilter.GaussianBlur(radius=8.0))
    shadow_patch = Image.new('RGBA', (target_w, target_h), (5, 5, 8, 180))
    shadow_patch.putalpha(shadow_mask)
    
    bg_img.paste(shadow_patch, (pos_x + 4, pos_y + 12), mask=shadow_mask)
    bg_img.paste(sleeve_scaled, (pos_x, pos_y), mask=sleeve_scaled.split()[3])
    
    final = bg_img.convert('RGB')
    final.save(os.path.join(prod_dir, out_name), quality=96)
    print(f"Saved 1024x1024 studio sleeve: {out_name}")

make_studio_sleeve(front_sleeve, 'axiom-arm-sleeve-3d-front-studio.jpg')
make_studio_sleeve(back_sleeve, 'axiom-arm-sleeve-3d-back-studio.jpg')

# Also update printify.ts so it uses the studio images
with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("'/images/products/axiom-arm-sleeve-3d-front.png'", "'/images/products/axiom-arm-sleeve-3d-front-studio.jpg'")
text = text.replace("'/images/products/axiom-arm-sleeve-3d-back.png'", "'/images/products/axiom-arm-sleeve-3d-back-studio.jpg'")
text = text.replace("'/images/products/axiom-arm-sleeve-flat.png'", "'/images/products/axiom-arm-sleeve-3d-front-studio.jpg'")

with open('src/services/printify.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated printify.ts sleeve image references!")
