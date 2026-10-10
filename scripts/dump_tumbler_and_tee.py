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

print("=== TUMBLER 6ac7ed40fea4d4e68e0a0f6a ===")
tumbler = get(f'https://api.printify.com/v1/shops/{shop_id}/products/6ac7ed40fea4d4e68e0a0f6a.json')
print(json.dumps({
    'id': tumbler['id'],
    'title': tumbler['title'],
    'variants': tumbler['variants'],
    'images': [img['src'] for img in tumbler.get('images', [])[:3]],
    'external': tumbler.get('external')
}, indent=2))

print("\n=== TEE 6ac7ed0b9bfbeab23800dcdf ===")
tee = get(f'https://api.printify.com/v1/shops/{shop_id}/products/6ac7ed0b9bfbeab23800dcdf.json')
print(json.dumps({
    'id': tee['id'],
    'title': tee['title'],
    'variants': [{'id': v['id'], 'title': v['title'], 'price': v['price'], 'is_enabled': v['is_enabled'], 'is_default': v.get('is_default')} for v in tee['variants']],
    'print_areas': tee['print_areas'],
    'images': [img['src'] for img in tee.get('images', [])[:3]],
    'external': tee.get('external')
}, indent=2))
