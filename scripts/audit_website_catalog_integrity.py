import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

scratch = r'c:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store'
pub_dir = os.path.join(scratch, 'public')
printify_ts_path = os.path.join(scratch, 'src', 'services', 'printify.ts')

with open(printify_ts_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Extract all image paths referenced in printify.ts
img_refs = re.findall(r"['\"](/images/[^'\"]+)['\"]", code)
img_refs = list(set(img_refs))

print(f"=== CHECKING {len(img_refs)} IMAGE PATHS REFERENCED IN PRINTIFY.TS ===")
missing_images = []
for ref in img_refs:
    # remove leading /
    local_path = os.path.join(pub_dir, ref.lstrip('/'))
    if not os.path.exists(local_path):
        missing_images.append(ref)
    else:
        size = os.path.getsize(local_path)
        if size == 0:
            missing_images.append(f"{ref} (0 bytes)")

if missing_images:
    print(f"❌ FAILED: {len(missing_images)} missing or empty images found:")
    for m in missing_images:
        print(f"  - {m}")
else:
    print(f"✅ ALL {len(img_refs)} IMAGE ASSETS EXIST AND ARE NON-EMPTY ON DISK!")

# Verify collections separation
print("\n=== BRAND SEPARATION AUDIT ===")
prod_blocks = re.findall(r"id:\s*['\"]([^'\"]+)['\"][\s\S]*?name:\s*['\"]([^'\"]+)['\"][\s\S]*?collection:\s*['\"]([^'\"]+)['\"]", code)

allowed_collections = {'KrowN Supply Co.', 'KrowN Construction', 'AXA / Axiom Allegiance', 'KrowN Gaming', 'Accessories'}
collection_counts = {}
brand_errors = []

for pid, name, coll in prod_blocks:
    collection_counts[coll] = collection_counts.get(coll, 0) + 1
    if coll not in allowed_collections:
        brand_errors.append(f"Unknown collection: {coll} on {pid}")
    
    # Check for cross-contamination
    name_lower = name.lower()
    if coll == 'KrowN Construction':
        if 'axiom' in name_lower or 'axa' in name_lower:
            brand_errors.append(f"Axiom in Construction: {pid} - {name}")
    elif coll == 'KrowN Supply Co.':
        if 'construction' in name_lower or 'axiom' in name_lower:
            brand_errors.append(f"Cross-brand in Supply Co: {pid} - {name}")
    elif coll == 'AXA / Axiom Allegiance':
        if 'construction' in name_lower:
            brand_errors.append(f"Construction in Axiom: {pid} - {name}")

for coll, count in collection_counts.items():
    print(f"  • {coll:<25}: {count:2d} products")

if brand_errors:
    print(f"\n❌ BRAND CROSS-CONTAMINATION DETECTED:")
    for e in brand_errors:
        print(f"  - {e}")
else:
    print("\n✅ ZERO BRAND CROSS-CONTAMINATION DETECTED! 100% STRICT SEPARATION CONFIRMED.")
