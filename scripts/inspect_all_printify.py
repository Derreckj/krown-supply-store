import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

print("--- Uploaded Images ---")
uploads = get('https://api.printify.com/v1/uploads.json?limit=50')
for u in uploads.get('data', []):
    print(f"ID: {u['id']} | Name: {u.get('file_name')} | Size: {u.get('width')}x{u.get('height')}")

print("\n--- Current Products in Shop ---")
prods = get(f'https://api.printify.com/v1/shops/{shop_id}/products.json')
for p in prods.get('data', []):
    print(f"Product: {p['id']} | Title: {p['title'][:60]} | BP: {p['blueprint_id']} | Provider: {p['print_provider_id']}")
