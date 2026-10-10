import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

# Check blueprint 2001 placeholders
url = 'https://api.printify.com/v1/catalog/blueprints/2001/print_providers/99/variants.json'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print("BP 2001 keys:", list(data.keys()))
    # Let's inspect blueprint 2001 details from catalog
    bp = json.loads(urllib.request.urlopen(urllib.request.Request('https://api.printify.com/v1/catalog/blueprints/2001.json', headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})).read().decode())
    print("BP 2001 title:", bp.get('title'), "images:", len(bp.get('images', [])))
