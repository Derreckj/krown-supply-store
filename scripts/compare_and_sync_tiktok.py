import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))
api_key = env['PRINTIFY_API_KEY']
headers = {'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'}

def get_prods(shop_id):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products.json'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode()).get('data', [])

etsy_prods = get_prods(29252381)
tiktok_prods = get_prods(29241235)

print('=== ETSY SHOP (29252381) PRODUCTS ===')
for p in etsy_prods:
    print(f"ID: {p['id']} | Title: {p['title']} | Blueprint: {p.get('blueprint_id')} | Provider: {p.get('print_provider_id')}")

print('\n=== TIKTOK SHOP (29241235) PRODUCTS ===')
for p in tiktok_prods:
    print(f"ID: {p['id']} | Title: {p['title']} | Blueprint: {p.get('blueprint_id')} | Provider: {p.get('print_provider_id')}")
