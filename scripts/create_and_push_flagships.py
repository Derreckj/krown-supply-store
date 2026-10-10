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
shop_id = env['PRINTIFY_SHOP_ID']

def post_json(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def publish_product(pid):
    pub_url = f'https://api.printify.com/v1/shops/{shop_id}/products/{pid}/publish.json'
    pub_payload = {
        "title": True,
        "description": True,
        "images": True,
        "variants": True,
        "tags": True
    }
    try:
        post_json(pub_url, pub_payload)
        print(f"  ✓ Published {pid} to Etsy store!")
    except urllib.error.HTTPError as e:
        print(f"  ! Publish note for {pid}: {e.code} - {e.read().decode()[:150]}")

# 1. Publish Richardson 112 already created:
r112_id = '6ac80dc2f4d488e1be0b0902'
print(f"Publishing Richardson 112 ({r112_id})...")
publish_product(r112_id)

# 2. Create 480 GSM Heavyweight Streetwear Hoodie (Lane Seven LS19001, BP 2001, Prov 99)
print("\nCreating 480 GSM Heavyweight Streetwear Hoodie...")
hoodie_variants = [
    {"id": 122974, "price": 6800, "is_enabled": True}, # S
    {"id": 122967, "price": 6800, "is_enabled": True}, # M
    {"id": 122960, "price": 6800, "is_enabled": True, "is_default": True}, # L
    {"id": 122981, "price": 6800, "is_enabled": True}, # XL
    {"id": 122946, "price": 7200, "is_enabled": True}, # 2XL
]
hoodie_payload = {
    "title": 'KrowN "Built To Reign" Heavyweight Streetwear Hoodie',
    "description": '<p>Engineered for supreme warmth and clean streetwear drape. Crafted from ultra-heavyweight 3-end fleece with double-needle construction, matching flat drawstrings, and reinforced pouch pocket. Features the official gold 3D geometric KrowN brand crest. Built to Reign.</p>',
    "blueprint_id": 2001,
    "print_provider_id": 99,
    "variants": hoodie_variants,
    "print_areas": [
        {
            "variant_ids": [v['id'] for v in hoodie_variants],
            "placeholders": [
                {
                    "position": "front",
                    "images": [
                        {
                            "id": "6ac80c13cb84a6be727da69e", # krown-definitive-logo.png
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
}
try:
    h_res = post_json(f'https://api.printify.com/v1/shops/{shop_id}/products.json', hoodie_payload)
    h_id = h_res.get('id')
    print(f"  ✓ Hoodie created! Product ID: {h_id}")
    time.sleep(2)
    publish_product(h_id)
except urllib.error.HTTPError as e:
    print(f"  ✗ Hoodie creation error {e.code}: {e.read().decode()}")

# 3. Create AXA Cut-and-Sew Pro Esports Jersey (BP 1332, Prov 99)
print("\nCreating AXA Pro Esports Jersey...")
jersey_variants = [
    {"id": 101479, "price": 5500, "is_enabled": True}, # S
    {"id": 101480, "price": 5500, "is_enabled": True}, # M
    {"id": 101481, "price": 5500, "is_enabled": True, "is_default": True}, # L
    {"id": 101482, "price": 5500, "is_enabled": True}, # XL
    {"id": 101483, "price": 5800, "is_enabled": True}, # 2XL
]
jersey_payload = {
    "title": 'Axiom Allegiance AXA Cut-and-Sew Pro Esports Jersey',
    "description": '<p>Official tournament-grade athletic jersey for Axiom Allegiance. Moisture-wicking performance polyester mesh, vibrant all-over sublimation detailing with the high-definition Axiom Owl mascot crest. Precision engineered for elite competitive play.</p>',
    "blueprint_id": 1332,
    "print_provider_id": 99,
    "variants": jersey_variants,
    "print_areas": [
        {
            "variant_ids": [v['id'] for v in jersey_variants],
            "placeholders": [
                {
                    "position": "front",
                    "images": [
                        {
                            "id": "6ac70061b193f868adb8a466", # axiom-owl-mascot.png
                            "x": 0.5,
                            "y": 0.45,
                            "scale": 0.80,
                            "angle": 0
                        }
                    ]
                }
            ]
        }
    ]
}
try:
    j_res = post_json(f'https://api.printify.com/v1/shops/{shop_id}/products.json', jersey_payload)
    j_id = j_res.get('id')
    print(f"  ✓ Jersey created! Product ID: {j_id}")
    time.sleep(2)
    publish_product(j_id)
except urllib.error.HTTPError as e:
    print(f"  ✗ Jersey creation error {e.code}: {e.read().decode()}")

# 4. Create Heavy Ribbed Cuffed Beanie (BP 1922, Prov 99)
print("\nCreating Heavy Ribbed Cuffed Beanie...")
beanie_variants = [
    {"id": 119474, "price": 2800, "is_enabled": True, "is_default": True}, # Black
    {"id": 119476, "price": 2800, "is_enabled": True}, # Light Grey Melange
    {"id": 119478, "price": 2800, "is_enabled": True}, # Navy
    {"id": 119479, "price": 2800, "is_enabled": True}, # Olive
]
beanie_payload = {
    "title": 'KrowN Construction Heavy Ribbed Cuffed Beanie',
    "description": '<p>Heavyweight ribbed knit cuffed beanie engineered for sub-zero jobsite shifts and clean street style. Thermal insulation, snug shape retention, and embroidered KrowN Construction branding. Built to Reign.</p>',
    "blueprint_id": 1922,
    "print_provider_id": 99,
    "variants": beanie_variants,
    "print_areas": [
        {
            "variant_ids": [v['id'] for v in beanie_variants],
            "placeholders": [
                {
                    "position": "front",
                    "images": [
                        {
                            "id": "6ac7007d077755cc444de3b2", # Krown-Construction-Emblem.png
                            "x": 0.5,
                            "y": 0.5,
                            "scale": 0.75,
                            "angle": 0
                        }
                    ]
                }
            ]
        }
    ]
}
try:
    b_res = post_json(f'https://api.printify.com/v1/shops/{shop_id}/products.json', beanie_payload)
    b_id = b_res.get('id')
    print(f"  ✓ Beanie created! Product ID: {b_id}")
    time.sleep(2)
    publish_product(b_id)
except urllib.error.HTTPError as e:
    print(f"  ✗ Beanie creation error {e.code}: {e.read().decode()}")

print("\n=== FLAGSHIP CREATION & SYNC COMPLETE ===")
