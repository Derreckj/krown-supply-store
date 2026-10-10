import re
import os

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all image paths
img_paths = set(re.findall(r'/images/products/[a-zA-Z0-9_\-\.]+', text))

print(f"Total unique product image paths in printify.ts: {len(img_paths)}")
missing = []
for p in sorted(img_paths):
    local_p = os.path.join('public', p.lstrip('/'))
    if not os.path.exists(local_p):
        missing.append((p, local_p))
    else:
        sz = os.path.getsize(local_p)
        if sz < 1000:
            print(f"WARNING small file: {p} ({sz} bytes)")

if missing:
    print(f"MISSING FILES ({len(missing)}):")
    for m in missing:
        print(" ", m[0])
else:
    print("All referenced product images exist on disk and are valid!")
