with open('src/services/printify.ts', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("'axiom-hoodie-01'")
if idx == -1: idx = text.find('"axiom-hoodie-01"')
print(text[idx:idx+2500])
