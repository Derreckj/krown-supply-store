from PIL import Image, ImageFilter
import numpy as np

# Load blank hat
blank_hat = Image.open('test_blank_hat_seamless.png').convert('RGB')
w_hat, h_hat = blank_hat.size

# Load pure embroidered owl
owl_src = Image.open('test_pure_embroidered_owl_full.png').convert('RGBA')

# Target size for the dad hat front panel
target_w = 185
aspect = owl_src.height / owl_src.width
target_h = int(target_w * aspect)

owl_resized = owl_src.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Position: center front crown
pos_x = (w_hat - target_w) // 2
pos_y = 365

# Create soft fabric contact shadow
shadow_canvas = Image.new('RGBA', blank_hat.size, (0, 0, 0, 0))
owl_alpha = owl_resized.split()[3]
shadow_mask = owl_alpha.filter(ImageFilter.GaussianBlur(radius=3.0))

shadow_patch = Image.new('RGBA', (target_w, target_h), (15, 15, 18, 140))
shadow_patch.putalpha(shadow_mask)
shadow_canvas.paste(shadow_patch, (pos_x + 1, pos_y + 3), mask=shadow_mask)

# Composite shadow then real embroidered owl
result = blank_hat.copy().convert('RGBA')
result = Image.alpha_composite(result, shadow_canvas)
result.paste(owl_resized, (pos_x, pos_y), mask=owl_resized)

result = result.convert('RGB')
result.save('test_axiom_hat_authentic_v3.jpg', quality=95)
print("Saved test_axiom_hat_authentic_v3.jpg successfully")
