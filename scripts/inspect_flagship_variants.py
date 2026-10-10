import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

print("=== HOODIE BP 2001, Provider 99 ===")
h_data = get('https://api.printify.com/v1/catalog/blueprints/2001/print_providers/99/variants.json')
for v in h_data.get('variants', []):
    if v.get('options', {}).get('color') == 'Black':
        print(f"  vID: {v['id']} | title: {v['title']} | options: {v.get('options')}")

print("\n=== JERSEY BP 1332, Provider 99 ===")
j_data = get('https://api.printify.com/v1/catalog/blueprints/1332/print_providers/99/variants.json')
for v in j_data.get('variants', []):
    print(f"  vID: {v['id']} | title: {v['title']} | options: {v.get('options')}")

print("\n=== BEANIE BP 1691 (Yupoong), Provider 99 ===")
b_data = get('https://api.printify.com/v1/catalog/blueprints/1691/print_providers/99/variants.json')
for v in b_data.get('variants', []):
    if v.get('options', {}).get('color') in ['Black', 'Dark Grey', 'Navy']:
        print(f"  vID: {v['id']} | title: {v['title']} | options: {v.get('options')}")

print("\n=== BEANIE BP 1922 (Atlantis Ribbed), Provider 99 ===")
b2_data = get('https://api.printify.com/v1/catalog/blueprints/1922/print_providers/99/variants.json')
for v in b2_data.get('variants', []):
    print(f"  vID: {v['id']} | title: {v['title']} | options: {v.get('options')}")
