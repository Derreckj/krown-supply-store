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

# Candidates to inspect:
# 1. Richardson 112: 1743
# 2. Hoodie: 2001 (Lane Seven LS19001 Heavyweight), 439 (Lane Seven LS14001)
# 3. Jersey: 1332 (Men's Sports Jersey AOP), 593 (Baseball Jersey AOP)
# 4. Beanie: 1922 (Atlantis Ribbed Knit Beanie), 1691 (Yupoong 1501KC Cuffed Beanie)

check_list = [
    ("Richardson 112", 1743),
    ("Heavyweight Hoodie (Lane Seven LS19001)", 2001),
    ("Three-Panel Hoodie (Lane Seven LS14001)", 439),
    ("Men's Sports Jersey (AOP)", 1332),
    ("Ribbed Knit Beanie (Atlantis)", 1922),
    ("Classic Cuffed Beanie (Yupoong 1501KC)", 1691)
]

for name, bp_id in check_list:
    print(f"\n==========================================")
    print(f"PRODUCT: {name} (BP {bp_id})")
    providers = get(f'https://api.printify.com/v1/catalog/blueprints/{bp_id}/print_providers.json')
    if not providers:
        continue
    for p in providers:
        print(f"Provider: ID={p['id']} - {p['title']}")
        # Get variants for first provider
    first_prov = providers[0]['id']
    v_data = get(f'https://api.printify.com/v1/catalog/blueprints/{bp_id}/print_providers/{first_prov}/variants.json')
    if v_data:
        variants = v_data.get('variants', [])
        print(f"Variants count for provider {first_prov}: {len(variants)}")
        for v in variants[:4]:
            print(f"  vID: {v['id']} | title: {v['title']} | options: {v.get('options')}")
        # Check print areas
        pa = v_data.get('print_areas') or v_data.get('placeholders')
        print(f"  print_areas/placeholders info: {v_data.get('placeholders_keys', []) or list(v_data.keys())}")
