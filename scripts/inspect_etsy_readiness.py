import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

req = urllib.request.Request(
    f'https://api.printify.com/v1/shops/{shop_id}/products.json',
    headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print(f"Total Products: {len(data.get('data', []))}\n")
    for p in data.get('data', []):
        ext = p.get('external', {}) or {}
        imgs = p.get('images', [])
        print("--------------------------------------------------")
        print(f"ID: {p['id']}")
        print(f"Title: {p['title']}")
        print(f"Image Count: {len(imgs)}")
        print(f"Etsy Listing ID: {ext.get('id')} | Handle: {ext.get('handle')}")
