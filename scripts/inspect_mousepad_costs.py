import urllib.request, json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

url = f'https://api.printify.com/v1/shops/{shop_id}/products.json'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    for p in data.get('data', []):
        if 'desk mat' in p['title'].lower() or 'mouse pad' in p['title'].lower():
            print(f"Product ID: {p['id']} - {p['title']}")
            print(f"Blueprint: {p.get('blueprint_id')}, Provider: {p.get('print_provider_id')}")
            for v in p.get('variants', []):
                pr = v.get('price', 0) / 100.0
                co = v.get('cost', 0) / 100.0
                margin = pr - co
                pct = (margin / pr * 100.0) if pr > 0 else 0
                print(f"  Variant {v.get('id')}: {v.get('title')} | Price: ${pr:.2f} | Base Cost: ${co:.2f} | Profit: ${margin:.2f} ({pct:.1f}%)")
