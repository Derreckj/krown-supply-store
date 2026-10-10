import os
import shutil

src_dir = 'public/images/products'
vault_dir = 'public/images/products/masters'
os.makedirs(vault_dir, exist_ok=True)

copied = 0
for f in os.listdir(src_dir):
    if f == 'masters':
        continue
    src_file = os.path.join(src_dir, f)
    if os.path.isfile(src_file) and f.endswith(('.jpg', '.png', '.webp')):
        dst_file = os.path.join(vault_dir, f)
        shutil.copyfile(src_file, dst_file)
        copied += 1

print(f"Vaulted {copied} master product images to {vault_dir}")
