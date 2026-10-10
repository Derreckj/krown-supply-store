from PIL import Image, ImageFilter
import numpy as np

whisk = Image.open('test_whisk_crop3.jpg').convert('RGB')
w, h = whisk.size
whisk_np = np.array(whisk, dtype=np.float32)

# The wire is shiny stainless steel: R, G, B values are high (> 70)
# Dark table background has R, G, B < 40
# Let's compute a clean luminance mask:
lum = (0.299 * whisk_np[:, :, 0] + 0.587 * whisk_np[:, :, 1] + 0.114 * whisk_np[:, :, 2])

# Threshold for wire highlights:
# Soft sigmoid ramp between 38 and 85
wire_mask = np.clip((lum - 38.0) / 45.0, 0.0, 1.0)

# Outside the circular sphere of the whisk ball (center ~ 110, 125, radius ~ 95), alpha should be 0:
y, x = np.mgrid[0:h, 0:w]
dist_center = np.sqrt((x - 110)**2 + (y - 125)**2)
circle_fade = np.clip(1.0 - (dist_center - 88) / 10.0, 0.0, 1.0)

final_alpha = (wire_mask * circle_fade * 255.0).astype(np.uint8)
alpha_img = Image.fromarray(final_alpha, mode='L')
alpha_smooth = alpha_img.filter(ImageFilter.GaussianBlur(radius=0.5))

whisk_rgba = whisk.convert('RGBA')
whisk_rgba.putalpha(alpha_smooth)
whisk_rgba.save('test_isolated_whisk.png')
print("Saved test_isolated_whisk.png")
