import re

with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    text = f.read()

pids = ['axiom-hoodie-01', 'axiom-dad-hat-01', 'axiom-sweatpants-pro', 'kc-shaker-01', 'krown-shaker-01', 'krown-dadhat-01']

for p in pids:
    idx = text.find(f"'{p}'")
    if idx == -1:
        idx = text.find(f'"{p}"')
    print(f"=== {p} ===")
    chunk = text[idx:idx+1500]
    imgs = re.findall(r'images:\s*\[(.*?)\]', chunk, re.DOTALL)
    if imgs:
        print(imgs[0].strip())
    else:
        print("No images found in chunk")
