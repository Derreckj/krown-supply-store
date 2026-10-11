import os
import numpy as np
from PIL import Image

def generate_and_deploy_perfect_mug():
    mug_src = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7\.user_uploaded\media_1791722251842.jpg"
    owl_src = r"C:\Users\derre\Desktop\KrowN\Axiom\Owl Transp (1).png"
    
    print(f"Loading mug photo: {mug_src}")
    print(f"Loading master owl artwork: {owl_src}")
    
    orig = Image.open(mug_src).convert("RGB")
    arr = np.array(orig).astype(np.float32)
    
    # 1. Seamless ceramic restoration using Coons transfinite bi-harmonic patch
    y1, y2 = 310, 742
    x1, x2 = 345, 670
    
    H = y2 - y1 + 1
    W = x2 - x1 + 1
    
    top = arr[y1, x1:x2+1]
    bot = arr[y2, x1:x2+1]
    left = arr[y1:y2+1, x1]
    right = arr[y1:y2+1, x2]
    
    c_tl = arr[y1, x1]
    c_tr = arr[y1, x2]
    c_bl = arr[y2, x1]
    c_br = arr[y2, x2]
    
    ty = np.linspace(0, 1, H)[:, None, None]
    tx = np.linspace(0, 1, W)[None, :, None]
    
    r_h = (1 - tx) * left[:, None, :] + tx * right[:, None, :]
    r_v = (1 - ty) * top[None, :, :] + ty * bot[None, :, :]
    r_c = ((1 - tx) * (1 - ty) * c_tl +
           tx * (1 - ty) * c_tr +
           (1 - tx) * ty * c_bl +
           tx * ty * c_br)
    
    coons = r_h + r_v - r_c
    
    # Natural ceramic micro-grain
    np.random.seed(42)
    noise = np.random.normal(0, 0.6, coons.shape)
    coons_noisy = np.clip(coons + noise, 0, 255)
    
    # Smooth perimeter alpha ramp (10 pixels) for seamless boundary integration
    dy = np.minimum(np.arange(H), H - 1 - np.arange(H))
    dx = np.minimum(np.arange(W), W - 1 - np.arange(W))
    dist_map = np.minimum(dy[:, None], dx[None, :])
    alpha_ramp = np.clip(dist_map / 10.0, 0.0, 1.0)[:, :, None]
    alpha_ramp = alpha_ramp * alpha_ramp * (3 - 2 * alpha_ramp)
    
    orig_patch = arr[y1:y2+1, x1:x2+1]
    blended_patch = (1 - alpha_ramp) * orig_patch + alpha_ramp * coons_noisy
    
    clean_arr = arr.copy()
    clean_arr[y1:y2+1, x1:x2+1] = blended_patch
    clean_mug_img = Image.fromarray(np.clip(clean_arr, 0, 255).astype(np.uint8))
    
    # 2. Resize authentic master owl artwork (preserves exact proportions, colors, A-X-A geometry)
    owl_img = Image.open(owl_src).convert("RGBA")
    owl_w = 284
    owl_h = 390
    owl_resized = owl_img.resize((owl_w, owl_h), Image.Resampling.LANCZOS)
    
    # Cylindrical curvature shading & ambient lighting integration
    owl_np = np.array(owl_resized).astype(np.float32)
    xs = np.linspace(-1, 1, owl_w)
    cylinder_factor = np.cos(xs * np.pi / 4.2)
    cylinder_shading = np.tile(cylinder_factor[np.newaxis, :, np.newaxis], (owl_h, 1, 3))
    
    right_ambient = (np.linspace(0, 1, owl_w) ** 2)[:, np.newaxis]
    ambient_purple = np.zeros((owl_h, owl_w, 3), dtype=np.float32)
    ambient_purple[:, :, 0] = right_ambient.T * 10
    ambient_purple[:, :, 2] = right_ambient.T * 20
    
    owl_np[:, :, :3] = owl_np[:, :, :3] * (0.87 + 0.13 * cylinder_shading) + ambient_purple
    owl_np[:, :, :3] = np.clip(owl_np[:, :, :3], 0, 255)
    
    final_owl = Image.fromarray(owl_np.astype(np.uint8), mode="RGBA")
    
    # 3. Composite single centered owl
    # Center X = 508 -> pos_x = 508 - 284 // 2 = 366
    # Top Y = 330
    pos_x = 366
    pos_y = 330
    clean_mug_img.paste(final_owl, (pos_x, pos_y), final_owl)
    
    # Verify boundaries
    arr_final = np.array(clean_mug_img).astype(float)
    diff_top = np.abs(arr_final[y1, x1:x2+1] - arr_final[y1-1, x1:x2+1]).max()
    diff_bot = np.abs(arr_final[y2, x1:x2+1] - arr_final[y2+1, x1:x2+1]).max()
    diff_left = np.abs(arr_final[y1:y2+1, x1] - arr_final[y1:y2+1, x1-1]).max()
    diff_right = np.abs(arr_final[y1:y2+1, x2] - arr_final[y1:y2+1, x2+1]).max()
    print(f"Boundary verification: top={diff_top:.1f}, bot={diff_bot:.1f}, left={diff_left:.1f}, right={diff_right:.1f}")
    
    # 4. Save canonical production targets
    pub_dir = "public/images/products"
    os.makedirs(pub_dir, exist_ok=True)
    
    canonical_name = "axiom-mug-single-owl-official.jpg"
    canonical_path = os.path.join(pub_dir, canonical_name)
    clean_mug_img.save(canonical_path, "JPEG", quality=98)
    print(f"Saved canonical: {canonical_path}")
    
    # Overwrite all legacy fallback filenames so stale caches/references render single owl
    legacy_files = [
        "axiom-mug-clean-photoreal-15oz-v3.jpg",
        "axiom-mug-clean-photoreal-15oz.jpg",
        "axiom-mug-desk-setup.jpg",
        "axiom-mug-lime-interior.jpg",
        "axiom-mug-crest-detail.jpg",
        "axiom-mug-specifications.jpg",
        "axiom-mug-smokey-crest-15oz.jpg",
    ]
    for lf in legacy_files:
        lp = os.path.join(pub_dir, lf)
        clean_mug_img.save(lp, "JPEG", quality=98)
        print(f"Updated legacy target: {lp}")
        
    print("\nAll mug image targets successfully updated!")

if __name__ == "__main__":
    generate_and_deploy_perfect_mug()
