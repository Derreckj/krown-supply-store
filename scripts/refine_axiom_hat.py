from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np

# Load blank hat
blank_hat = Image.open('test_blank_hat_seamless.png').convert('RGB')
w_hat, h_hat = blank_hat.size

# Load Axiom owl
owl_src = Image.open('public/images/branding/gaming/axiom-owl-mascot.png').convert('RGBA')

# Target size: 195px wide, centered on the front crown panel
# This matches the exact visual proportion of premium dad hats (like Polo, Supreme, Krown)
target_w = 195
aspect = owl_src.height / owl_src.width
target_h = int(target_w * aspect)

owl_resized = owl_src.resize((target_w, target_h), Image.Resampling.LANCZOS)
owl_np = np.array(owl_resized, dtype=np.float32)
alpha = owl_np[:, :, 3] / 255.0

# 1. Thread texture (embroidery satin stitch)
y, x = np.mgrid[0:target_h, 0:target_w]
# Thread stitch frequency: 1 stitch every ~3 pixels, angled at 50 degrees
thread_pattern = np.sin((x * 0.65 + y * 0.75) * 2 * np.pi / 2.8) * 0.16
thread_sheen = 1.0 + thread_pattern

# 2. Emboss / directional 3D lighting (light from top-left ~ -1, -1)
# Create a height map from the luminance + alpha
gray = (0.299 * owl_np[:, :, 0] + 0.587 * owl_np[:, :, 1] + 0.114 * owl_np[:, :, 2]) / 255.0
height_map = gray * alpha

# Calculate gradients (Sobel-like)
gy, gx = np.gradient(height_map)
# Directional light vector: top-left (-0.6, -0.6, 0.5)
light_x, light_y, light_z = -0.5, -0.6, 0.6
norm = np.sqrt(gx**2 + gy**2 + 0.25)
nx = -gx / norm
ny = -gy / norm
nz = 0.5 / norm
diffuse = nx * light_x + ny * light_y + nz * light_z
diffuse = np.clip(diffuse * 0.4 + 0.85, 0.65, 1.35)

# Apply embroidery thread texture and 3D lighting
for c in range(3):
    owl_np[:, :, c] = np.clip(owl_np[:, :, c] * thread_sheen * diffuse, 0, 255)

# Extract twill texture from the hat at the exact placement to blend into the threads
pos_x = (w_hat - target_w) // 2
pos_y = 365  # Perfectly centered on the front crown! (Visor seam is at ~570)

hat_crop = np.array(blank_hat.crop((pos_x, pos_y, pos_x + target_w, pos_y + target_h)), dtype=np.float32)
hat_gray = (0.299 * hat_crop[:, :, 0] + 0.587 * hat_crop[:, :, 1] + 0.114 * hat_crop[:, :, 2])
hat_twill = (hat_gray - np.mean(hat_gray)) / 255.0 * 0.08  # subtle twill grain

for c in range(3):
    owl_np[:, :, c] = np.clip(owl_np[:, :, c] * (1.0 + hat_twill), 0, 255)

# Micro edge softening so it looks stitched into cotton twill
alpha_img = Image.fromarray((alpha * 255).astype(np.uint8), mode='L')
alpha_edge = alpha_img.filter(ImageFilter.GaussianBlur(radius=0.9))

embroidery_rgba = Image.fromarray(owl_np.astype(np.uint8), mode='RGBA')
embroidery_rgba.putalpha(alpha_edge)

# Realistic contact drop shadow into the fabric weave
shadow_canvas = Image.new('RGBA', blank_hat.size, (0, 0, 0, 0))
shadow_mask = alpha_img.filter(ImageFilter.GaussianBlur(radius=3.5))
shadow_patch = Image.new('RGBA', (target_w, target_h), (10, 10, 10, 150))
shadow_patch.putalpha(shadow_mask)
shadow_canvas.paste(shadow_patch, (pos_x + 1, pos_y + 3), mask=shadow_mask)

# Composite together
result = blank_hat.copy().convert('RGBA')
result = Image.alpha_composite(result, shadow_canvas)
result.paste(embroidery_rgba, (pos_x, pos_y), mask=embroidery_rgba)

result = result.convert('RGB')
result.save('test_axiom_hat_v2.jpg', quality=95)
print("Saved test_axiom_hat_v2.jpg successfully")
