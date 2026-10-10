import re

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern to extract products
pattern = re.compile(
    r"id:\s*['\"]([^'\"]+)['\"].*?"
    r"name:\s*['\"]([^'\"]+)['\"].*?"
    r"collection:\s*['\"]([^'\"]+)['\"].*?"
    r"images:\s*\[([^\]]*)\]",
    re.DOTALL
)

matches = pattern.findall(text)
print(f"Total products parsed: {len(matches)}")
print("-" * 100)
for pid, name, col, imgs in matches:
    img_matches = re.findall(r"['\"]([^'\"]+)['\"]", imgs)
    first_img = img_matches[0] if img_matches else "NO_IMAGE"
    print(f"{pid:<28} | {col:<22} | {first_img}")
