import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

new_pids = [
    '6ac80dc2f4d488e1be0b0902',
    '6ac80dff9f3e89dde70da38d',
    '6ac80e034a1cdf2ad60e0bed',
    '6ac80e07cafb2cd4c60b7c96'
]

for pid in new_pids:
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{pid}.json'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        prod = json.loads(resp.read().decode())
        print(f"Product {pid}: {prod['title']}")
        print(f"  Locked: {prod.get('is_locked')}, External: {prod.get('external')}")
