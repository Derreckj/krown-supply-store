import urllib.request
import re
import json
from PIL import Image
import io

BASE_URL = 'https://www.krownsupplyco.com'

def fetch_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as res:
        return res.status, res.read().decode('utf-8')

def download_image(url):
    if not url.startswith('http'):
        url = BASE_URL + url
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as res:
        data = res.read()
        im = Image.open(io.BytesIO(data))
        return len(data), im.size, im.format

print("=== STARTING COMPLETE LIVE STORE AUDIT ===")
status, html_all = fetch_url(f'{BASE_URL}/collections/all')
print(f"1. /collections/all -> Status {status}, HTML bytes: {len(html_all)}")

# Find all product links on /collections/all
product_hrefs = list(set(re.findall(r'href=[\"\'](/products/[a-zA-Z0-9_\-]+)[\"\']', html_all)))
print(f"Total product links found on collections/all: {len(product_hrefs)}")

results = []

for href in sorted(product_hrefs):
    prod_url = f'{BASE_URL}{href}'
    try:
        p_status, p_html = fetch_url(prod_url)
        # Extract title
        title_m = re.search(r'<h1[^>]*>(.*?)</h1>', p_html)
        title = title_m.group(1).strip() if title_m else 'Unknown'

        # Extract product images
        img_srcs = re.findall(r'src=[\"\'](/images/products/[a-zA-Z0-9_\-\.]+\.jpg)[\"\']', p_html)
        unique_imgs = list(dict.fromkeys(img_srcs))

        img_details = []
        for img_url in unique_imgs:
            try:
                bytes_len, size, fmt = download_image(img_url)
                img_details.append({
                    'url': img_url,
                    'size': size,
                    'bytes': bytes_len,
                    'format': fmt,
                    'ok': True
                })
            except Exception as e_img:
                img_details.append({
                    'url': img_url,
                    'error': str(e_img),
                    'ok': False
                })

        results.append({
            'href': href,
            'title': title,
            'status': p_status,
            'images': img_details
        })
        print(f"Audited: {href} - '{title[:40]}' ({len(unique_imgs)} images verified)")
    except Exception as e:
        print(f"ERROR on {prod_url}: {e}")

print("\n=== AUDIT SUMMARY ===")
total_prods = len(results)
total_imgs = sum(len(r['images']) for r in results)
broken_imgs = sum(sum(1 for i in r['images'] if not i.get('ok', False)) for r in results)

print(f"Products Audited: {total_prods}")
print(f"Total Unique Images Checked: {total_imgs}")
print(f"Broken Images: {broken_imgs}")

# Check key products specifically
print("\n=== KEY PRODUCTS DEEP CHECK ===")
key_targets = ['kc-shaker-01', 'axiom-hoodie-01', 'krown-mat-01', 'axiom-wrist-rest-01', 'axiom-beanie-01', 'kc-beanie-01', 'axiom-sweatpants-pro', 'krown-work-01']
for r in results:
    for kt in key_targets:
        if kt in r['href']:
            print(f"\nProduct: {r['title']} ({r['href']})")
            for im in r['images']:
                print(f"  - Image: {im['url']} | Dim: {im.get('size')} | Size: {im.get('bytes', 0):,} bytes | OK: {im.get('ok')}")

with open('audit_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("\nFull audit report saved to audit_results.json")
