import shutil
import os

prod_dir = 'public/images/products'
hoodie_master = os.path.join(prod_dir, 'axiom-heavyweight-hoodie-photoreal-v6.jpg')

targets = [
    'axiom-heavyweight-hoodie-v3.jpg',
    'axiom-heavyweight-hoodie-v2.jpg',
    'axiom-heavyweight-hoodie-studio.jpg',
]

for t in targets:
    dst = os.path.join(prod_dir, t)
    shutil.copyfile(hoodie_master, dst)
    print(f"Synced {dst}")

print("All Axiom hoodie backup targets synced to photoreal v6!")
