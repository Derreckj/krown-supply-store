import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

url = f'https://api.printify.com/v1/shops/{shop_id}/products/6ac7ed40fea4d4e68e0a0f6a.json'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
with urllib.request.urlopen(req) as resp:
    p = json.loads(resp.read().decode())
    print("Tumbler ID:", p['id'])
    print("External:", p.get('external'))
    print("Variants:", p.get('variants'))
