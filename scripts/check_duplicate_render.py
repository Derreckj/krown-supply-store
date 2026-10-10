import urllib.request
import re

html = urllib.request.urlopen('http://localhost:3000/collections/all').read().decode('utf-8')
cards = re.findall(r'class="product-name">(.*?)</h3>', html)
print(f"Total Products rendered on /collections/all: {len(cards)}")

seen = set()
duplicates = []
for c in cards:
    clean = c.strip()
    if clean in seen:
        duplicates.append(clean)
    seen.add(clean)

print(f"Duplicates count: {len(duplicates)}")
if duplicates:
    print("Duplicates found:")
    for d in duplicates:
        print("  -", d)
else:
    print("✓ ZERO duplicates! Catalog is clean and unique.")

print("\nSample Unique Items:")
for c in list(seen)[:8]:
    print("  *", c)
