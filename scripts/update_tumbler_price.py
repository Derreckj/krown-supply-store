import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

product_id = '6ac7ed40fea4d4e68e0a0f6a'

# 1. Update product price in Printify
update_url = f'https://api.printify.com/v1/shops/{shop_id}/products/{product_id}.json'
update_payload = {
    "variants": [
        {
            "id": 44519,
            "price": 2999,
            "is_enabled": True
        }
    ]
}

req = urllib.request.Request(
    update_url,
    data=json.dumps(update_payload).encode('utf-8'),
    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
    method='PUT'
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    print("Tumbler updated in Printify:")
    for v in res.get('variants', []):
        print(f"  Variant {v['id']}: price = ${v['price']/100:.2f}, enabled = {v['is_enabled']}")

# 2. Publish / Sync to Etsy
pub_url = f'https://api.printify.com/v1/shops/{shop_id}/products/{product_id}/publish.json'
pub_payload = {
    "title": False,
    "description": False,
    "images": False,
    "variants": True,
    "tags": False
}

pub_req = urllib.request.Request(
    pub_url,
    data=json.dumps(pub_payload).encode('utf-8'),
    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
    method='POST'
)

try:
    with urllib.request.urlopen(pub_req) as resp:
        print("Tumbler publish triggered successfully to Etsy!")
except urllib.error.HTTPError as e:
    print(f"Publish error {e.code}: {e.read().decode()}")
