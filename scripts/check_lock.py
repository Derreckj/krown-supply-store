import urllib.request
import json
import time

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']
product_id = '6ac7ed0b9bfbeab23800dcdf'

for i in range(15):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{product_id}.json'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        prod = json.loads(resp.read().decode())
        locked = prod.get('is_locked', False)
        print(f"Attempt {i+1}: is_locked = {locked}")
        if not locked:
            print("Product unlocked!")
            break
    time.sleep(3)
