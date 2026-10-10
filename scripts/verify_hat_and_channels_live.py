import sys
import io
import urllib.request
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']
headers = {'Authorization': f'Bearer {api_key}', 'User-Agent': 'KrowN/1.0'}

def api_get(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def verify_hat():
    print("="*70)
    print("1. VERIFYING RICHARDSON 112 HAT ON PRINTIFY")
    print("="*70)
    
    # Etsy Hat
    etsy_hat = api_get("https://api.printify.com/v1/shops/29252381/products/6ac80dc2f4d488e1be0b0902.json")
    print(f"\n[Etsy Store Hat]")
    print(f"Title: {etsy_hat['title']}")
    print(f"Visible: {etsy_hat['visible']} | Locked: {etsy_hat['is_locked']}")
    print(f"External Link: {etsy_hat.get('external', {}).get('handle')}")
    print(f"Listing ID: {etsy_hat.get('external', {}).get('id')}")
    pa = etsy_hat['print_areas'][0]['placeholders'][0]
    img = pa['images'][0]
    print(f"Applied Artwork ID: {img['id']} (Expected: 6ac9298bef9a14a3b58c969a)")
    print(f"Artwork Coordinates: scale={img['scale']}, x={img['x']}, y={img['y']}")
    print(f"Active Mockup Images Generated: {len(etsy_hat['images'])}")
    if etsy_hat['images']:
        print(f"Sample Front Mockup URL: {etsy_hat['images'][0]['src']}")

    # TikTok Hat
    tiktok_hat = api_get("https://api.printify.com/v1/shops/29241235/products/6ac8f2e9b0b07f13520b055c.json")
    print(f"\n[TikTok Store Hat]")
    print(f"Title: {tiktok_hat['title']}")
    print(f"Visible: {tiktok_hat['visible']} | Locked: {tiktok_hat['is_locked']}")
    pa_tt = tiktok_hat['print_areas'][0]['placeholders'][0]
    img_tt = pa_tt['images'][0]
    print(f"Applied Artwork ID: {img_tt['id']} (Expected: 6ac9298bef9a14a3b58c969a)")
    print(f"Active Mockup Images Generated: {len(tiktok_hat['images'])}")
    if tiktok_hat['images']:
        print(f"Sample Front Mockup URL: {tiktok_hat['images'][0]['src']}")

def verify_all_channels():
    print("\n" + "="*70)
    print("2. VERIFYING ALL 9 PRODUCTS ACROSS CHANNELS")
    print("="*70)
    
    shops = api_get("https://api.printify.com/v1/shops.json")
    for s in shops:
        sid = s['id']
        stitle = s['title']
        channel = s.get('sales_channel')
        if channel not in ['etsy', 'tiktok']:
            continue
        
        prods = api_get(f"https://api.printify.com/v1/shops/{sid}/products.json").get('data', [])
        print(f"\n---> {channel.upper()} CHANNEL ({stitle} - ID: {sid}) | {len(prods)} Products:")
        for idx, p in enumerate(prods, 1):
            enabled_vars = [v for v in p['variants'] if v.get('is_enabled', True)]
            prices = [v.get('price', 0) / 100 for v in enabled_vars if v.get('price')]
            price_str = f"${min(prices):.2f}" if len(prices) == 1 else f"${min(prices):.2f}-${max(prices):.2f}"
            ext_id = p.get('external', {}).get('id') if p.get('external') else 'In-Queue/Sync'
            print(f"  [{idx}] {p['title'][:45]:<45} | Price: {price_str:<12} | Variants: {len(enabled_vars)} | External: {ext_id}")

if __name__ == '__main__':
    verify_hat()
    verify_all_channels()
