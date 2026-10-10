import os
import re
from PIL import Image
import numpy as np

# Load products from printify.ts
with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    ts_code = f.read()

# Extract all product blocks
# Matches id: '...', name: '...', collection: '...', images: [...]
product_matches = re.findall(
    r"id:\s*['\"]([^'\"]+)['\"].*?name:\s*['\"]([^'\"]+)['\"].*?collection:\s*['\"]([^'\"]+)['\"].*?images:\s*\[(.*?)\]",
    ts_code,
    re.DOTALL
)

print(f"Total products parsed from printify.ts: {len(product_matches)}\n")

issues = []

for pid, name, collection, images_raw in product_matches:
    img_urls = re.findall(r"['\"](/images/products/[^'\"]+)['\"]", images_raw)
    
    for url in img_urls:
        local_path = os.path.join('public', url.lstrip('/'))
        if not os.path.exists(local_path):
            issues.append(f"MISSING FILE: {name} ({pid}) -> {url}")
            continue
            
        size_kb = os.path.getsize(local_path) / 1024.0
        if size_kb < 15:
            issues.append(f"SUSPICIOUSLY SMALL FILE: {name} ({pid}) -> {url} ({size_kb:.1f} KB)")
            
        try:
            im = Image.open(local_path)
            w, h = im.size
            
            # Check aspect ratio
            if abs(w - h) > 50 and not ('banner' in url.lower() or 'lineup' in url.lower() or '3-editions' in url.lower() or '4-editions' in url.lower()):
                issues.append(f"NON-SQUARE PRODUCT IMAGE: {name} ({pid}) -> {url} ({w}x{h})")
                
            # Check for black pillarbox borders (e.g. phone aspect squeezed into square)
            arr = np.array(im.convert('RGB'))
            left_col = arr[:, :20, :]
            right_col = arr[:, -20:, :]
            if np.mean(left_col) < 5 and np.mean(right_col) < 5 and np.mean(arr[:, 200:800, :]) > 30:
                issues.append(f"PILLARBOX DETECTED: {name} ({pid}) -> {url}")
                
            # Brand integrity checks
            if 'AXA' in collection or 'Axiom' in collection or 'axiom' in pid:
                # Check for gold crown pixels on Axiom products
                # Gold has R > 150, G > 120, B < 80, and R > B * 1.8
                r = arr[:, :, 0]
                g = arr[:, :, 1]
                b = arr[:, :, 2]
                gold_pixels = (r > 160) & (g > 130) & (b < 80) & (r > b * 2.0)
                gold_count = np.sum(gold_pixels)
                # Small highlights are fine, but a gold crown has thousands of gold pixels
                if gold_count > 1200 and 'wrist' not in pid and 'shorts' not in pid:
                    issues.append(f"BRAND CONTAMINATION: Gold crown detected on Axiom product! {name} ({pid}) -> {url} ({gold_count} gold pixels)")
                    
        except Exception as e:
            issues.append(f"ERROR reading {url}: {e}")

print("=== CATALOG AUDIT RESULTS ===")
if not issues:
    print("PERFECT: Zero issues found across all product images in printify.ts!")
else:
    print(f"Found {len(issues)} issues:")
    for iss in issues:
        print("  *", iss)
