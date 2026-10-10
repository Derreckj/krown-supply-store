import os
import json
import urllib.request

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

headers = {'Authorization': f'Bearer {env["PRINTIFY_API_KEY"]}', 'User-Agent': 'KrowN/1.0'}

def audit_shop(name, shop_id):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products.json'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        products = data.get('data', [])
        print(f"=== {name} (Shop ID: {shop_id}) ===")
        print(f"Total Products: {len(products)}")
        for p in products:
            img_count = len(p.get('images', []))
            enabled_vars = [v for v in p.get('variants', []) if v.get('is_enabled', True)]
            var_count = len(enabled_vars)
            prices = [v.get('price', 0) for v in enabled_vars]
            min_price = (min(prices) / 100) if prices else 0.0
            max_price = (max(prices) / 100) if prices else 0.0
            price_str = f"${min_price:.2f}" if min_price == max_price else f"${min_price:.2f} - ${max_price:.2f}"
            print(f"- [{p['id']}] {p['title'][:48]:<48} | {price_str:<16} | Vars: {var_count:2d} | Images: {img_count:2d}")
        print()

audit_shop('Etsy Shop', 29252381)
audit_shop('TikTok Shop', 29241235)
