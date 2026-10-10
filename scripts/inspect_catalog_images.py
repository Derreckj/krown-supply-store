import re
import os

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Match each product block
items = re.split(r'\{\s*id:\s*[\'"]', content)[1:]
for item in items:
    pid_match = re.match(r'([^\'"]+)', item)
    if not pid_match:
        continue
    pid = pid_match.group(1)
    name_match = re.search(r'name:\s*[\'"]([^\'"]+)', item)
    name = name_match.group(1) if name_match else 'Unknown'
    img_match = re.search(r'images:\s*\[(.*?)\]', item, re.DOTALL)
    images = []
    if img_match:
        images = [im.strip().strip('\'" ') for im in img_match.group(1).split(',') if im.strip().strip('\'" ')]
    first_img = images[0] if images else 'NONE'
    
    # Check if file exists on disk
    disk_path = os.path.join('public', first_img.lstrip('/'))
    exists = os.path.exists(disk_path)
    print(f"{pid:25} | {name[:40]:40} | exists={exists} | {first_img}")
