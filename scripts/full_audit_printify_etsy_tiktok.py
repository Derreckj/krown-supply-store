import sys
import io
import urllib.request
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
headers = {'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'}

def api_get(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def audit_shop(shop_id, channel_name):
    print(f"\n{'='*70}")
    print(f"AUDITING: {channel_name.upper()} (Shop ID: {shop_id})")
    print(f"{'='*70}")
    
    url = f"https://api.printify.com/v1/shops/{shop_id}/products.json"
    prods_data = api_get(url)
    products = prods_data.get('data', [])
    print(f"Total Products in Catalog: {len(products)}")
    
    for idx, p in enumerate(products, 1):
        pid = p['id']
        title = p['title']
        bp = p.get('blueprint_id')
        prov = p.get('print_provider_id')
        visible = p.get('visible')
        is_locked = p.get('is_locked')
        external = p.get('external', {})
        variants = p.get('variants', [])
        enabled_variants = [v for v in variants if v.get('is_enabled', True)]
        prices = [v.get('price', 0) / 100 for v in enabled_variants if v.get('price')]
        price_range = f"${min(prices):.2f} - ${max(prices):.2f}" if prices else "N/A"
        images = p.get('images', [])

        print(f"\n[{idx}] {title}")
        print(f"    - ID: {pid}")
        print(f"    - Blueprint: {bp} | Provider: {prov}")
        print(f"    - Visibility: {'Active/Visible' if visible else 'Hidden/Draft'} | Locked: {is_locked}")
        print(f"    - Variants: {len(enabled_variants)} active / {len(variants)} total | Price Range: {price_range}")
        print(f"    - Mockup Images: {len(images)} loaded")
        if external:
            ext_id = external.get('id')
            ext_handle = external.get('handle')
            shipping_template = external.get('shipping_template_id')
            print(f"    - External Sync: ID={ext_id}, Handle={ext_handle}, ShippingTemplate={shipping_template}")
        else:
            print("    - External Sync: Native Printify managed")

def main():
    shops = api_get("https://api.printify.com/v1/shops.json")
    print("=== CONNECTED CHANNELS IN PRINTIFY ===")
    for s in shops:
        print(f"Shop: '{s['title']}' | ID: {s['id']} | Channel: {s.get('sales_channel')}")

    for s in shops:
        channel = s.get('sales_channel', 'unknown')
        if channel in ['tiktok', 'etsy']:
            audit_shop(s['id'], f"{channel.title()} Store ({s['title']})")

if __name__ == '__main__':
    main()
