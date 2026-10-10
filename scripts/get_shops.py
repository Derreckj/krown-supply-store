import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
req = urllib.request.Request('https://api.printify.com/v1/shops.json', headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
with urllib.request.urlopen(req) as resp:
    shops = json.loads(resp.read().decode())
    print("Shops:", json.dumps(shops, indent=2))
