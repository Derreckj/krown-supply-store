import re
import os

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    content = f.read()

products = [
    'axiom-wrist-rest-01',
    'axiom-beanie-01',
    'axiom-sweatpants-pro',
    'axiom-dad-hat-01',
    'axiom-stickers-01'
]

for pid in products:
    pattern = r"id:\s*'" + pid + r"'.*?name:\s*'(.*?)'.*?collection:\s*'(.*?)'.*?images:\s*\[(.*?)\]"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        name = match.group(1)
        coll = match.group(2)
        raw_imgs = match.group(3)
        imgs = [x.strip().strip("'\"") for x in raw_imgs.split(',') if x.strip()]
        print(f"\n=== {pid} ===")
        print(f"Name: {name}")
        print(f"Collection: {coll}")
        print(f"Images: {imgs}")
        
        # Check variants
        var_pattern = r"id:\s*'" + pid + r"'.*?variants:\s*\[(.*?)\]"
        var_match = re.search(var_pattern, content, re.DOTALL)
        if var_match:
            print(f"Variants: {var_match.group(1).strip()[:300]}...")
