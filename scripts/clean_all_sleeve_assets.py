import os
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
from collections import deque

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_UPLOADED_DIR = r"C:\Users\derre\.gemini\antigravity-ide\brain\b3121527-ae41-459e-801f-4ef537223171\.user_uploaded"
PUBLIC_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
PUBLIC_BRANDING_GAMING = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")

os.makedirs(PUBLIC_PRODUCTS, exist_ok=True)
os.makedirs(PUBLIC_BRANDING_GAMING, exist_ok=True)

def remove_white_background_bfs(pil_img, tolerance=12):
    """
    Performs BFS from image edges to find pure/near-white outer background
    and turns it into clean transparent alpha without affecting inner graphics.
    """
    img = pil_img.convert("RGBA")
    arr = np.array(img)
    h, w = arr.shape[:2]

    # Background is near white: R, G, B >= (255 - tolerance)
    is_white = (arr[:, :, 0] >= (255 - tolerance)) & \
               (arr[:, :, 1] >= (255 - tolerance)) & \
               (arr[:, :, 2] >= (255 - tolerance))

    visited = np.zeros((h, w), dtype=bool)
    q = deque()

    # Seed with all boundary pixels that match white
    for x in range(w):
        if is_white[0, x]:
            q.append((0, x))
            visited[0, x] = True
        if is_white[h - 1, x]:
            q.append((h - 1, x))
            visited[h - 1, x] = True

    for y in range(h):
        if is_white[y, 0] and not visited[y, 0]:
            q.append((y, 0))
            visited[y, 0] = True
        if is_white[y, w - 1] and not visited[y, w - 1]:
            q.append((y, w - 1))
            visited[y, w - 1] = True

    while q:
        cy, cx = q.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_white[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    # Mask alpha
    alpha = arr[:, :, 3].astype(np.float32)
    alpha[visited] = 0.0

    # Defringe edge pixels: For non-visited pixels adjacent to visited, soften alpha and defringe white
    mask_img = Image.fromarray((alpha).astype(np.uint8), mode='L')
    # Soft 1px edge
    feathered_mask = mask_img.filter(ImageFilter.SMOOTH)
    
    # Recombine
    arr[:, :, 3] = np.array(feathered_mask)
    result = Image.fromarray(arr, mode="RGBA")
    return result

def crop_to_content(pil_img, padding=20):
    """Crops transparent PNG to non-transparent bounding box with padding."""
    arr = np.array(pil_img)
    alpha = arr[:, :, 3]
    non_zero = np.where(alpha > 15)
    if len(non_zero[0]) == 0:
        return pil_img

    y_min, y_max = non_zero[0].min(), non_zero[0].max()
    x_min, x_max = non_zero[1].min(), non_zero[1].max()

    h, w = arr.shape[:2]
    crop_ymin = max(0, y_min - padding)
    crop_ymax = min(h, y_max + padding)
    crop_xmin = max(0, x_min - padding)
    crop_xmax = min(w, x_max + padding)

    return pil_img.crop((crop_xmin, crop_ymin, crop_xmax, crop_ymax))

def render_studio_mockup(transparent_img, canvas_w=1000, canvas_h=1000, bg_color=(13, 15, 18)):
    """
    Places the isolated transparent product on a luxury dark studio canvas
    with radial spotlight and realistic soft contact shadow.
    """
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (bg_color[0], bg_color[1], bg_color[2], 255))
    
    # Create radial gradient spotlight in the center
    spotlight = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    spot_draw = ImageDraw.Draw(spotlight)
    center_x, center_y = canvas_w // 2, canvas_h // 2
    for r in range(int(canvas_w * 0.45), 0, -12):
        intensity = int(22 * (1.0 - r / (canvas_w * 0.45)))
        # Subtle violet/emerald tint matching Axiom brand
        spot_draw.ellipse(
            [center_x - r, center_y - r * 1.1, center_x + r, center_y + r * 1.1],
            fill=(40, 25, 55, intensity)
        )
    canvas = Image.alpha_composite(canvas, spotlight)

    # Scale product to fit comfortably (max 82% height, max 78% width)
    max_h = int(canvas_h * 0.84)
    max_w = int(canvas_w * 0.78)
    scale = min(max_w / transparent_img.width, max_h / transparent_img.height)
    new_w = int(transparent_img.width * scale)
    new_h = int(transparent_img.height * scale)
    scaled_img = transparent_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Create subtle drop shadow
    shadow_offset_y = int(new_h * 0.02)
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    pos_x = (canvas_w - new_w) // 2
    pos_y = (canvas_h - new_h) // 2

    # Shadow silhouette from alpha
    scaled_arr = np.array(scaled_img)
    shadow_arr = np.zeros_like(scaled_arr)
    shadow_arr[:, :, 3] = (scaled_arr[:, :, 3].astype(np.float32) * 0.45).astype(np.uint8)
    shadow_img = Image.fromarray(shadow_arr).filter(ImageFilter.GaussianBlur(18))
    
    canvas.paste(shadow_img, (pos_x, pos_y + shadow_offset_y), shadow_img)
    canvas.paste(scaled_img, (pos_x, pos_y), scaled_img)
    return canvas

