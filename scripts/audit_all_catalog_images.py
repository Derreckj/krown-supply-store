import re
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINTIFY_TS = os.path.join(BASE_DIR, "src", "services", "printify.ts")
PUB_DIR = os.path.join(BASE_DIR, "public")

with open(PRINTIFY_TS, "r", encoding="utf-8") as f:
    content = f.read()

# Match each object in the products array
# Each product has id: '...', name: '...', images: [...]
product_blocks = re.findall(r"\{\s*id:\s*['\"]([^'\"]+)['\"].*?name:\s*['\"]([^'\"]+)['\"].*?images:\s*\[(.*?)\]", content, re.DOTALL)

print(f"Total products found: {len(product_blocks)}")
print("=" * 80)

for pid, name, images_str in product_blocks:
    # parse images
    raw_imgs = re.findall(r"['\"](/images/[^'\"]+)['\"]", images_str)
    print(f"\nProduct: [{pid}] {name}")
    for img_rel in raw_imgs:
        disk_path = os.path.normpath(os.path.join(PUB_DIR, img_rel.lstrip("/")))
        if not os.path.exists(disk_path):
            print(f"  [MISSING] {img_rel}")
        else:
            try:
                im = Image.open(disk_path)
                print(f"  [OK] {img_rel} ({im.size[0]}x{im.size[1]}, {im.format})")
            except Exception as e:
                print(f"  [CORRUPT] {img_rel} ({e})")
