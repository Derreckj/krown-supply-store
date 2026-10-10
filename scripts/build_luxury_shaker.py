from PIL import Image, ImageFilter
import numpy as np

# Load base tumbler image
base_img = Image.open('public/images/products/krown-construction-jobsite-tumbler-32oz.png').convert('RGB')
w, h = base_img.size

# Load pure 3D gold crown
crown = Image.open('test_pure_gold_crown.png').convert('RGBA')

# In base_img, the bottle is in the center:
# x: ~320 to ~670, y: ~135 to ~830
# The KC logo is on the bottle from y: ~320 to ~570
# Let's inspect the bottle surface color:
# Matte black powder coat with subtle vertical light reflection
base_np = np.array(base_img, dtype=np.float32)

# Create a clean patch over the KC logo:
# Let's sample the matte black powder coat color from just above the logo (y=290 to 320) and below (y=610 to 640)
# The bottle has a natural cylindrical lighting gradient: darker on left and right, subtle highlight near center (x~500)
# We can inpaint/blend the matte black bottle texture smoothly across the logo area!

print("Tumbler size:", base_img.size)
