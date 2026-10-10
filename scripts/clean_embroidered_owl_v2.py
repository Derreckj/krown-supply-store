from PIL import Image, ImageFilter
import numpy as np

# Load original crop
hoodie = Image.open('public/images/products/axiom-heavyweight-hoodie-photoreal-v6.jpg').convert('RGB')
crop = hoodie.crop((370, 350, 654, 615))
crop_np = np.array(crop, dtype=np.float32)

h, w = crop.size[1], crop.size[0]
mask = np.zeros((h, w), dtype=np.uint8)

for y in range(h):
    for x in range(w):
        # Exclude drawstring remnants at the top and bottom pocket seam
        if y < 25 and (x < 85 or x > 155):
            continue
        if y < 10:
            continue
        if y > 252:
            continue
        if x < 42 or x > 240:
            continue
        r, g, b = crop_np[y, x, :3]
        max_val = max(r, g, b)
        if max_val > 42:
            mask[y, x] = 255

mask_img = Image.fromarray(mask, mode='L')
mask_img = mask_img.filter(ImageFilter.MaxFilter(size=5)).filter(ImageFilter.MinFilter(size=5))
mask_smooth = mask_img.filter(ImageFilter.GaussianBlur(radius=0.8))

owl_clean = crop.convert('RGBA')
owl_clean.putalpha(mask_smooth)
owl_clean.save('test_pure_embroidered_owl.png')
print("Saved perfect test_pure_embroidered_owl.png")
