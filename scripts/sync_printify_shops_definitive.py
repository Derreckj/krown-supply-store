import requests
import json
import base64
import os

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}

ETSY_SHOP_ID = 29252381
TIKTOK_SHOP_ID = 29241235

# 1. Upload vertical sleeve artwork to Printify
sleeve_path = "public/images/branding/masters/axiom-sleeve-vertical-artwork.png"
with open(sleeve_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

upload_payload = {
    "file_name": "axiom-sleeve-vertical-artwork.png",
    "contents": b64
}
print("Uploading vertical sleeve artwork to Printify...")
r_up = requests.post("https://api.printify.com/v1/uploads/images.json", headers=headers, json=upload_payload)
if r_up.status_code in [200, 201]:
    sleeve_upload_id = r_up.json().get('id')
    print(f"Uploaded sleeve artwork! Upload ID: {sleeve_upload_id}")
else:
    print(f"Failed to upload sleeve artwork: {r_up.status_code} - {r_up.text}")
    exit(1)

owl_upload_id = "6ac70061b193f868adb8a466" # axiom-owl-mascot.png
display_mat_upload_id = "6ac7007408e4cece8eaa2594" # axiom-owl-display.png

# Blueprint 49, Provider 99 Black variant IDs
# 25397: S, 25428: M, 25459: L, 25490: XL, 25521: 2XL, 25552: 3XL, 25583: 4XL, 25614: 5XL
crew_variant_ids = [25397, 25428, 25459, 25490, 25521, 25552, 25583, 25614]
crew_variants = []
for vid in crew_variant_ids:
    price = 4999 if vid in [25397, 25428, 25459, 25490] else 5499
    crew_variants.append({
        "id": vid,
        "price": price,
        "is_enabled": True
    })

crew_payload = {
    "title": "Axiom Allegiance Official Crewneck Sweatshirt - Vertical Sleeve Edition",
    "description": (
        "Official Axiom Allegiance tournament crewneck sweatshirt in Obsidian Black. "
        "Cut on the premium Gildan 18000 Heavy Blend fleece (8.0 oz/yd²) with ribbed collar, cuffs, and waistband. "
        "Features high-density print of the official Axiom Owl mascot centered on the chest, paired with bold "
        "vertical 'Aχισм Aℓℓєgιαηcє' stylized sleeve lettering in signature electric toxic lime and royal purple. "
        "Manufactured and fulfilled with precision print on demand."
    ),
    "tags": ["Axiom Allegiance", "Crewneck", "Sweatshirt", "Esports", "Gaming Apparel", "Streetwear", "Gildan 18000"],
    "blueprint_id": 49,
    "print_provider_id": 99,
    "variants": crew_variants,
    "print_areas": [
        {
            "variant_ids": crew_variant_ids,
            "placeholders": [
                {
                    "position": "front",
                    "images": [
                        {
                            "id": owl_upload_id,
                            "x": 0.5,
                            "y": 0.45,
                            "scale": 0.70,
                            "angle": 0
                        }
                    ]
                },
                {
                    "position": "right_sleeve",
                    "images": [
                        {
                            "id": sleeve_upload_id,
                            "x": 0.5,
                            "y": 0.50,
                            "scale": 0.90,
                            "angle": 0
                        }
                    ]
                }
            ]
        }
    ]
}

# Create on both shops
created_crewnecks = {}
for shop_id, sname in [(TIKTOK_SHOP_ID, "TikTok"), (ETSY_SHOP_ID, "Etsy")]:
    print(f"\nCreating Axiom Crewneck on {sname} shop (ID: {shop_id})...")
    r_c = requests.post(f"https://api.printify.com/v1/shops/{shop_id}/products.json", headers=headers, json=crew_payload)
    if r_c.status_code in [200, 201]:
        prod_data = r_c.json()
        pid = prod_data.get('id')
        created_crewnecks[shop_id] = pid
        print(f"Successfully created crewneck on {sname}! Product ID: {pid}")
        # Publish
        pub_res = requests.post(
            f"https://api.printify.com/v1/shops/{shop_id}/products/{pid}/publish.json",
            headers=headers,
            json={"title": True, "description": True, "images": True, "variants": True, "tags": True}
        )
        print(f"Published crewneck on {sname}: {pub_res.status_code}")
    else:
        print(f"Failed to create on {sname}: {r_c.status_code} - {r_c.text}")

print("\nCrewneck creation summary:", created_crewnecks)
