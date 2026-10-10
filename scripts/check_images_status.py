from PIL import Image
import os

images_to_check = [
    'axiom-heavyweight-hoodie-photoreal-v6.jpg',
    'axiom-heavyweight-hoodie-model-v6.jpg',
    'axiom-dad-hat-photoreal-v6.jpg',
    'krown-dad-hat-photoreal-v6.jpg',
    'axiom-sweatpants-pro-photoreal-v6.jpg',
    'axiom-sweatpants-pro-heavyweight-studio.jpg',
    'kc-shaker-photoreal-v6.jpg',
    'kc-shaker-steelcore-v6.jpg',
    'kc-shaker-tradesman-v6.jpg',
    'krown-shaker-photoreal-v6.jpg',
    'krown-shaker-smoke-v6.jpg',
    'krown-shaker-brushed-v6.jpg'
]

for name in images_to_check:
    path = os.path.join('public/images/products', name)
    if os.path.exists(path):
        img = Image.open(path)
        print(f"{name}: {img.size}, mode={img.mode}, {os.path.getsize(path)/1024:.1f} KB")
    else:
        print(f"MISSING: {name}")
