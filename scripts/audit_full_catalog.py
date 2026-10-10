import re
import os

printify_file = r'src/services/printify.ts'
with open(printify_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all product definitions
pattern = r"id:\s*['\"]([^'\"]+)['\"],\s*\n\s*name:\s*['\"]([^'\"]+)['\"],\s*\n\s*slug:\s*['\"]([^'\"]+)['\"].*?collection:\s*['\"]([^'\"]+)['\"].*?images:\s*\[(.*?)\]"
matches = re.findall(pattern, content, re.DOTALL)

print(f"Total products matched: {len(matches)}\n")

all_missing = {}

for pid, name, slug, collection, img_block in matches:
    images = re.findall(r"['\"](/images/[^'\"]+)['\"]", img_block)
    missing = []
    for img in images:
        path = os.path.join('.', 'public', img.replace('/images/', 'images/').lstrip('/'))
        if not os.path.exists(path):
            missing.append(img)
    
    status = "OK" if not missing else "MISSING FILES"
    print(f"[{pid}] {name}")
    print(f"  Collection: {collection}")
    print(f"  Primary Image: {images[0] if images else 'None'}")
    print(f"  Total Images: {len(images)}")
    if missing:
        print(f"  ⚠️ Missing: {missing}")
        all_missing[pid] = missing
    print()

if not all_missing:
    print("ALL PRODUCT IMAGES EXIST ON DISK WITH 0 MISSING FILES!")
else:
    print(f"Products with missing images: {len(all_missing)}")
