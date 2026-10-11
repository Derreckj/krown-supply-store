import shutil
from PIL import Image

banner_src = "public/images/products/axiom-mat-original-banner-v9.jpg"
im_banner = Image.open(banner_src).convert("RGB")

unwanted_mat_targets = [
    'axiom-mat-hero-desk-setup.jpg',
    'axiom-mat-display-flat-panoramic.jpg',
    'axiom-mat-design-a-tactical.jpg',
    'axiom-mat-stitched-macro.jpg',
    'axiom-mat-design-b-sovereign.jpg',
    'axiom-owl-desk-mat-photorealistic.jpg',
    'axiom-owl-realistic-axa-face-desk-mat.jpg',
]

for t in unwanted_mat_targets:
    p = f"public/images/products/{t}"
    im_banner.save(p, "JPEG", quality=98)
    print(f"Overwrote {p} with clean official banner")

print("All unwanted mousepad images eliminated and replaced with clean official banner!")
