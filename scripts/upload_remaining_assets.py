import urllib.request
import json
import base64

with open('.env.local') as f:
    env = dict(line.strip().split('=', 1) for line in f if '=' in line and not line.startswith('#'))

api_key = env['PRINTIFY_API_KEY']

files = [
    ('public/images/branding/krown-logo-icon.png', 'krown-logo-icon.png'),
    ('public/images/branding/construction/KC.jpg', 'KC-construction-banner.jpg'),
    ('public/images/branding/construction/Krown Construction.png', 'Krown-Construction-Emblem.png')
]

for path, fname in files:
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    payload = json.dumps({'file_name': fname, 'contents': b64}).encode('utf-8')
    req = urllib.request.Request(
        'https://api.printify.com/v1/uploads/images.json',
        data=payload,
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'User-Agent': 'KrowN/1.0'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"{fname} -> ID: {res.get('id')}")
