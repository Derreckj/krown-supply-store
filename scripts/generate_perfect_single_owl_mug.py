import numpy as np
from PIL import Image

def generate_perfect_single_owl_mug():
    src_path = r"C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7\.user_uploaded\media_1791721737036.jpg"
    orig = Image.open(src_path).convert("RGB")
    arr = np.array(orig).copy()
    
    pts_left = [
        (220, 431),
        (240, 431),
        (260, 432),
        (280, 436),
        (300, 442),
        (320, 445),
        (340, 442),
        (360, 440),
        (380, 436),
        (400, 434),
        (420, 434),
        (440, 437),
        (460, 442),
        (480, 449),
        (500, 458),
        (520, 470),
        (540, 485),
        (560, 496),
        (580, 505),
        (600, 505)
    ]
    
    pts_right = [
        (220, 579),
        (241, 579),
        (260, 578),
        (280, 574),
        (300, 568),
        (320, 565),
        (340, 568),
        (360, 570),
        (380, 574),
        (400, 576),
        (420, 576),
        (440, 573),
        (460, 568),
        (480, 561),
        (500, 552),
        (520, 540),
        (540, 525),
        (560, 514),
        (580, 505),
        (600, 505)
    ]
    
    y_l, x_l = zip(*pts_left)
    y_r, x_r = zip(*pts_right)
    
    inner_left_map = np.interp(np.arange(1024), y_l, x_l)
    inner_right_map = np.interp(np.arange(1024), y_r, x_r)
    
    def brow_y(x):
        dx = x - 505
        return 340 - 99 * ((dx / 74) ** 2)
    
    for y in range(220, 585):
        xl = int(inner_left_map[y])
        xr = int(inner_right_map[y])
        
        # Clean left side (ghost left horn & ghost left wing):
        for x in range(340, xl):
            ref_c = np.median(arr[y, 310:335], axis=0)
            noise = np.random.normal(0, 1.0, 3)
            arr[y, x] = np.clip(ref_c + noise, 0, 255).astype(np.uint8)
            
        # Clean right side (ghost right horn & ghost right wing):
        for x in range(xr + 1, 675):
            ref_c = np.median(arr[y, 675:700], axis=0)
            noise = np.random.normal(0, 1.0, 3)
            arr[y, x] = np.clip(ref_c + noise, 0, 255).astype(np.uint8)
            
        # Clean between horns if above the brow curve:
        for x in range(max(xl, 431), min(xr, 580)):
            if y < brow_y(x):
                t = (x - 431) / (579 - 431)
                c_l = np.median(arr[y, 310:335], axis=0)
                c_r = np.median(arr[y, 675:700], axis=0)
                interp = (1 - t) * c_l + t * c_r
                noise = np.random.normal(0, 1.0, 3)
                arr[y, x] = np.clip(interp + noise, 0, 255).astype(np.uint8)
                
    cleaned = Image.fromarray(arr)
    
    # Save production image
    out_path = "public/images/products/axiom-mug-desk-setup.jpg"
    cleaned.save(out_path, "JPEG", quality=96)
    cleaned.save("public/images/products/axiom-mug-single-owl-official.jpg", "JPEG", quality=96)
    cleaned.save("public/images/products/axiom-mug-clean-photoreal-15oz-v3.jpg", "JPEG", quality=96)
    cleaned.save("public/images/products/axiom-mug-lime-interior.jpg", "JPEG", quality=96)
    cleaned.save("public/images/products/axiom-mug-crest-detail.jpg", "JPEG", quality=96)
    cleaned.save("public/images/products/axiom-mug-specifications.jpg", "JPEG", quality=96)
    print("Successfully generated perfect single-owl mug photo!")

if __name__ == "__main__":
    generate_perfect_single_owl_mug()
