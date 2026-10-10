from PIL import Image
import numpy as np

shaker = Image.open('test_krown_shaker.jpg').convert('RGB')
print("Loaded test_krown_shaker.jpg:", shaker.size)

# Let's crop the bottle + whisk region:
# x: 220 to 660, y: 120 to 900
crop = shaker.crop((210, 120, 660, 900))
crop.save('test_shaker_crop.jpg')
print("Saved test_shaker_crop.jpg")
