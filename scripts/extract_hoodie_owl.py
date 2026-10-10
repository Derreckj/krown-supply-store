from PIL import Image, ImageFilter
import numpy as np

# Load the hoodie image
hoodie = Image.open('public/images/products/axiom-heavyweight-hoodie-photoreal-v6.jpg').convert('RGB')

# The owl is centered around x=512, y=490
# Let's crop a tight box around the owl: x from 360 to 664 (w=304), y from 350 to 615 (h=265)
crop = hoodie.crop((370, 350, 654, 615))
crop_np = np.array(crop, dtype=np.float32)

# Black fabric background is around (25, 27, 30)
# Green border has high G (G > 120, G > R*1.5), purple has high B/R, grey has R,G,B around 90-140.
# Let's extract mask where the patch exists:
# The black hoodie background around it has R < 45, G < 45, B < 50
bg_dist = np.maximum.reduce([crop_np[:, :, 0], crop_np[:, :, 1], crop_np[:, :, 2]])
mask = np.clip((bg_dist - 35) / 25.0 * 255.0, 0, 255).astype(np.uint8)

# Flood fill or clean up the outside of the patch
mask_img = Image.fromarray(mask, mode='L')
# Let's inspect the mask
crop_rgba = crop.convert('RGBA')
crop_rgba.putalpha(mask_img)
crop_rgba.save('test_isolated_embroidered_owl.png')
print("Saved test_isolated_embroidered_owl.png")
