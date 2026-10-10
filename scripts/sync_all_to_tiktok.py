import sys
import io
import urllib.request
import json
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'KrowN/1.0'
}

ETSY_SHOP_ID = 29252381
TIKTOK_SHOP_ID = 29241235

def get_products(shop_id):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products.json'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode()).get('data', [])

def get_product(shop_id, prod_id):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def create_product(shop_id, payload):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products.json'
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def publish_product(shop_id, prod_id):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}/publish.json'
    pub_payload = {
        "title": True,
        "description": True,
        "images": True,
        "variants": True,
        "tags": True
    }
    data = json.dumps(pub_payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Publish notice ({prod_id}): {e.code} - {e.read().decode()[:150]}")
        return None

def main():
    print("Fetching products from Etsy Shop...")
    etsy_prods = get_products(ETSY_SHOP_ID)
    print(f"Found {len(etsy_prods)} products in Etsy shop.")

    print("Fetching products from TikTok Shop...")
    tiktok_prods = get_products(TIKTOK_SHOP_ID)
    print(f"Found {len(tiktok_prods)} products in TikTok shop.")

    tiktok_blueprints = {p.get('blueprint_id'): p['title'] for p in tiktok_prods}

    # Clone missing products to TikTok Shop
    for p in etsy_prods:
        bp_id = p.get('blueprint_id')
        if bp_id in tiktok_blueprints:
            print(f"✓ Already present in TikTok Shop: '{p['title']}'")
            continue
        
        print(f"\n--> Syncing missing product to TikTok Shop: '{p['title']}'...")
        full_p = get_product(ETSY_SHOP_ID, p['id'])

        variants = []
        for v in full_p.get('variants', []):
            variants.append({
                'id': v['id'],
                'price': v['price'],
                'is_enabled': v.get('is_enabled', True),
                'is_default': v.get('is_default', False)
            })

        payload = {
            'title': full_p['title'],
            'description': full_p['description'],
            'tags': full_p.get('tags', []),
            'blueprint_id': full_p['blueprint_id'],
            'print_provider_id': full_p['print_provider_id'],
            'variants': variants,
            'print_areas': full_p.get('print_areas', [])
        }

        try:
            new_p = create_product(TIKTOK_SHOP_ID, payload)
            new_id = new_p.get('id')
            print(f"  ✓ Created in TikTok Shop! ID: {new_id}")
            time.sleep(2)
            publish_product(TIKTOK_SHOP_ID, new_id)
            print(f"  ✓ Initiated publish for {new_id}")
        except urllib.error.HTTPError as e:
            print(f"  ✗ Error creating product: {e.code} - {e.read().decode()}")

    print("\n--- Current TikTok Shop Inventory ---")
    current_tiktok = get_products(TIKTOK_SHOP_ID)
    for p in current_tiktok:
        print(f"ID: {p['id']} | Title: {p['title']}")

if __name__ == '__main__':
    main()
