import os
import sys
import io
import urllib.request
import json
import base64
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
shop_id = env['PRINTIFY_SHOP_ID']

def get_product(pid):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{pid}.json'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def update_product(pid, payload):
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{pid}.json'
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
        method='PUT'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def publish_product(pid, sync_fields=None):
    if sync_fields is None:
        sync_fields = {"title": True, "description": False, "images": True, "variants": True, "tags": True}
    url = f'https://api.printify.com/v1/shops/{shop_id}/products/{pid}/publish.json'
    req = urllib.request.Request(
        url,
        data=json.dumps(sync_fields).encode('utf-8'),
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'},
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def upload_image(filepath, filename):
    with open(filepath, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    payload = json.dumps({'file_name': filename, 'contents': b64}).encode('utf-8')
    req = urllib.request.Request(
        'https://api.printify.com/v1/uploads/images.json',
        data=payload,
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"Uploaded {filename} -> Image ID: {res.get('id')}")
        return res.get('id')

print("=== STEP 1: UPLOAD HOODIE BACK ARTWORK TO PRINTIFY ===")
back_path = "public/images/products/krown-heavyweight-hoodie-back-krown.jpg"
back_img_id = upload_image(back_path, "krown-heavyweight-hoodie-back-artwork.jpg")

print("\n=== STEP 2: UPDATE HOODIE (6ac80dff9f3e89dde70da38d) WITH FRONT & BACK ARTWORK ===")
hoodie_id = "6ac80dff9f3e89dde70da38d"
h_prod = get_product(hoodie_id)

# Enable both Black and Heather Grey variants
# Heather Grey IDs: S: 122975, M: 122968, L: 122961, XL: 122982, 2XL: 122947
enabled_vids = {
    # Black
    122974: 6800, # S
    122967: 6800, # M
    122960: 6800, # L (default)
    122981: 6800, # XL
    122946: 7200, # 2XL
    # Heather Grey
    122975: 6800, # S
    122968: 6800, # M
    122961: 6800, # L
    122982: 6800, # XL
    122947: 7200, # 2XL
}

h_variants = []
for v in h_prod['variants']:
    vid = v['id']
    if vid in enabled_vids:
        h_variants.append({
            "id": vid,
            "price": enabled_vids[vid],
            "is_enabled": True,
            "is_default": (vid == 122960)
        })
    else:
        h_variants.append({
            "id": vid,
            "price": v.get('price', 6800),
            "is_enabled": False,
            "is_default": False
        })

front_logo_id = "6ac80c13cb84a6be727da69e"

h_print_areas = [
    {
        "variant_ids": [v['id'] for v in h_variants],
        "placeholders": [
            {
                "position": "front",
                "images": [
                    {
                        "id": front_logo_id,
                        "x": 0.5,
                        "y": 0.45,
                        "scale": 0.70,
                        "angle": 0
                    }
                ]
            },
            {
                "position": "back",
                "images": [
                    {
                        "id": back_img_id,
                        "x": 0.5,
                        "y": 0.50,
                        "scale": 0.85,
                        "angle": 0
                    }
                ]
            }
        ]
    }
]

h_payload = {
    "title": 'KrowN Heavyweight Streetwear Hoodie (480 GSM) - Vintage French Terry Pullover',
    "description": h_prod['description'],
    "variants": h_variants,
    "print_areas": h_print_areas
}

try:
    update_product(hoodie_id, h_payload)
    print("  ✓ Hoodie updated with Front & Back print areas and Black + Heather Grey colors!")
    time.sleep(2)
    publish_product(hoodie_id, {"title": True, "description": False, "images": True, "variants": True, "tags": True})
    print("  ✓ Hoodie re-published to Etsy with multi-angle mockups!")
except urllib.error.HTTPError as e:
    print(f"  ✗ Hoodie error {e.code}: {e.read().decode()[:200]}")

print("\n=== STEP 3: OPTIMIZE PRODUCT TITLES FOR ETSY SEARCH ALGORITHM ===")
# Title optimizations for the flagged listings
title_updates = [
    ('6ac7ed40fea4d4e68e0a0f6a', '20oz Vacuum Insulated Jobsite Tumbler - Matte Black Stainless Steel Coffee Travel Mug'),
    ('6ac7ed486443c9f27801af1b', 'Axiom Owl Panoramic Gaming Desk Mat (32x16) - Extended Non-Slip Esports Mouse Pad'),
    ('6ac7ed46ad560d80d10eb55c', 'Axiom Owl Holographic Kiss-Cut Vinyl Stickers - Esports Gaming Decals'),
    ('6ac7ed44fea4d4e68e0a0f80', 'Hardhat Sticker Pack (5-Pack) - Weatherproof Vinyl Tool Box Decals')
]

for pid, new_title in title_updates:
    try:
        update_product(pid, {"title": new_title})
        print(f"  ✓ Updated title for {pid}: '{new_title}'")
        time.sleep(1)
        publish_product(pid, {"title": True, "description": False, "images": False, "variants": False, "tags": False})
        print(f"    ✓ Synced title to Etsy!")
    except urllib.error.HTTPError as e:
        print(f"  ✗ Title update error for {pid} {e.code}: {e.read().decode()[:150]}")

print("\n=== ETSY TITLE & MOCKUP SYNC COMPLETED ===")
