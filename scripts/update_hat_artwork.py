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

new_img_id = '6ac9298bef9a14a3b58c969a'

shops_products = [
    (29252381, '6ac80dc2f4d488e1be0b0902', 'Etsy'),
    (29241235, '6ac8f2e9b0b07f13520b055c', 'TikTok')
]

for shop_id, prod_id, platform in shops_products:
    print(f"\nUpdating {platform} product ({prod_id})...")
    get_req = urllib.request.Request(f'https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json', headers=headers)
    with urllib.request.urlopen(get_req) as resp:
        prod = json.loads(resp.read().decode())
    
    all_variant_ids = [v['id'] for v in prod['variants']]
    
    update_payload = {
        'title': 'KrowN Supply Co. Richardson 112 Leather Patch Trucker Snapback',
        'description': '<p>Authentic Richardson 112 Classic Trucker Snapback featuring our official laser-engraved KrowN Supply Co. saddle-brown leather hexagon patch with stitched border. Structured mid-profile 6-panel design with pre-curved visor, contrast stitching, and breathable mesh back. Wear the KrowN.</p>',
        'tags': ['richardson 112', 'trucker hat', 'leather patch hat', 'krown supply co', 'snapback hat', 'mens hat'],
        'print_areas': [
            {
                'variant_ids': all_variant_ids,
                'placeholders': [
                    {
                        'position': 'front',
                        'images': [
                            {
                                'id': new_img_id,
                                'x': 0.5,
                                'y': 0.5,
                                'scale': 0.70,
                                'angle': 0
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    put_req = urllib.request.Request(
        f'https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json',
        data=json.dumps(update_payload).encode('utf-8'),
        headers=headers,
        method='PUT'
    )
    with urllib.request.urlopen(put_req) as resp:
        print(f"  ✓ Updated {platform} product artwork!")
    
    time.sleep(2)
    pub_req = urllib.request.Request(
        f'https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}/publish.json',
        data=json.dumps({'title': True, 'description': True, 'images': True, 'variants': True, 'tags': True}).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(pub_req) as resp:
        print(f"  ✓ Initiated re-publish to {platform}!")

print("\nFinished updating hat on Printify for Etsy and TikTok!")
