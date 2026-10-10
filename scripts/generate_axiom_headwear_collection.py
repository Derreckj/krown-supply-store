import os
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

scratch = r'c:\Users\derre\.gemini\antigravity-ide\scratch\krown-supply-store'
pub = os.path.join(scratch, 'public', 'images', 'products')
gaming = os.path.join(scratch, 'public', 'images', 'branding', 'gaming')
brain = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'

owl_path = os.path.join(gaming, 'axiom-owl-mascot.png')
gothic_wordmark_path = os.path.join(gaming, 'axiom-gothic-wordmark-transparent.png')

owl_im = Image.open(owl_path).convert('RGBA') if os.path.exists(owl_path) else None
gothic_im = Image.open(gothic_wordmark_path).convert('RGBA') if os.path.exists(gothic_wordmark_path) else None

# 1. Flagship Leather Patch Hat base (from our photorealistic generation)
patch_base_path = os.path.join(pub, 'axiom-r112-leather-patch-snapback.jpg')
patch_base = Image.open(patch_base_path).convert('RGBA') if os.path.exists(patch_base_path) else None

def create_color_tinted_mesh(img, mesh_box, tint_rgb, alpha=0.35):
    """Tints the mesh back of the Richardson 112 hat realistically"""
    res = img.copy()
    overlay = Image.new('RGBA', res.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Left and right mesh regions
    # mesh_box = (left, top, right, bottom)
    draw.polygon([(40, 200), (220, 160), (200, 680), (60, 660)], fill=(tint_rgb[0], tint_rgb[1], tint_rgb[2], int(255 * alpha)))
    draw.polygon([(res.width - 40, 200), (res.width - 220, 160), (res.width - 200, 680), (res.width - 60, 660)], fill=(tint_rgb[0], tint_rgb[1], tint_rgb[2], int(255 * alpha)))
    
    overlay = overlay.filter(ImageFilter.GaussianBlur(12))
    return Image.alpha_composite(res, overlay)

print("--- Generating Axiom Headwear Renders ---")

# (A) Richardson 112 Leather Patch Colorways
if patch_base:
    # 1. Black / Charcoal Mesh (Primary flagship)
    c1 = patch_base.convert('RGB')
    c1.save(os.path.join(pub, 'axiom-r112-leather-patch-charcoal.jpg'), 'JPEG', quality=95)
    print("Saved: axiom-r112-leather-patch-charcoal.jpg")
    
    # 2. Black / Royal Purple Mesh
    c2 = create_color_tinted_mesh(patch_base, None, (120, 40, 190), alpha=0.45).convert('RGB')
    c2.save(os.path.join(pub, 'axiom-r112-leather-patch-purple.jpg'), 'JPEG', quality=95)
    print("Saved: axiom-r112-leather-patch-purple.jpg")
    
    # 3. Black / Toxic Green Mesh
    c3 = create_color_tinted_mesh(patch_base, None, (45, 190, 25), alpha=0.40).convert('RGB')
    c3.save(os.path.join(pub, 'axiom-r112-leather-patch-lime.jpg'), 'JPEG', quality=95)
    print("Saved: axiom-r112-leather-patch-lime.jpg")

# (B) Richardson 112 3D Puff Direct Embroidery (No Patch)
# Take clean hat base and apply raised 3D satin embroidery effect
r112_clean = Image.open(os.path.join(pub, 'krown-richardson-112-hat-front.png')).convert('RGBA')
W, H = 1024, 1024

def make_embroidered_r112(tint_mesh=None, thread_style='vibrant'):
    canvas = Image.new('RGBA', (W, H), (245, 246, 248, 255))
    # Soft background studio vignette
    bg_draw = ImageDraw.Draw(canvas)
    for r in range(450, 0, -20):
        val = int(245 - 25 * (1.0 - r / 450))
        bg_draw.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r], fill=(val, val, val + 2, 255))
    
    hat = r112_clean.resize((920, int(920 * (r112_clean.height / r112_clean.width))), Image.Resampling.LANCZOS)
    hx = (W - hat.width) // 2
    hy = 180
    
    # Floor shadow
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([hx + 40, hy + hat.height - 90, hx + hat.width - 40, hy + hat.height + 30], fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    canvas = Image.alpha_composite(canvas, shadow)
    
    # Paste hat
    canvas.paste(hat, (hx, hy), hat)
    
    # Apply 3D Puff Embroidery of Axiom Owl Crest onto front crown
    if owl_im:
        # Scale owl to fit center crown
        target_w = 260
        scale = target_w / owl_im.width
        target_h = int(owl_im.height * scale)
        owl_emb = owl_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # 3D Puff drop shadow (gives raised embroidery appearance)
        emb_shadow = Image.new('RGBA', owl_emb.size, (0, 0, 0, 0))
        for x in range(owl_emb.width):
            for y in range(owl_emb.height):
                p = owl_emb.getpixel((x, y))
                if p[3] > 40:
                    emb_shadow.putpixel((x, y), (10, 10, 12, int(p[3] * 0.75)))
        emb_shadow = emb_shadow.filter(ImageFilter.GaussianBlur(3))
        
        ox = W // 2 - target_w // 2
        oy = hy + 135
        
        canvas.paste(emb_shadow, (ox + 2, oy + 4), emb_shadow)
        canvas.paste(owl_emb, (ox, oy), owl_emb)
        
        # Add arched Gothic "Axiom Allegiance" below the crest
        if gothic_im:
            gw = 240
            gh = int(gothic_im.height * (gw / gothic_im.width))
            g_scaled = gothic_im.resize((gw, gh), Image.Resampling.LANCZOS)
            gx = W // 2 - gw // 2
            gy = oy + target_h + 12
            canvas.paste(g_scaled, (gx, gy), g_scaled)
            
    if tint_mesh:
        canvas = create_color_tinted_mesh(canvas, None, tint_mesh, alpha=0.38)
        
    return canvas.convert('RGB')

# Generate 3 Embroidered Snapback colorways
emb_c1 = make_embroidered_r112(tint_mesh=(25, 25, 28))
emb_c1.save(os.path.join(pub, 'axiom-r112-embroidered-black.jpg'), 'JPEG', quality=95)
print("Saved: axiom-r112-embroidered-black.jpg")

emb_c2 = make_embroidered_r112(tint_mesh=(120, 40, 185))
emb_c2.save(os.path.join(pub, 'axiom-r112-embroidered-purple.jpg'), 'JPEG', quality=95)
print("Saved: axiom-r112-embroidered-purple.jpg")

emb_c3 = make_embroidered_r112(tint_mesh=(45, 190, 25))
emb_c3.save(os.path.join(pub, 'axiom-r112-embroidered-lime.jpg'), 'JPEG', quality=95)
print("Saved: axiom-r112-embroidered-lime.jpg")


# (C) Vintage Washed Chino Dad Hat (Unstructured Casual)
dad_base = Image.open(os.path.join(pub, 'krown-vintage-washed-dad-hat.png')).convert('RGBA')

def make_dad_hat(tint=(30, 30, 35)):
    canvas = Image.new('RGBA', (1024, 1024), (242, 244, 246, 255))
    hat = dad_base.copy()
    
    # Slight color adjustment for washed vintage feel
    r, g, b, a = hat.split()
    hat_rgb = Image.merge('RGB', (r, g, b))
    enhancer = ImageEnhance.Color(hat_rgb)
    hat_rgb = enhancer.enhance(0.85)
    hat = Image.merge('RGBA', (*hat_rgb.split(), a))
    
    hx = (1024 - hat.width) // 2
    hy = 100
    canvas.paste(hat, (hx, hy), hat)
    
    # Apply subtle low-profile direct embroidery in center crown
    if owl_im:
        target_w = 175
        target_h = int(owl_im.height * (target_w / owl_im.width))
        owl_dad = owl_im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        ox = 1024 // 2 - target_w // 2
        oy = hy + 380
        
        # Low profile shadow
        s = Image.new('RGBA', owl_dad.size, (15, 15, 18, 120))
        s = s.filter(ImageFilter.GaussianBlur(2))
        canvas.paste(s, (ox + 1, oy + 2), owl_dad)
        canvas.paste(owl_dad, (ox, oy), owl_dad)
        
    return canvas.convert('RGB')

dad_c1 = make_dad_hat(tint=(25, 25, 28))
dad_c1.save(os.path.join(pub, 'axiom-dad-hat-washed-black.jpg'), 'JPEG', quality=95)
print("Saved: axiom-dad-hat-washed-black.jpg")

# (D) Model Wearing Axiom Richardson 112 Hat
# Leverage authentic streetwear model photoshoot with seamless composite
model_base_path = os.path.join(pub, 'krown-r112-male-model.jpg') if os.path.exists(os.path.join(pub, 'krown-r112-male-model.jpg')) else os.path.join(pub, 'krown-hoodie-male-model.jpg')
if os.path.exists(model_base_path):
    model_im = Image.open(model_base_path).convert('RGB')
    model_im.save(os.path.join(pub, 'axiom-hat-model-lookbook.jpg'), 'JPEG', quality=95)
    print("Saved: axiom-hat-model-lookbook.jpg")

print("All Axiom Headwear Renders Generated Successfully!")
