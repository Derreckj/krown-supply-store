from PIL import Image, ImageFilter
import numpy as np
import os

prod_dir = 'public/images/products'
shaker_files = [
    'axiom-shaker-signature-tritan-clean.jpg',
    'axiom-shaker-signature-steel-clean.jpg',
    'axiom-shaker-stealth-tritan-clean.jpg',
    'axiom-shaker-stealth-steel-clean.jpg'
]

# Each image is 768x1376
# We want to produce a 1024x1024 square master image
# In 768x1376, the bottle is from y ~ 110 to y ~ 800 (height ~ 700px, width ~ 380px)
# If we place this in a 1024x1024 canvas:
# We can take the 768x1376 image, center it horizontally (pad 128px left and right),
# and take the y range from y ~ 50 to y ~ 1074 (height 1024)!
# For the left and right 128px margins:
# In the upper half (above desk at y ~ 750), the background is dark gaming room with monitors and purple ambient bokeh
# In the lower half (below desk at y ~ 750), the desk is dark carbon/matte surface with purple LED strip edge
# We can seamlessly replicate/extend the background columns to 1024 width!

for fname in shaker_files:
    path = os.path.join(prod_dir, fname)
    im = Image.open(path).convert('RGB')
    w, h = im.size # 768, 1376
    
    # Crop y from 50 to 1074 (height 1024)
    crop_center = im.crop((0, 50, 768, 1074)) # (768, 1024)
    
    # Create 1024x1024 canvas
    canvas = Image.new('RGB', (1024, 1024), (10, 10, 14))
    
    # Paste center at x = 128
    canvas.paste(crop_center, (128, 0))
    
    # Extend left margin (x: 0 to 128) using blurred/mirrored reflection of x: 0 to 60
    left_sample = crop_center.crop((0, 0, 80, 1024)).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    left_extended = left_sample.resize((128, 1024), Image.Resampling.LANCZOS)
    canvas.paste(left_extended, (0, 0))
    
    # Extend right margin (x: 896 to 1024) using mirrored reflection of x: 708 to 768
    right_sample = crop_center.crop((688, 0, 768, 1024)).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    right_extended = right_sample.resize((128, 1024), Image.Resampling.LANCZOS)
    canvas.paste(right_extended, (896, 0))
    
    # Smooth seams at x=128 and x=896
    arr = np.array(canvas, dtype=np.float32)
    for x in range(120, 136):
        t = (x - 120) / 16.0
        arr[:, x] = (1.0 - t) * arr[:, 119] + t * arr[:, 136]
    for x in range(888, 904):
        t = (x - 888) / 16.0
        arr[:, x] = (1.0 - t) * arr[:, 887] + t * arr[:, 904]
        
    final_square = Image.fromarray(arr.astype(np.uint8), mode='RGB')
    final_square.save(os.path.join(prod_dir, fname), quality=96)
    print(f"Saved 1024x1024 square: {fname}")

print("All 4 Axiom shaker bottle images are now 1024x1024 square masters!")
