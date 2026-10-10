from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np

# Load blank hat
blank_hat = Image.open('test_blank_hat_seamless.png').convert('RGB')
w_hat, h_hat = blank_hat.size

# Load Axiom owl
owl_src = Image.open('public/images/branding/gaming/axiom-owl-mascot.png').convert('RGBA')

# Target size on the dad hat:
# A realistic dad hat embroidery is about 220px wide by 235px high
target_w = 230
aspect = owl_src.height / owl_src.width
target_h = int(target_w * aspect)

owl_resized = owl_src.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Create 3D embroidery effect:
# 1. Thread texture / satin stitch lines
# We generate microscopic diagonal thread ridges across the owl
owl_np = np.array(owl_resized, dtype=np.float32)
alpha = owl_np[:, :, 3] / 255.0

# Generate thread angle pattern (e.g. 45 degree satin stitch)
y, x = np.mgrid[0:target_h, 0:target_w]
# Thread stitch frequency: 1 stitch every ~3.5 pixels
thread_pattern = np.sin((x * 0.7 + y * 0.7) * 2 * np.pi / 3.5) * 0.12  # subtle +/- 12% intensity
thread_sheen = (1.0 + thread_pattern)

# Apply thread pattern to RGB channels where alpha > 0.1
for c in range(3):
    owl_np[:, :, c] = np.clip(owl_np[:, :, c] * thread_sheen, 0, 255)

# 2. Emboss / bevel for 3D raised puff embroidery
# Create height map from alpha and inner edges
alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode='L')
# Relief highlight (top-left light source: -1, -1)
# Contact drop shadow (bottom-right: +2, +3)
shadow_mask = alpha_img.filter(ImageFilter.GaussianBlur(radius=4))
shadow_offset = Image.new('L', (target_w, target_h), 0)

# 3. Micro edge softness: embroidery threads have micro fiber edges (not razor sharp vector lines)
alpha_smooth = alpha_img.filter(ImageFilter.GaussianBlur(radius=0.8))

# Let's create the final embroidered owl RGBA
embroidery_rgba = Image.fromarray(owl_np.astype(np.uint8), mode='RGBA')
embroidery_rgba.putalpha(alpha_smooth)

# Subtle spherical curvature warp (hat crown is curved):
# We can apply a slight barrel/pincushion mesh or vertical bulge
# The dad hat center is around (512, 450)
pos_x = (w_hat - target_w) // 2
pos_y = 445  # Right on the front crown above the brim

# Soft contact shadow onto the cap twill:
shadow_canvas = Image.new('RGBA', blank_hat.size, (0, 0, 0, 0))
shadow_patch = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 160))
shadow_patch.putalpha(shadow_mask)
shadow_canvas.paste(shadow_patch, (pos_x + 1, pos_y + 3), mask=shadow_mask)
shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(radius=3))

# Composite shadow then embroidery onto blank hat
result = blank_hat.copy().convert('RGBA')
result = Image.alpha_composite(result, shadow_canvas)
result.paste(embroidery_rgba, (pos_x, pos_y), mask=embroidery_rgba)

result = result.convert('RGB')
result.save('test_axiom_hat_v1.jpg', quality=95)
print("Saved test_axiom_hat_v1.jpg successfully")
