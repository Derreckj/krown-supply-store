from PIL import Image, ImageFilter
import numpy as np

# Load original crop
hoodie = Image.open('public/images/products/axiom-heavyweight-hoodie-photoreal-v6.jpg').convert('RGB')
crop = hoodie.crop((370, 350, 654, 615))
crop_np = np.array(crop, dtype=np.float32)

# Create a clean mask using color distance and connected components
# The drawstrings are far on the left (x < 35) and right (x > 245)
# In the center (35 <= x <= 245), the owl is the main colored object
h, w = crop.size[1], crop.size[0]
mask = np.zeros((h, w), dtype=np.uint8)

# The owl colors:
# green border: G > 110, G > R*1.3
# purple: R > 70, B > 80, B > G*1.2
# grey: R,G,B all between 60 and 150
# black background of hoodie: R < 38, G < 38, B < 42
for y in range(h):
    for x in range(w):
        # Ignore drawstrings on outer edges
        if x < 40 or x > 244:
            continue
        r, g, b = crop_np[y, x, :3]
        max_val = max(r, g, b)
        if max_val > 45:
            mask[y, x] = 255

# Fill small interior holes
mask_img = Image.fromarray(mask, mode='L')
mask_img = mask_img.filter(ImageFilter.MaxFilter(size=5)).filter(ImageFilter.MinFilter(size=5))
# Smooth edges
mask_smooth = mask_img.filter(ImageFilter.GaussianBlur(radius=1.0))

owl_clean = crop.convert('RGBA')
owl_clean.putalpha(mask_smooth)
owl_clean.save('test_pure_embroidered_owl.png')
print("Saved test_pure_embroidered_owl.png")
