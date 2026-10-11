import os, json, requests

api_key = None
shop_id = None
if os.path.exists('.env.local'):
    with open('.env.local', 'r') as f:
        for line in f:
            if line.startswith('PRINTIFY_API_KEY='):
                api_key = line.strip().split('=', 1)[1]
            elif line.startswith('PRINTIFY_SHOP_ID='):
                shop_id = line.strip().split('=', 1)[1]

headers = {'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'}
shops_res = requests.get('https://api.printify.com/v1/shops.json', headers=headers).json()
for s in shops_res:
    s_id = s['id']
    s_title = s['title']
    print(f'=== SHOP {s_id}: {s_title} ===')
    prods_res = requests.get(f'https://api.printify.com/v1/shops/{s_id}/products.json', headers=headers).json()
    for p in prods_res.get('data', []):
        t = p['title'].lower()
        if 'mat' in t or 'mouse' in t or 'pad' in t:
            print(f"  Product ID: {p['id']}, Title: {p['title']}")
            for img in p.get('images', []):
                print(f"    is_default={img.get('is_default')}, src={img.get('src')}")
