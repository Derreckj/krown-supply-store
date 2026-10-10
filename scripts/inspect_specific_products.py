import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

for pid in ['6ac7ed40fea4d4e68e0a0f6a', '6ac7ed0b9bfbeab23800dcdf']:
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{pid}.json'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        p = json.loads(resp.read().decode())
        print('====================================')
        print('PRODUCT ID:', p['id'], p['title'])
        print('Blueprint:', p['blueprint_id'], 'Provider:', p['print_provider_id'])
        print('Print areas count:', len(p.get('print_areas', [])))
        for pa in p.get('print_areas', []):
            print('  Area:', pa.get('placeholders'))
        variants = p.get('variants', [])
        print('Variants count:', len(variants))
        for v in variants[:5]:
            print('  Variant:', v['id'], v['title'], v['price'], 'enabled:', v['is_enabled'])
