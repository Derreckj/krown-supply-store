import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code} for {url}: {e.read().decode()[:300]}")
        return None

specs = [
    ("Richardson 112", 1743, 99),
    ("Heavyweight Hoodie", 2001, 99),
    ("Sports Jersey AOP", 1332, 99),
    ("Ribbed Beanie", 1922, 99),
    ("Cuffed Beanie", 1691, 99),
]

for name, bp_id, prov_id in specs:
    print(f"\n==========================================")
    print(f"SPEC FOR {name} (BP {bp_id}, Prov {prov_id})")
    data = get(f'https://api.printify.com/v1/catalog/blueprints/{bp_id}/print_providers/{prov_id}/variants.json')
    if data:
        # Check print areas or placeholders if available in blueprint or variant response
        # In printify, placeholders can also be found by getting catalog/blueprints/{id}/print_providers/{id}.json or creating a dummy
        bp_prov = get(f'https://api.printify.com/v1/catalog/blueprints/{bp_id}/print_providers/{prov_id}.json')
        print("BP Prov info:", bp_prov)
