import urllib.request
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

# Try creating Richardson 112
variants_ids = [118722, 118723, 118724, 118726, 118727]
variant_payload = [{"id": vid, "price": 3499, "is_enabled": True} for vid in variants_ids]

# Using KC Emblem or Definitive Logo
img_id = '6ac7007d077755cc444de3b2' # Krown-Construction-Emblem.png

payload = {
    "title": "KrowN Richardson 112 Leather Patch Trucker Snapback",
    "description": "<p>Official Richardson 112 Classic Trucker Cap featuring our custom laser-engraved KrowN brand patch. Mid-profile structured design with pre-curved contrast stitched visor and breathable mesh backing. Built to Reign.</p>",
    "blueprint_id": 1743,
    "print_provider_id": 99,
    "variants": variant_payload,
    "print_areas": [
        {
            "variant_ids": variants_ids,
            "placeholders": [
                {
                    "position": "front",
                    "images": [
                        {
                            "id": img_id,
                            "x": 0.5,
                            "y": 0.5,
                            "scale": 0.8,
                            "angle": 0
                        }
                    ]
                }
            ]
        }
    ]
}

req = urllib.request.Request(
    f"https://api.printify.com/v1/shops/{shop_id}/products.json",
    data=json.dumps(payload).encode('utf-8'),
    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print("Success! Created Richardson 112 Product ID:", res.get('id'))
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
