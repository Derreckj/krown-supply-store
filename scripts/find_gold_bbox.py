from PIL import Image
import numpy as np

im = Image.open('public/images/products/krown-construction-jobsite-tumbler.png').convert('RGB')
arr = np.array(im)

# Detect pixels with gold color:
# Gold has R > 120, G > 90, B < 80, and R > B * 1.5
r = arr[:, :, 0]
g = arr[:, :, 1]
b = arr[:, :, 2]

gold_mask = (r > 80) & (g > 70) & (r > b * 1.3)
ys, xs = np.where(gold_mask)

print(f"Gold bounding box: x from {xs.min()} to {xs.max()}, y from {ys.min()} to {ys.max()}")