def main():
    print("=== Cleaning Sleeve Assets ===")

    # 1. 3D Sleeve Back / Elbow view (Owl Eyes motif)
    # File: media_1791413065395.png
    src_3d_back = os.path.join(USER_UPLOADED_DIR, "media_1791413065395.png")
    if os.path.exists(src_3d_back):
        print("Processing 3D Sleeve (Back/Elbow view)...")
        raw = Image.open(src_3d_back)
        # Crop out top phone status bar (0..150) and bottom Android nav (961..1024)
        crop_ui = raw.crop((0, 150, raw.width, 961))
        # Remove white outer background via BFS
        isolated = remove_white_background_bfs(crop_ui, tolerance=15)
        # Crop tightly to sleeve
        tight = crop_to_content(isolated, padding=15)
        
        # Save transparent PNG
        out_trans = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-3d-back.png")
        tight.save(out_trans, format="PNG", optimize=True)
        print(f"Saved: {out_trans} ({tight.size})")

        # Save studio mockup version
        studio = render_studio_mockup(tight)
        out_studio = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-3d-back-studio.png")
        studio.save(out_studio, format="PNG", optimize=True)
        print(f"Saved: {out_studio}")
    else:
        print(f"File not found: {src_3d_back}")

    # 2. 3D Sleeve Front / Forearm view (AXIOM ALLEGIANCE text + owl crest)
    # File: media_1791413112174.png
    src_3d_front = os.path.join(USER_UPLOADED_DIR, "media_1791413112174.png")
    if os.path.exists(src_3d_front):
        print("Processing 3D Sleeve (Front/Forearm view)...")
        raw = Image.open(src_3d_front)
        # Crop out top phone status bar (0..160) and bottom Android nav (961..1024)
        crop_ui = raw.crop((0, 160, raw.width, 961))
        # Remove white outer background via BFS
        isolated = remove_white_background_bfs(crop_ui, tolerance=15)
        # Crop tightly to sleeve
        tight = crop_to_content(isolated, padding=15)
        
        # Save transparent PNG
        out_trans = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-3d-front.png")
        tight.save(out_trans, format="PNG", optimize=True)
        print(f"Saved: {out_trans} ({tight.size})")

        # Save studio mockup version
        studio = render_studio_mockup(tight)
        out_studio = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-3d-front-studio.png")
        studio.save(out_studio, format="PNG", optimize=True)
        print(f"Saved: {out_studio}")
    else:
        print(f"File not found: {src_3d_front}")

    # 3. Clean Flat Blueprint View (Strip editor bounding box, handles, and canvas)
    # Source: existing public/images/products/axiom-arm-sleeve-mockup.png
    src_flat = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-mockup.png")
    if os.path.exists(src_flat):
        print("Processing Flat Sleeve Design (removing bounding box & resize handles)...")
        flat_raw = Image.open(src_flat).convert("RGBA")
        arr = np.array(flat_raw)
        
        # The sleeve itself is in [31:565, 360:665]
        # Crop inside the selection box to completely discard handles at x=324, x=690, y=582
        sleeve_crop = flat_raw.crop((360, 31, 665, 565))
        
        # Remove dark background around the flat trapezoid:
        s_arr = np.array(sleeve_crop)
        # Pixels that are outer black / canvas: R, G, B < 15
        is_canvas = (s_arr[:, :, 0] < 12) & (s_arr[:, :, 1] < 12) & (s_arr[:, :, 2] < 12)
        
        # BFS from edges of sleeve_crop to clear only the outer canvas
        h_s, w_s = s_arr.shape[:2]
        visited_s = np.zeros((h_s, w_s), dtype=bool)
        q_s = deque()
        for x in range(w_s):
            if is_canvas[0, x]: q_s.append((0, x)); visited_s[0, x] = True
            if is_canvas[h_s-1, x]: q_s.append((h_s-1, x)); visited_s[h_s-1, x] = True
        for y in range(h_s):
            if is_canvas[y, 0] and not visited_s[y, 0]: q_s.append((y, 0)); visited_s[y, 0] = True
            if is_canvas[y, w_s-1] and not visited_s[y, w_s-1]: q_s.append((y, w_s-1)); visited_s[y, w_s-1] = True

        while q_s:
            cy, cx = q_s.popleft()
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h_s and 0 <= nx < w_s and not visited_s[ny, nx] and is_canvas[ny, nx]:
                    visited_s[ny, nx] = True
                    q_s.append((ny, nx))

        s_arr[visited_s, 3] = 0
        cleaned_flat = Image.fromarray(s_arr, mode="RGBA")
        tight_flat = crop_to_content(cleaned_flat, padding=12)

        out_flat_trans = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-flat.png")
        tight_flat.save(out_flat_trans, format="PNG", optimize=True)
        print(f"Saved: {out_flat_trans} ({tight_flat.size})")

        studio_flat = render_studio_mockup(tight_flat, canvas_w=1000, canvas_h=1000)
        out_flat_studio = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-flat-studio.png")
        studio_flat.save(out_flat_studio, format="PNG", optimize=True)
        print(f"Saved: {out_flat_studio}")

    # 4. Also set primary default mockup axiom-arm-sleeve-mockup.png to the clean 3D front studio render
    # so any existing component that references it displays the pristine image immediately!
    primary_src = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-3d-front-studio.png")
    if os.path.exists(primary_src):
        img_primary = Image.open(primary_src)
        dest_mockup = os.path.join(PUBLIC_PRODUCTS, "axiom-arm-sleeve-mockup.png")
        img_primary.save(dest_mockup, format="PNG", optimize=True)
        print(f"Updated default mockup: {dest_mockup}")

    print("=== All sleeve assets successfully cleaned and processed! ===")

if __name__ == "__main__":
    main()
