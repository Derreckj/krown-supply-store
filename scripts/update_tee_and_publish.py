import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']
product_id = '6ac7ed0b9bfbeab23800dcdf'

# Fetch existing product
get_url = f'https://api.printify.com/v1/shops/{shop_id}/products/{product_id}.json'
req = urllib.request.Request(get_url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
with urllib.request.urlopen(req) as resp:
    prod = json.loads(resp.read().decode())

# Gold definitive logo ID
logo_id = '6ac80c13cb84a6be727da69e'

# Configure variants: Enable Black and Pepper S through 2XL at $34.00 (3400 cents)
enabled_ids = {
    # Pepper
    79046: 3400, # S
    79047: 3400, # M
    79048: 3400, # L
    79049: 3400, # XL
    79050: 3600, # 2XL ($36.00)
    # Black
    73196: 3400, # S
    73200: 3400, # M
    73204: 3400, # L
    73208: 3400, # XL
    73212: 3600, # 2XL ($36.00)
}

default_variant_id = 79048 # L / Pepper

updated_variants = []
for v in prod['variants']:
    vid = v['id']
    if vid in enabled_ids:
        updated_variants.append({
            'id': vid,
            'price': enabled_ids[vid],
            'is_enabled': True,
            'is_default': (vid == default_variant_id)
        })
    else:
        updated_variants.append({
            'id': vid,
            'price': v.get('price', 3400),
            'is_enabled': False,
            'is_default': False
        })

# Configure print areas
print_areas = [
    {
        "variant_ids": [v['id'] for v in updated_variants],
        "placeholders": [
            {
                "position": "front",
                "images": [
                    {
                        "id": logo_id,
                        "x": 0.5,
                        "y": 0.45,
                        "scale": 0.70,
                        "angle": 0
                    }
                ]
            }
        ]
    }
]

payload = {
    "title": 'KrowN "Wear The Krown" Comfort Colors 1717 Vintage Heavy Tee',
    "description": '<p>Authentic Comfort Colors 1717 garment-dyed 100% ring-spun cotton tee with vintage broken-in wash. Relaxed boxy streetwear fit featuring the official gold 3D geometric KrowN brand crest. Built to Reign.</p>',
    "variants": updated_variants,
    "print_areas": print_areas
}

update_url = f'https://api.printify.com/v1/shops/{shop_id}/products/{product_id}.json'
update_req = urllib.request.Request(
    update_url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
    method='PUT'
)

try:
    with urllib.request.urlopen(update_req) as resp:
        res = json.loads(resp.read().decode())
        print("Tee updated successfully in Printify!")
        print("Enabled variants:")
        for v in res.get('variants', []):
            if v.get('is_enabled'):
                print(f"  {v['id']}: {v['title']} - ${v['price']/100:.2f} (default: {v.get('is_default')})")
        print("Print area image:", res.get('print_areas', [])[0]['placeholders'][0]['images'])
        
        # Trigger publish to Etsy
        pub_url = f'https://api.printify.com/v1/shops/{shop_id}/products/{product_id}/publish.json'
        pub_payload = {
            "title": True,
            "description": True,
            "images": True,
            "variants": True,
            "tags": True
        }
        pub_req = urllib.request.Request(
            pub_url,
            data=json.dumps(pub_payload).encode('utf-8'),
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
            method='POST'
        )
        with urllib.request.urlopen(pub_req) as p_resp:
            print("Tee publish triggered successfully to Etsy!")
except urllib.error.HTTPError as e:
    print(f"Update error {e.code}: {e.read().decode()}")

