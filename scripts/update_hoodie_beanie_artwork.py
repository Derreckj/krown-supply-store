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

CREST_IMG_ID = '6ac9306a928f403068ae59bf' # transparent gold crown
PATCH_IMG_ID = '6ac9298bef9a14a3b58c969a' # transparent leather patch

def update_product_artwork(shop_id, prod_id, new_img_id, scale=0.70, y_pos=0.45):
    url = f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}.json"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        prod = json.loads(resp.read().decode())
    
    all_var_ids = [v['id'] for v in prod['variants']]
    
    put_payload = {
        'print_areas': [
            {
                'variant_ids': all_var_ids,
                'placeholders': [
                    {
                        'position': 'front',
                        'images': [
                            {
                                'id': new_img_id,
                                'x': 0.5,
                                'y': y_pos,
                                'scale': scale,
                                'angle': 0
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    put_req = urllib.request.Request(url, data=json.dumps(put_payload).encode('utf-8'), headers=headers, method='PUT')
    with urllib.request.urlopen(put_req) as resp:
        print(f"  ✓ Updated product {prod_id} print area with clean transparent artwork!")
    
    time.sleep(1)
    pub_url = f"https://api.printify.com/v1/shops/{shop_id}/products/{prod_id}/publish.json"
    pub_req = urllib.request.Request(pub_url, data=json.dumps({'title': True, 'description': True, 'images': True, 'variants': True, 'tags': True}).encode('utf-8'), headers=headers, method='POST')
    with urllib.request.urlopen(pub_req) as resp:
        print(f"  ✓ Re-published {prod_id}!")

def main():
    print("--- 1. Updating Heavyweight 480 GSM Hoodie ---")
    # Etsy Hoodie (29252381 / 6ac80dff9f3e89dde70da38d)
    print("Updating Etsy Hoodie...")
    update_product_artwork(29252381, '6ac80dff9f3e89dde70da38d', CREST_IMG_ID, scale=0.65, y_pos=0.45)
    
    # TikTok Hoodie (29241235 / 6ac8f2e4af7641b637093037)
    print("Updating TikTok Hoodie...")
    update_product_artwork(29241235, '6ac8f2e4af7641b637093037', CREST_IMG_ID, scale=0.65, y_pos=0.45)

    print("\n--- 2. Updating Heavy Ribbed Beanie ---")
    # Etsy Beanie (29252381 / 6ac80e07cafb2cd4c60b7c96)
    print("Updating Etsy Beanie...")
    update_product_artwork(29252381, '6ac80e07cafb2cd4c60b7c96', PATCH_IMG_ID, scale=0.65, y_pos=0.50)

    # TikTok Beanie (29241235 / 6ac8f2d10a804851a8009ad3)
    print("Updating TikTok Beanie...")
    update_product_artwork(29241235, '6ac8f2d10a804851a8009ad3', PATCH_IMG_ID, scale=0.65, y_pos=0.50)

    print("\nPrintify product artwork update complete!")

if __name__ == '__main__':
    main()
