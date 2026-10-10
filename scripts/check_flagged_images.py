import re

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    c = f.read()

pids = [
    'custom-krown-works-hat',
    'krown-dadhat-01',
    'krown-shorts-01',
    'krown-streetwear-set',
    'krown-shaker-01',
    'axiom-hoodie-01',
    'axiom-sweatpants-pro',
    'axiom-dad-hat-01',
    'krown-hoodie-premium',
    'krown-crewneck-01'
]

for pid in pids:
    pattern = r'id:\s*[\'"]' + pid + r'[\'"].*?images:\s*\[(.*?)\]'
    m = re.search(pattern, c, re.DOTALL)
    if m:
        imgs = [i.strip().strip('\'" ') for i in m.group(1).split(',') if i.strip().strip('\'" ')]
        print(f"{pid}:")
        for img in imgs:
            print(f"  {img}")
