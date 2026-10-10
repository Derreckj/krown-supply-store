import urllib.request
import json
import time

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

for pid, name in [('6ac7ed40fea4d4e68e0a0f6a', 'Tumbler'), ('6ac7ed0b9bfbeab23800dcdf', 'CC1717 Tee')]:
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{pid}.json'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        prod = json.loads(resp.read().decode())
        print(f"\n=== {name} ===")
        print("Title:", prod['title'])
        print("Locked:", prod.get('is_locked'))
        print("External:", prod.get('external'))
        print("Mockup images:")
        for img in prod.get('images', [])[:3]:
            print(" ", img['src'], "is_default:", img.get('is_default'))
