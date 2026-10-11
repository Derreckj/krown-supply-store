import os
from PIL import Image, ImageDraw, ImageFilter

def build_perfect_axiom_banner_mousepad():
    banner_src = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7\.user_uploaded\media_1791720004544.png"
    if not os.path.exists(banner_src):
        banner_src = "public/images/branding/gaming/axiom-owl-display.png"
    
    banner = Image.open(banner_src).convert("RGBA")
    print(f"Loaded user's Axiom Banner: {banner.size}")
    
    # Square studio canvas 1024x1024
    W, H = 1024, 1024
    canvas = Image.new("RGBA", (W, H), (14, 16, 20, 255))
    
    # Subtle dark radial vignette for studio depth
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for r in range(500, 200, -15):
        alpha = int(40 * ((500 - r) / 300))
        vdraw.ellipse([W//2 - r, H//2 - int(r*0.8), W//2 + r, H//2 + int(r*0.8)], fill=(22, 25, 32, alpha))
    canvas = Image.alpha_composite(canvas, vignette)
    
    # Desk mat dimensions: 900 x 450 (2:1 classic panoramic extended desk mat)
    mat_w, mat_h = 900, 450
    mat_x = (W - mat_w) // 2
    mat_y = (H - mat_h) // 2
    
    # 1. Soft realistic drop shadow under the desk mat
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        [mat_x - 4, mat_y + 14, mat_x + mat_w + 4, mat_y + mat_h + 24],
        radius=26,
        fill=(0, 0, 0, 200)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow)
    
    # 2. 4mm Natural rubber base border
    base_rubber = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(base_rubber)
    bdraw.rounded_rectangle(
        [mat_x - 1, mat_y + 3, mat_x + mat_w + 1, mat_y + mat_h + 5],
        radius=24,
        fill=(12, 14, 18, 255)
    )
    canvas = Image.alpha_composite(canvas, base_rubber)
    
    # 3. Fit user's Axiom Banner onto the mat surface
    # Resize banner to exact mat surface dimensions (900x450)
    banner_resized = banner.resize((mat_w, mat_h), Image.Resampling.LANCZOS)
    
    # Mask with rounded corners (radius 22px)
    mask = Image.new("L", (mat_w, mat_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, mat_w, mat_h], radius=22, fill=255)
    
    # Black precision lockstitching around edge
    stitch = Image.new("RGBA", (mat_w, mat_h), (0, 0, 0, 0))
    stdraw = ImageDraw.Draw(stitch)
    stdraw.rounded_rectangle([2, 2, mat_w - 3, mat_h - 3], radius=21, outline=(10, 12, 16, 240), width=4)
    stdraw.rounded_rectangle([4, 4, mat_w - 5, mat_h - 5], radius=19, outline=(28, 30, 36, 160), width=1)
    
    mat_comp = Image.new("RGBA", (mat_w, mat_h), (0, 0, 0, 0))
    mat_comp.paste(banner_resized, (0, 0), mask)
    mat_comp = Image.alpha_composite(mat_comp, stitch)
    
    canvas.paste(mat_comp, (mat_x, mat_y), mask)
    final_rgb = canvas.convert("RGB")
    
    # Target files to overwrite
    targets = [
        "public/images/products/axiom-mat-original-banner-v9.jpg",
        "public/images/products/axiom-mat-hero-desk-setup.jpg",
        "public/images/products/axiom-mat-display-flat-panoramic.jpg",
        "public/images/products/axiom-mat-design-a-tactical.jpg",
        "public/images/products/axiom-mat-stitched-macro.jpg",
        "public/images/products/axiom-mat-design-b-sovereign.jpg",
        "public/images/products/axiom-owl-desk-mat-photorealistic.jpg",
        "public/images/products/axiom-owl-realistic-axa-face-desk-mat.jpg",
        "public/images/products/masters/axiom-mat-original-banner-v9.jpg",
    ]
    
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        final_rgb.save(t, "JPEG", quality=98)
        print(f"Saved clean Axiom Banner mousepad to {t}")
        
    print("\nSuccessfully replaced 1st mouse pad photo with clean Axiom Banner across all targets!")

if __name__ == "__main__":
    build_perfect_axiom_banner_mousepad()
