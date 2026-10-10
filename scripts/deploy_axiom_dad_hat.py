from PIL import Image, ImageFilter
import numpy as np

# Load blank hat
blank_hat = Image.open('test_blank_hat_seamless.png').convert('RGB')
w_hat, h_hat = blank_hat.size

# Load pure embroidered owl
owl_src = Image.open('test_pure_embroidered_owl_full.png').convert('RGBA')

# Target size: 185w x ~210h
target_w = 185
aspect = owl_src.height / owl_src.width
target_h = int(target_w * aspect)

owl_resized = owl_src.resize((target_w, target_h), Image.Resampling.LANCZOS)
owl_np = np.array(owl_resized)

# Clean any tiny stray specks outside the main connected component
# Check alpha channel
alpha = owl_np[:, :, 3]
# Any stray pixel in top 20 rows with x > 140
for y in range(35):
    for x in range(130, target_w):
        # The right horn is around x=135-155, y=5-35
        # Anything far right x > 156 in the top 35 rows is stray
        if x > 155:
            owl_np[y, x, 3] = 0

owl_cleaned = Image.fromarray(owl_np, mode='RGBA')

# Position: center front crown
pos_x = (w_hat - target_w) // 2
pos_y = 368

# Create soft fabric contact shadow
shadow_canvas = Image.new('RGBA', blank_hat.size, (0, 0, 0, 0))
owl_alpha = owl_cleaned.split()[3]
shadow_mask = owl_alpha.filter(ImageFilter.GaussianBlur(radius=3.0))

shadow_patch = Image.new('RGBA', (target_w, target_h), (15, 15, 18, 140))
shadow_patch.putalpha(shadow_mask)
shadow_canvas.paste(shadow_patch, (pos_x + 1, pos_y + 3), mask=shadow_mask)

# Composite shadow then real embroidered owl
result = blank_hat.copy().convert('RGBA')
result = Image.alpha_composite(result, shadow_canvas)
result.paste(owl_cleaned, (pos_x, pos_y), mask=owl_cleaned)

result = result.convert('RGB')
result.save('public/images/products/axiom-dad-hat-photoreal-v6.jpg', quality=95)
result.save('public/images/products/axiom-dad-hat-washed-black.jpg', quality=95)
result.save('public/images/products/axiom-dad-hat-washed-black-v2.jpg', quality=95)
result.save('public/images/products/axiom-dad-hat-washed-black-v3.jpg', quality=95)
result.save('public/images/products/axiom-dad-hat-washed-black-v4.jpg', quality=95)
print("Saved all Axiom dad hat variants successfully!")
