import shutil
import os

prod_dir = 'public/images/products'
studio_src = os.path.join(prod_dir, 'axiom-sweatpants-pro-heavyweight-studio.jpg')
photoreal_dst = os.path.join(prod_dir, 'axiom-sweatpants-pro-photoreal-v6.jpg')

# Overwrite the cloned model file with the pristine studio flat-lay
shutil.copyfile(studio_src, photoreal_dst)
print("Overwrote axiom-sweatpants-pro-photoreal-v6.jpg with pristine studio master!")

# Update src/services/printify.ts so axiom-sweatpants-pro has axiom-sweatpants-pro-heavyweight-studio.jpg first
with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Check for axiom-sweatpants-pro
idx = text.find("'axiom-sweatpants-pro'")
if idx == -1: idx = text.find('"axiom-sweatpants-pro"')
end_idx = text.find('}', text.find('variants:', idx) + 500)
chunk = text[idx:end_idx]

print("Current chunk images:\n", chunk[:400])
