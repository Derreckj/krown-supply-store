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
        print(f"HTTPError {e.code} for {url}: {e.read().decode()}")
        return None

# Check blueprints
blueprints = [112, 1035, 872, 342]
for bp_id in blueprints:
    bp = get(f'https://api.printify.com/v1/catalog/blueprints/{bp_id}.json')
    if bp:
        print(f"\n================ Blueprint {bp_id}: {bp.get('title')} ================")
        print(f"Brand: {bp.get('brand')}, Model: {bp.get('model')}")
        providers = get(f'https://api.printify.com/v1/catalog/blueprints/{bp_id}/print_providers.json')
        print(f"Available Providers: {len(providers) if providers else 0}")
        if providers:
            for prov in providers:
                print(f"  Provider ID: {prov['id']} - {prov.get('title')}")
