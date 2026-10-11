import requests
import json

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}

display_mat_upload_id = "6ac7007408e4cece8eaa2594" # axiom-owl-display.png

# 1. Update Desk Mats on both shops
mousepad_targets = [
    (29241235, '6ac700b20a223533b30704f4', 'TikTok Mousepad'),
    (29252381, '6ac7ed486443c9f27801af1b', 'Etsy Mousepad')
]

for shop_id, prod_id, label in mousepad_targets:
    print(f"\nUpdating {label} ({prod_id}) with Axiom Owl Display artwork...")
    # Fetch current product
    r_get = requests.get(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json", headers=headers)
    if r_get.status_code != 200:
        print(f"Failed to fetch {label}: {r_get.status_code}")
        continue
    pdata = r_get.json()
    
    # Update print areas image
    print_areas = pdata.get('print_areas', [])
    for pa in print_areas:
        for ph in pa.get('placeholders', []):
            ph['images'] = [
                {
                    "id": display_mat_upload_id,
                    "x": 0.5,
                    "y": 0.5,
                    "scale": 1.0,
                    "angle": 0
                }
            ]
            
    # PUT update
    update_payload = {
        "title": pdata.get('title'),
        "description": (
            "Axiom Allegiance Official Panoramic Gaming Desk Mat featuring the definitive Axiom Owl Display artwork. "
            "High-density micro-woven cloth surface, anti-slip natural rubber base, and precision black edge stitching. "
            "Optimized for low and high DPI mouse tracking."
        ),
        "tags": ["Axiom Allegiance", "Gaming Desk Mat", "Esports", "Mouse Pad", "Extended Desk Pad"],
        "variants": pdata.get('variants', []),
        "print_areas": print_areas
    }
    
    r_put = requests.put(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json", headers=headers, json=update_payload)
    if r_put.status_code == 200:
        print(f"Successfully updated {label} print area to Axiom Owl Display!")
        # Publish
        r_pub = requests.post(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}/publish.json", headers=headers, json={"title": True, "description": True, "images": True, "variants": True, "tags": True})
        print(f"Published {label}: {r_pub.status_code}")
    else:
        print(f"Failed to update {label}: {r_put.status_code} - {r_put.text}")

# 2. Remove / Unpublish deprecated products from both shops
deprecated_items = [
    # Beanies
    (29241235, '6ac8f2d10a804851a8009ad3', 'TikTok Cuffed Beanie'),
    (29252381, '6ac80e07cafb2cd4c60b7c96', 'Etsy Cuffed Beanie'),
    # 20oz Jobsite Tumblers
    (29241235, '6ac700d2e586b62fb50465b2', 'TikTok 20oz Tumbler'),
    (29252381, '6ac7ed40fea4d4e68e0a0f6a', 'Etsy 20oz Tumbler'),
    # Axiom Vinyl Stickers
    (29241235, '6ac700cf826b7669c103bbda', 'TikTok Axiom Stickers'),
    (29252381, '6ac7ed46ad560d80d10eb55c', 'Etsy Axiom Stickers'),
]

print("\n--- Purging Deprecated Products from Printify Shops ---")
for shop_id, prod_id, label in deprecated_items:
    print(f"Removing {label} ({prod_id}) from shop {shop_id}...")
    # First unpublish
    try:
        requests.post(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}/unpublish.json", headers=headers, json={})
    except Exception as e:
        pass
    # Then delete from Printify catalog
    r_del = requests.delete(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json", headers=headers)
    print(f"Delete {label}: {r_del.status_code}")

print("\nCompleted Mousepad Update & Deprecated Product Purge!")
