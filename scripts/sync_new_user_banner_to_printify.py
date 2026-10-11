import os, json, requests

with open('.env.local', 'r') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'}

upload_id = "6acb7edaa4cd51f9161ae6c8" # User's exact Axiom Owl Banner

targets = [
    (29241235, '6ac700b20a223533b30704f4', 'TikTok / Main Store Mouse Pad'),
    (29252381, '6ac7ed486443c9f27801af1b', 'Etsy Mouse Pad')
]

for shop_id, prod_id, label in targets:
    print(f"\nProcessing {label} (Shop: {shop_id}, Product: {prod_id})...")
    r_get = requests.get(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json", headers=headers)
    if r_get.status_code != 200:
        print(f"Failed to fetch {label}: {r_get.status_code} {r_get.text}")
        continue
    pdata = r_get.json()
    
    print_areas = pdata.get('print_areas', [])
    for pa in print_areas:
        for ph in pa.get('placeholders', []):
            ph['images'] = [
                {
                    "id": upload_id,
                    "x": 0.5,
                    "y": 0.5,
                    "scale": 1.0,
                    "angle": 0
                }
            ]
            
    payload = {
        "title": "Axiom Owl Display Customizable Gaming Desk Mat (Esports Mouse Pad)",
        "description": (
            "Official Axiom Allegiance tournament gaming desk mat featuring the definitive Axiom Owl Display artwork. "
            "High-density micro-woven cloth surface engineered for pixel-precise optical sensor tracking and effortless mouse glide. "
            "Reinforced anti-fray precision lockstitched black perimeter and textured non-slip natural rubber base. "
            "Customizable with player gamertag, clan handle, and squad number."
        ),
        "tags": ["Axiom Allegiance", "Gaming Desk Mat", "Esports", "Mouse Pad", "Customizable Mouse Pad", "Extended Desk Mat"],
        "variants": pdata.get('variants', []),
        "print_areas": print_areas
    }
    
    r_put = requests.put(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json", headers=headers, json=payload)
    print(f"PUT {label} status: {r_put.status_code}")
    if r_put.status_code == 200:
        # Publish
        r_pub = requests.post(f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}/publish.json", headers=headers, json={"title": True, "description": True, "images": True, "variants": True, "tags": True})
        print(f"Publish {label} status: {r_pub.status_code}")
