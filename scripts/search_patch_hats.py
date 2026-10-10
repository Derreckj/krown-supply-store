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

req = urllib.request.Request('https://api.printify.com/v1/catalog/blueprints.json', headers=headers)
with urllib.request.urlopen(req) as resp:
    bps = json.loads(resp.read().decode())
    for bp in bps:
        title = bp.get('title', '').lower()
        desc = (bp.get('description') or '').lower()
        brand = (bp.get('brand') or '').lower()
        if any(w in title or w in brand for w in ['richardson', 'patch', 'leather', 'trucker', 'hat', 'cap']):
            print(f"ID: {bp['id']} | Title: '{bp['title']}' | Brand: '{bp.get('brand')}'")
