import re

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all product definitions
product_chunks = re.split(r'\{\s*id:\s*[\'"]', text)[1:]
axiom_products = []

for chunk in product_chunks:
    pid = chunk.split("'")[0].split('"')[0]
    coll_m = re.search(r'collection:\s*[\'"]([^\'"]+)', chunk)
    coll = coll_m.group(1) if coll_m else ''
    if 'AXA' in coll or 'Axiom' in coll:
        name_m = re.search(r'name:\s*[\'"]([^\'"]+)', chunk)
        name = name_m.group(1) if name_m else ''
        imgs_m = re.search(r'images:\s*\[(.*?)\]', chunk, re.DOTALL)
        imgs = re.findall(r'[\'"]([^\'"]+)[\'"]', imgs_m.group(1)) if imgs_m else []
        axiom_products.append({
            'id': pid,
            'name': name,
            'collection': coll,
            'images': imgs
        })

print(f"Found {len(axiom_products)} Axiom Allegiance products:")
for p in axiom_products:
    print(f"\nProduct: [{p['id']}] {p['name']}")
    for img in p['images']:
        print(f"   Image: {img}")
