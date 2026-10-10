import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

all_blueprints = get('https://api.printify.com/v1/catalog/blueprints.json')
print(f"Total blueprints returned: {len(all_blueprints)}")

terms = ["richardson", "hoodie", "jersey", "beanie", "hat", "cap"]

matches = {term: [] for term in terms}

for bp in all_blueprints:
    title = bp.get('title', '').lower()
    brand = bp.get('brand', '').lower()
    model = bp.get('model', '').lower()
    full_str = f"{title} {brand} {model}"
    for term in terms:
        if term in full_str:
            matches[term].append(bp)

for term, bps in matches.items():
    print(f"\n=== MATCHES FOR '{term}' ({len(bps)}) ===")
    for bp in bps[:10]:
        print(f"  ID: {bp['id']} | Title: {bp['title']} | Brand: {bp.get('brand')} | Model: {bp.get('model')}")
