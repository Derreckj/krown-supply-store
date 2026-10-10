import os
import shutil
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'public', 'images', 'products')
MASTERS_DIR = os.path.join(PROD_DIR, 'masters')

# Master realistic workbench shaker photo (with tools pegboard, steel workbench, water droplets, and whisk ball)
src_master = 'test_commit_88c_kc.jpg'

kc_targets = [
    'kc-shaker-photoreal-v6.jpg',
    'kc-shaker-steelcore-v6.jpg',
    'kc-shaker-tradesman-v6.jpg',
    'kc-shaker-highvis-steel.jpg',
    'kc-shaker-highvis-steel-v2.jpg',
    'kc-shaker-highvis-tritan.jpg',
    'kc-shaker-highvis-tritan-v3.jpg',
    'kc-shaker-highvis-tritan-v4.jpg',
    'kc-shaker-steelcore-steel.jpg',
    'kc-shaker-steelcore-tritan.jpg',
    'kc-shaker-jobsite-steel.jpg',
    'kc-shaker-jobsite-tritan.jpg',
]

for t in kc_targets:
    p = os.path.join(PROD_DIR, t)
    m = os.path.join(MASTERS_DIR, t)
    shutil.copyfile(src_master, p)
    shutil.copyfile(src_master, m)
    print(f"Unified KC Shaker: {t}")

print("All KrowN Construction shaker targets unified to photorealistic master!")
