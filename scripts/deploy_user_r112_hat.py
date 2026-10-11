import shutil
from PIL import Image

src = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7\.user_uploaded\media_1791719767628.png"
dst = r"public/images/products/axiom-r112-leather-patch-charcoal.jpg"
dst_master = r"public/images/products/masters/axiom-r112-leather-patch-charcoal.jpg"

im = Image.open(src).convert("RGB")
# Scale up with high quality LANCZOS to 1024x1024
im_1024 = im.resize((1024, 1024), Image.Resampling.LANCZOS)
im_1024.save(dst, "JPEG", quality=98)
im_1024.save(dst_master, "JPEG", quality=98)
print(f"Saved {dst} at 1024x1024 quality 98")

# Also overwrite any other r112 hat image paths so they cannot display anything else
other_hat_targets = [
    'axiom-r112-worn-lifestyle.jpg',
    'axiom-r112-mesh-profile.jpg',
    'axiom-r112-leather-macro.jpg',
    'axiom-r112-supplier-specs.jpg',
    'axiom-r112-leather-patch-hero.jpg',
    'axiom-r112-photoreal-hero.jpg'
]

for t in other_hat_targets:
    p = f"public/images/products/{t}"
    im_1024.save(p, "JPEG", quality=98)
    print(f"Overwrote {p} with single official user hat image")

print("Finished deploying single official Axiom Richardson 112 hat image!")
