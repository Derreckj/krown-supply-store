import shutil
import os

prod_dir = 'public/images/products'
src_master = 'test_krown_luxury_shaker_final.jpg'

krown_targets = [
    'krown-shaker-photoreal-v6.jpg',
    'krown-shaker-smoke-v6.jpg',
    'krown-shaker-brushed-v6.jpg',
    'krown-shaker-obsidian-steel.jpg',
    'krown-shaker-obsidian-tritan.jpg',
    'krown-shaker-obsidian-steel-v2.jpg',
    'krown-shaker-smoke-steel.jpg',
    'krown-shaker-smoke-tritan.jpg',
    'krown-shaker-brushed-steel.jpg',
    'krown-shaker-brushed-tritan.jpg',
]

for t in krown_targets:
    dst = os.path.join(prod_dir, t)
    shutil.copyfile(src_master, dst)
    print(f"Copied {src_master} -> {dst}")

print("All KrowN Supply Co shaker variant images unified to master!")
