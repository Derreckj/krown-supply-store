import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

url = 'https://api.printify.com/v1/catalog/blueprints/706/print_providers/3/variants.json'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print("Total variants for CC1717 / Monster Digital:", len(data.get('variants', [])))
    for v in data.get('variants', []):
        print(f"ID: {v['id']} | Title: {v['title']} | Options: {v.get('options')}")
