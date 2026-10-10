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
        print(f"HTTPError {e.code} for {url}: {e.read().decode()[:200]}")
        return None

# Let's inspect blueprint 1743 (Richardson 112)
print("=== RICHARDSON 112 (Blueprint 1743) ===")
r112 = get('https://api.printify.com/v1/catalog/blueprints/1743.json')
if r112:
    print(r112.get('title'), r112.get('brand'), r112.get('model'))
    provs = get('https://api.printify.com/v1/catalog/blueprints/1743/print_providers.json')
    for p in provs:
        print(" Provider:", p['id'], p['title'])

# Let's inspect Beanies (1691, 1922, 1728)
print("\n=== BEANIES ===")
for b_id in [1691, 1922, 1728, 1689]:
    b = get(f'https://api.printify.com/v1/catalog/blueprints/{b_id}.json')
    if b:
        provs = get(f'https://api.printify.com/v1/catalog/blueprints/{b_id}/print_providers.json')
        print(f"Blueprint {b_id}: {b.get('title')} ({b.get('brand')} {b.get('model')}) - Providers: {[p['id'] for p in provs]}")

# Let's search all blueprints for heavyweight hoodie (Independent, Lane Seven, etc)
all_blueprints = get('https://api.printify.com/v1/catalog/blueprints.json')
print("\n=== HOODIES SEARCH ===")
for bp in all_blueprints:
    title = bp.get('title', '').lower()
    brand = bp.get('brand', '').lower()
    model = bp.get('model', '').lower()
    s = f"{title} {brand} {model}"
    if 'hoodie' in s and ('heavy' in s or 'lane seven' in s or 'independent' in s or 'fleece' in s or 'street' in s or 'oversized' in s or 'premium' in s):
        print(f"BP {bp['id']}: {bp['title']} | Brand: {bp.get('brand')} | Model: {bp.get('model')}")

print("\n=== AOP / JERSEY SEARCH ===")
for bp in all_blueprints:
    title = bp.get('title', '').lower()
    brand = bp.get('brand', '').lower()
    model = bp.get('model', '').lower()
    s = f"{title} {brand} {model}"
    if ('jersey' in s or 'esports' in s or 'athletic' in s) and ('aop' in s or 'cut' in s or 'sublimat' in s or 'all-over' in s or 'mesh' in s or 'sport' in s):
        print(f"BP {bp['id']}: {bp['title']} | Brand: {bp.get('brand')} | Model: {bp.get('model')}")
    elif bp.get('id') in [872, 1035, 342, 112]:
        print(f"FOUND EXACT ID BP {bp['id']}: {bp['title']}")
