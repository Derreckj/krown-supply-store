import urllib.request
import json
import os

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

url = f'https://api.printify.com/v1/shops/{shop_id}/products.json'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print(f'Total products in shop {shop_id}: {data.get("total")}')
    for p in data.get('data', []):
        print('-----------------------------------------')
        print(f"ID: {p['id']}")
        print(f"Title: {p['title']}")
        print(f"Blueprint: {p.get('blueprint_id')}")
        print(f"Print Provider: {p.get('print_provider_id')}")
        variants = p.get('variants', [])
        print(f"Variants count: {len(variants)}")
        if variants:
            print(f"Sample price: ${variants[0].get('price') / 100:.2f}")
        images = p.get('images', [])
        print(f"Images count: {len(images)}")
