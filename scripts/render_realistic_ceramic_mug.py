import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB_PRODUCTS = os.path.join(BASE_DIR, "public", "images", "products")
GAMING_DIR = os.path.join(BASE_DIR, "public", "images", "branding", "gaming")

# Assets
owl_path = os.path.join(GAMING_DIR, "axiom-smokey-owl-green-eyes-clean.png")
gothic_path = os.path.join(GAMING_DIR, "axiom-two-tone-gothic-clean-alpha.png")

owl_img = Image.open(owl_path).convert("RGBA")
gothic_img = Image.open(gothic_path).convert("RGBA")

def render_photoreal_ceramic_mug(out_filename="axiom-mug-smokey-crest-15oz.png"):
    W, H = 1024, 1024
    
    # 1. Realistic Studio Environment (Dark Wood Battlestation Desk + Atmospheric Ambient)
    # Upper half: Soft dark obsidian gradient with subtle purple ambient glow
    # Lower half (y > 640): Dark studio walnut/battlestation desk with perspective lighting
    canvas = Image.new("RGBA", (W, H), (14, 15, 18, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Atmospheric background gradient
    for y in range(650):
        t = y / 650.0
        r = int(10 + 12 * (1.0 - t))
        g = int(11 + 6 * (1.0 - t))
        b = int(16 + 18 * (1.0 - t))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Subtle soft violet/purple glow in the center backdrop
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for r in range(400, 0, -10):
        alpha = int(22 * (1.0 - r / 400.0))
        gdraw.ellipse([512 - r, 420 - int(r*0.7), 512 + r, 420 + int(r*0.7)], fill=(45, 15, 65, alpha))
    canvas = Image.alpha_composite(canvas, glow)
    draw = ImageDraw.Draw(canvas)
    
    # Tabletop Surface (y = 620 to 1024)
    table_top_y = 620
    for y in range(table_top_y, H):
        t = (y - table_top_y) / (H - table_top_y)
        # Deep matte studio tabletop with subtle surface light
        tr = int(18 + 10 * t)
        tg = int(19 + 9 * t)
        tb = int(22 + 8 * t)
        draw.line([(0, y), (W, y)], fill=(tr, tg, tb))
        
    # Table surface soft horizon blur line
    draw.line([(0, table_top_y), (W, table_top_y)], fill=(32, 34, 40), width=2)
    
    # 2. Mug Dimensions and Placement
    # Standard 15oz Ceramic Mug: Slightly taller than wide
    cx, cy = 490, 520
    mug_w = 420
    mug_h = 470
    
    # Base and Top coordinates
    top_y = cy - mug_h // 2
    bot_y = cy + mug_h // 2
    left_x = cx - mug_w // 2
    right_x = cx + mug_w // 2
    
    # 3. Soft Realistic Contact Shadow on Table
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    # Broad soft ambient shadow
    sdraw.ellipse([cx - 240, bot_y - 25, cx + 290, bot_y + 110], fill=(0, 0, 0, 160))
    # Tight occlusion shadow directly under base
    sdraw.ellipse([cx - 205, bot_y - 12, cx + 205, bot_y + 35], fill=(0, 0, 0, 220))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.alpha_composite(canvas, shadow)
    
    # 4. Realistic Ceramic Handle (Attached on Right side)
    # The handle is glossy black on the outer contour, with glossy electric lime interior
    handle_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(handle_layer)
    hx = right_x - 35
    hy_top = top_y + 70
    hy_bot = bot_y - 70
    hw = 150
    hh = hy_bot - hy_top
    
    # Handle Drop Shadow on background
    h_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hsdraw = ImageDraw.Draw(h_shadow)
    hsdraw.ellipse([hx + 10, hy_top + 10, hx + hw + 10, hy_bot + 10], fill=(0, 0, 0, 140))
    h_shadow = h_shadow.filter(ImageFilter.GaussianBlur(10))
    canvas = Image.alpha_composite(canvas, h_shadow)
    
    # Outer black glossy handle curve
    hdraw.ellipse([hx, hy_top, hx + hw, hy_bot], fill=(22, 23, 27), outline=(42, 44, 52), width=3)
    # Inner cutout of handle (showing table/background through it)
    # We clear the inner hole
    cut_w = hw - 65
    cut_h = hh - 60
    hdraw.ellipse([hx + 28, hy_top + 30, hx + 28 + cut_w, hy_top + 30 + cut_h], fill=(0, 0, 0, 0))
    
    # Electric Lime glazed inner curve of the handle!
    # Draw an arc on the inner edge of the handle
    hdraw.arc([hx + 26, hy_top + 28, hx + 28 + cut_w + 4, hy_top + 30 + cut_h + 4], start=70, end=290, fill=(57, 255, 20), width=4)
    # Subtle glossy specular shine on the outer handle curve
    hdraw.arc([hx + 4, hy_top + 4, hx + hw - 4, hy_bot - 4], start=290, end=70, fill=(75, 78, 88), width=3)
    
    canvas = Image.alpha_composite(canvas, handle_layer)
    
    # 5. Ceramic Mug Cylinder Body (Glossy Jet Black Ceramic)
    # Cylinder mask with slightly tapered base (typical of ceramic mugs)
    body_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(body_layer)
    
    # Tapered polygon body
    # Top ellipse y center = top_y
    # Bottom ellipse y center = bot_y
    rim_ry = 32 # vertical radius of the top rim ellipse
    bot_ry = 26
    
    # Base polygon
    b_pts = [
        (left_x, top_y),
        (right_x, top_y),
        (right_x - 12, bot_y),
        (left_x + 12, bot_y),
    ]
    bdraw.polygon(b_pts, fill=(18, 19, 23))
    # Bottom rounded base cap
    bdraw.ellipse([left_x + 12, bot_y - bot_ry, right_x - 12, bot_y + bot_ry], fill=(18, 19, 23))
    
    # 6. Realistic Ceramic Lighting & Curved Specular Reflections
    # Real glossy black ceramic has a bright vertical soft light reflection on the left (light source)
    # and deep rich black with subtle rim reflections on the right
    light_map = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(light_map)
    
    for x in range(left_x, right_x):
        norm_x = (x - left_x) / float(mug_w)
        # Specular highlight peak around norm_x = 0.22
        dist_highlight = abs(norm_x - 0.22)
        if dist_highlight < 0.28:
            spec = math.cos(dist_highlight / 0.28 * (math.pi / 2)) ** 2
            alpha = int(45 * spec)
            ldraw.line([(x, top_y), (x, bot_y)], fill=(120, 125, 140, alpha), width=1)
        
        # Soft rim light on the extreme right (from background glow)
        if norm_x > 0.88:
            rim_t = (norm_x - 0.88) / 0.12
            alpha = int(35 * rim_t)
            ldraw.line([(x, top_y), (x, bot_y)], fill=(80, 50, 110, alpha), width=1)
            
        # Left edge rim light
        if norm_x < 0.08:
            rim_l = (0.08 - norm_x) / 0.08
            alpha = int(28 * rim_l)
            ldraw.line([(x, top_y), (x, bot_y)], fill=(57, 255, 20, alpha), width=1)
            
    body_layer = Image.alpha_composite(body_layer, light_map)
    
    # 7. Artwork Projection onto Curved Ceramic Mug Face
    # We combine the smoky owl crest and the two-tone Gothic "Axiom Allegiance"
    # and map them with slight cylindrical perspective
    art_w = 340
    art_h = 320
    art_canvas = Image.new("RGBA", (art_w, art_h), (0, 0, 0, 0))
    
    # Resize owl
    o_h = 205
    o_w = int(owl_img.width * (o_h / owl_img.height))
    o_res = owl_img.resize((o_w, o_h), Image.Resampling.LANCZOS)
    art_canvas.paste(o_res, ((art_w - o_w) // 2, 8), o_res)
    
    # Resize two-tone gothic text
    g_w = 310
    g_h = int(gothic_img.height * (g_w / gothic_img.width))
    g_res = gothic_img.resize((g_w, g_h), Image.Resampling.LANCZOS)
    art_canvas.paste(g_res, ((art_w - g_w) // 2, o_h + 15), g_res)
    
    # Position artwork on the mug front face (slightly shifted left to account for cylindrical curvature)
    art_x = cx - art_w // 2 - 12
    art_y = top_y + 80
    
    # Ceramic gloss reflection over the artwork so it looks printed directly onto the high-gloss ceramic!
    gloss_overlay = Image.new("RGBA", (art_w, art_h), (0, 0, 0, 0))
    godraw = ImageDraw.Draw(gloss_overlay)
    for x in range(art_w):
        nx = x / float(art_w)
        if abs(nx - 0.28) < 0.22:
            s = math.cos(abs(nx - 0.28) / 0.22 * (math.pi / 2)) ** 2
            godraw.line([(x, 0), (x, art_h)], fill=(255, 255, 255, int(22 * s)), width=1)
            
    art_composite = Image.alpha_composite(art_canvas, gloss_overlay)
    body_layer.paste(art_composite, (art_x, art_y), art_composite)
    
    canvas = Image.alpha_composite(canvas, body_layer)
    draw = ImageDraw.Draw(canvas)
    
    # 8. Ceramic Top Rim & Vibrant Electric Lime Glazed Interior!
    # This is the defining feature: when you look into the mug, you see the rich glossy electric lime glaze!
    rim_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(rim_layer)
    
    # Outer black ceramic lip
    rdraw.ellipse([left_x, top_y - rim_ry, right_x, top_y + rim_ry], fill=(16, 17, 20), outline=(45, 48, 56), width=2)
    # Electric lime glazed rim inner edge
    lime_inner_ry = rim_ry - 5
    lime_inner_rx = mug_w // 2 - 8
    rdraw.ellipse([cx - lime_inner_rx, top_y - lime_inner_ry, cx + lime_inner_rx, top_y + lime_inner_ry], fill=(42, 175, 18), outline=(57, 255, 20), width=3)
    
    # Inside cavity depth (glaze slopes down into shadow)
    cavity_ry = rim_ry - 10
    cavity_rx = mug_w // 2 - 18
    # Gradient lime to dark in the cup interior
    for i in range(12):
        step_rx = cavity_rx - i * 3
        step_ry = cavity_ry - int(i * 1.5)
        if step_rx > 0 and step_ry > 0:
            # Shift slightly downward to simulate inner cup depth
            cy_shift = top_y + i * 2
            g_val = max(18, int(150 - i * 11))
            r_val = max(8, int(35 - i * 2.5))
            b_val = max(10, int(20 - i * 1.5))
            rdraw.ellipse([cx - step_rx, cy_shift - step_ry, cx + step_rx, cy_shift + step_ry], fill=(r_val, g_val, b_val))
            
    # Glossy ceramic rim highlight (reflection along front lip)
    rdraw.arc([left_x + 35, top_y - rim_ry + 2, right_x - 35, top_y + rim_ry - 2], start=10, end=170, fill=(200, 255, 180, 180), width=2)
    
    canvas = Image.alpha_composite(canvas, rim_layer)
    
    # 9. Clean Final Pass (Natural E-commerce Look)
    final_img = canvas.convert("RGB")
    out_path = os.path.join(PUB_PRODUCTS, out_filename)
    final_img.save(out_path, "JPEG", quality=95, progressive=True)
    print(f"Saved Photorealistic Ceramic Gamer Mug: {out_path} ({os.path.getsize(out_path)//1024} KB)")

if __name__ == "__main__":
    render_photoreal_ceramic_mug("axiom-mug-smokey-crest-15oz.png")
    render_photoreal_ceramic_mug("axiom-mug-smokey-crest-15oz.jpg")
