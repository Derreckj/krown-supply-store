import os
import requests

def inspect_shops():
    key = None
    with open('.env.local', 'r') as f:
        for l in f:
            if l.startswith('PRINTIFY_API_KEY='):
                key = l.strip().split('=', 1)[1]

    headers = {'Authorization': f'Bearer {key}'}

    for shop_id, name in [(29241235, 'TikTok'), (29252381, 'Etsy')]:
        print(f"\n=== {name} (Shop ID: {shop_id}) ===")
        r = requests.get(f"https://api.printify.com/v1/shops/{shop_id}/products.json", headers=headers)
        if r.status_code != 200:
            print("Error:", r.status_code, r.text)
            continue
        products = r.json().get('data', [])
        print(f"Total products: {len(products)}")
        for p in products:
            pid = p.get('id')
            title = p.get('title')
            b_id = p.get('blueprint_id')
            prov_id = p.get('print_provider_id')
            variants_count = len(p.get('variants', []))
            is_locked = p.get('is_locked')
            visible = p.get('visible')
            print(f"  ID: {pid} | {title} | Blueprint: {b_id} | Provider: {prov_id} | Variants: {variants_count} | Visible: {visible}")

if __name__ == '__main__':
    inspect_shops()
