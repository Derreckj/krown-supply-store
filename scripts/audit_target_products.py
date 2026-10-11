import re
import os

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    content = f.read()

products_to_check = [
    'kc-shaker-01',
    'krown-shaker-01',
    'axiom-shaker-01',
    'axiom-hoodie-01',
    'krown-mat-01',
    'axiom-wrist-rest-01',
    'kc-beanie-01',
    'axiom-beanie-01',
    'krown-work-01',
    'krown-tumbler-01'
]

for pid in products_to_check:
    pattern = r"id:\s*'" + pid + r"'.*?name:\s*'(.*?)'.*?collection:\s*'(.*?)'.*?images:\s*\[(.*?)\]"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        name = match.group(1)
        coll = match.group(2)
        raw_imgs = match.group(3)
        imgs = [x.strip().strip("'\"") for x in raw_imgs.split(',') if x.strip()]
        print(f"{pid}:")
        print(f"  Name: {name}")
        print(f"  Collection: {coll}")
        print(f"  Images:")
        for img in imgs:
            full_path = os.path.join('public', img.lstrip('/'))
            exists = os.path.exists(full_path)
            print(f"    - {img} (exists: {exists})")
    else:
        print(f"{pid}: NOT FOUND")
