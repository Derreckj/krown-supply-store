import os
import shutil
from PIL import Image

MASTER_SRC = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7\.user_uploaded\media_1791726803679.png"
PROD_DIR = r"c:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store\public\images\products"
MASTERS_DIR = os.path.join(PROD_DIR, "masters")
os.makedirs(MASTERS_DIR, exist_ok=True)

src = Image.open(MASTER_SRC).convert("RGB")
W, H = src.size

def make_sq_studio(crop_box, target_size=(1600, 1600), bg_color=(23, 27, 28)):
    """Crops the specified region, creates a seamless dark slate studio backdrop, and centers the garment."""
    cropped = src.crop(crop_box)
    cw, ch = cropped.size
    
    pad = 80
    max_w = target_size[0] - pad * 2
    max_h = target_size[1] - pad * 2
    
    ratio = min(max_w / cw, max_h / ch)
    new_w = int(cw * ratio)
    new_h = int(ch * ratio)
    
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    out = Image.new("RGB", target_size, bg_color)
    paste_x = (target_size[0] - new_w) // 2
    paste_y = (target_size[1] - new_h) // 2
    
    out.paste(resized, (paste_x, paste_y))
    return out

print("--- 1. Generating Main 3-View Studio Composite ---")
# 1. Main Thumbnail: High-res square master showing Front, Back, and Left Sleeve side-by-side
comp_sq = Image.new("RGB", (1600, 1600), (23, 27, 28))
ratio = min(1520 / W, 1520 / H)
comp_w = int(W * ratio)
comp_h = int(H * ratio)
resized_comp = src.resize((comp_w, comp_h), Image.Resampling.LANCZOS)
comp_sq.paste(resized_comp, ((1600 - comp_w) // 2, (1600 - comp_h) // 2))

main_path = os.path.join(PROD_DIR, "axiom-crewneck-sweatshirt-studio.jpg")
comp_sq.save(main_path, "JPEG", quality=95)
comp_sq.save(os.path.join(MASTERS_DIR, "axiom-crewneck-sweatshirt-studio.jpg"), "JPEG", quality=95)
print(f"Saved: {main_path}")

print("--- 2. Generating Front View ---")
# Front: x=20 to 382 isolates front view with zero adjacent bleed
front_img = make_sq_studio((20, 45, 382, 545))
front_path = os.path.join(PROD_DIR, "axiom-crewneck-sweatshirt-front.jpg")
front_img.save(front_path, "JPEG", quality=95)
front_img.save(os.path.join(MASTERS_DIR, "axiom-crewneck-sweatshirt-front.jpg"), "JPEG", quality=95)
print(f"Saved: {front_path}")

print("--- 3. Generating Back View ---")
# Back: x=420 to 765 isolates back view with zero front or sleeve bleed
back_img = make_sq_studio((420, 45, 765, 545))
back_path = os.path.join(PROD_DIR, "axiom-crewneck-sweatshirt-back.jpg")
back_img.save(back_path, "JPEG", quality=95)
back_img.save(os.path.join(MASTERS_DIR, "axiom-crewneck-sweatshirt-back.jpg"), "JPEG", quality=95)
print(f"Saved: {back_path}")

print("--- 4. Generating Sleeve Detail ---")
# Sleeve: x=805 to 985 isolates sleeve view with zero back view bleed
sleeve_img = make_sq_studio((805, 45, 985, 545))
sleeve_path = os.path.join(PROD_DIR, "axiom-crewneck-sleeve-detail.jpg")
sleeve_img.save(sleeve_path, "JPEG", quality=95)
sleeve_img.save(os.path.join(MASTERS_DIR, "axiom-crewneck-sleeve-detail.jpg"), "JPEG", quality=95)
print(f"Saved: {sleeve_path}")

print("--- 5. Generating Front Chest Macro ---")
chest_crop = src.crop((75, 120, 355, 420))
cw, ch = chest_crop.size
ratio = min(1400 / cw, 1400 / ch)
resized_chest = chest_crop.resize((int(cw * ratio), int(ch * ratio)), Image.Resampling.LANCZOS)
chest_sq = Image.new("RGB", (1600, 1600), (23, 27, 28))
chest_sq.paste(resized_chest, ((1600 - resized_chest.width) // 2, (1600 - resized_chest.height) // 2))
chest_path = os.path.join(PROD_DIR, "axiom-crewneck-chest-macro.jpg")
chest_sq.save(chest_path, "JPEG", quality=95)
chest_sq.save(os.path.join(MASTERS_DIR, "axiom-crewneck-chest-macro.jpg"), "JPEG", quality=95)
print(f"Saved: {chest_path}")

print("--- 6. Verifying Model Image ---")
model_path = os.path.join(PROD_DIR, "axiom-crewneck-sweatshirt-model.jpg")
if os.path.exists(model_path):
    print(f"Model image verified: {model_path} ({os.path.getsize(model_path)} bytes)")

print("Completed all high-resolution mockup renders successfully!")
