import os
import shutil

ARCHIVE_BASE = r"C:\Users\derre\Desktop\KrowN\Archived_Deploy_Assets_20261011"
os.makedirs(ARCHIVE_BASE, exist_ok=True)
print(f"Created archive directory: {ARCHIVE_BASE}")

# 1. Archive public/images/products/masters (75.1 MB)
src_prod_masters = "public/images/products/masters"
dst_prod_masters = os.path.join(ARCHIVE_BASE, "products_masters")
if os.path.exists(src_prod_masters):
    print(f"Archiving {src_prod_masters} -> {dst_prod_masters}...")
    shutil.copytree(src_prod_masters, dst_prod_masters, dirs_exist_ok=True)
    # Verify count
    src_cnt = len(os.listdir(src_prod_masters))
    dst_cnt = len(os.listdir(dst_prod_masters))
    print(f"Verified: {src_cnt} files in source, {dst_cnt} files in archive.")
    if src_cnt == dst_cnt:
        shutil.rmtree(src_prod_masters)
        print("Removed public/images/products/masters from deployment output.")

# 2. Archive public/images/branding/masters (6.01 MB)
src_brand_masters = "public/images/branding/masters"
dst_brand_masters = os.path.join(ARCHIVE_BASE, "branding_masters")
if os.path.exists(src_brand_masters):
    print(f"Archiving {src_brand_masters} -> {dst_brand_masters}...")
    shutil.copytree(src_brand_masters, dst_brand_masters, dirs_exist_ok=True)
    src_cnt = len(os.listdir(src_brand_masters))
    dst_cnt = len(os.listdir(dst_brand_masters))
    print(f"Verified: {src_cnt} files in source, {dst_cnt} files in archive.")
    if src_cnt == dst_cnt:
        shutil.rmtree(src_brand_masters)
        print("Removed public/images/branding/masters from deployment output.")

# 3. Archive unreferenced public/images/deliveries (10.86 MB)
# Keep only 01_KrowN_Supply_Co/KrowN_Supply_Streetwear_Tee which is referenced in audit-gallery
src_deliv = "public/images/deliveries"
dst_deliv = os.path.join(ARCHIVE_BASE, "deliveries")
if os.path.exists(src_deliv):
    print(f"Archiving unreferenced deliveries...")
    os.makedirs(dst_deliv, exist_ok=True)
    for division in os.listdir(src_deliv):
        div_path = os.path.join(src_deliv, division)
        if not os.path.isdir(div_path):
            continue
        for pack in os.listdir(div_path):
            pack_path = os.path.join(div_path, pack)
            if not os.path.isdir(pack_path):
                continue
            # Check if it's the referenced Streetwear Tee pack
            if division == "01_KrowN_Supply_Co" and pack == "KrowN_Supply_Streetwear_Tee":
                print(f"  KEEPING referenced pack: {pack_path}")
                continue
            
            # Archive this unreferenced pack
            dst_pack_path = os.path.join(dst_deliv, division, pack)
            shutil.copytree(pack_path, dst_pack_path, dirs_exist_ok=True)
            shutil.rmtree(pack_path)
            print(f"  Archived and removed: {division}/{pack}")

# 4. Archive public/media/axiom-intro.mp4 (124.6 MB)
src_video = "public/media/axiom-intro.mp4"
dst_media = os.path.join(ARCHIVE_BASE, "media")
os.makedirs(dst_media, exist_ok=True)
if os.path.exists(src_video):
    dst_video = os.path.join(dst_media, "axiom-intro.mp4")
    print(f"Archiving {src_video} -> {dst_video}...")
    shutil.copyfile(src_video, dst_video)
    if os.path.getsize(dst_video) == os.path.getsize(src_video):
        os.remove(src_video)
        print("Removed public/media/axiom-intro.mp4 from deployment output.")

# 5. Place lightweight web audio file (1.6 MB) for official Axiom Intro on homepage
desktop_music = r"C:\Users\derre\Desktop\KrowN\music\dj.mp3"
if os.path.exists(desktop_music):
    os.makedirs("public/media", exist_ok=True)
    shutil.copyfile(desktop_music, "public/media/axiom-intro.mp3")
    print(f"Installed web-optimized audio track: public/media/axiom-intro.mp3 ({os.path.getsize('public/media/axiom-intro.mp3')/1024/1024:.2f} MB)")

print("\nAsset archiving and cleanup completed successfully!")
