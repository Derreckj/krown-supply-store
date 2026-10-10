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

TIKTOK_SHOP_ID = 29241235

def put_json(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='PUT'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def post_json(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def publish(prod_id):
    pub_url = f'https://api.printify.com/v1/shops/{TIKTOK_SHOP_ID}/products/{prod_id}/publish.json'
    post_json(pub_url, {
        "title": True,
        "description": True,
        "images": True,
        "variants": True,
        "tags": True
    })

def main():
    print("Aligning Comfort Colors Tee on TikTok...")
    tee_id = '6ac700d4e586b62fb50465b4'
    # Fetch full tee from TikTok shop
    req = urllib.request.Request(f'https://api.printify.com/v1/shops/{TIKTOK_SHOP_ID}/products/{tee_id}.json', headers=headers)
    with urllib.request.urlopen(req) as resp:
        t_data = json.loads(resp.read().decode())

    target_variants = {
        73196: (3400, True),  # S Black
        73200: (3400, True),  # M Black
        73204: (3400, True),  # L Black
        73208: (3400, True),  # XL Black
        73212: (3600, True),  # 2XL Black
        79046: (3400, True),  # S Pepper
        79047: (3400, True),  # M Pepper
        79048: (3400, True),  # L Pepper
        79049: (3400, True),  # XL Pepper
        79050: (3600, True),  # 2XL Pepper
    }

    updated_variants = []
    for v in t_data.get('variants', []):
        vid = v['id']
        if vid in target_variants:
            price, enabled = target_variants[vid]
            updated_variants.append({
                'id': vid,
                'price': price,
                'is_enabled': enabled,
                'is_default': (vid == 73204) # L Black
            })
        else:
            updated_variants.append({
                'id': vid,
                'price': v.get('price', 3400),
                'is_enabled': False
            })

    put_json(f'https://api.printify.com/v1/shops/{TIKTOK_SHOP_ID}/products/{tee_id}.json', {
        'title': 'KrowN "Wear The Krown" Comfort Colors 1717 Vintage Heavy Tee',
        'variants': updated_variants
    })
    print("  ✓ Comfort Colors Tee variants updated to 10 active ($34-$36)!")
    publish(tee_id)

    print("\nAligning Tumbler on TikTok...")
    tumbler_id = '6ac700d2e586b62fb50465b2'
    put_json(f'https://api.printify.com/v1/shops/{TIKTOK_SHOP_ID}/products/{tumbler_id}.json', {
        'title': '20oz Vacuum Insulated Jobsite Tumbler - Matte Black Stainless Steel Coffee Travel Mug',
        'variants': [{'id': 44519, 'price': 2999, 'is_enabled': True, 'is_default': True}]
    })
    print("  ✓ Tumbler price updated to $29.99 matching Etsy!")
    publish(tumbler_id)

    print("\nAlignment complete!")

if __name__ == '__main__':
    main()
