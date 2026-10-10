from PIL import Image, ImageFilter
import numpy as np

# Load the master 1024x1024 tumbler
base_img = Image.open('public/images/products/krown-construction-jobsite-tumbler.png').convert('RGB')
w, h = base_img.size

# Load pure 3D gold crown
crown = Image.open('test_pure_gold_crown.png').convert('RGBA')

# Load whisk ball
whisk = Image.open('test_whisk_crop3.jpg').convert('RGB')

# Let's clean the bottle surface:
# The KC logo is in region: x: 340 to 650, y: 310 to 590
# The bottle powder-coat has a horizontal profile: darker at x=340 (~25), brighter at x=500 (~45-55), darker at x=650 (~25)
# We can sample the vertical slices from above (y=280..305) and below (y=610..635)
base_np = np.array(base_img, dtype=np.float32)

# Interpolate clean bottle texture over the logo region
y_top_clean = base_np[285:305, :, :]
y_bot_clean = base_np[615:635, :, :]

# Average clean strips vertically
top_prof = np.mean(y_top_clean, axis=0) # shape (1024, 3)
bot_prof = np.mean(y_bot_clean, axis=0) # shape (1024, 3)

# For y between 310 and 595, and x between 345 and 645:
# Linear vertical blend between top_prof and bot_prof + slight noise to match matte powder coat grain
np.random.seed(42)
for y_idx in range(310, 595):
    t = (y_idx - 310) / (595 - 310)
    blended_prof = (1.0 - t) * top_prof + t * bot_prof
    noise = np.random.normal(0, 1.5, size=(1024, 3))
    clean_row = np.clip(blended_prof + noise, 0, 255)
    
    for x_idx in range(345, 645):
        # Blend edge smoothly into existing bottle pixels
        edge_dist = min(x_idx - 345, 645 - x_idx, y_idx - 310, 595 - y_idx)
        alpha_blend = min(1.0, edge_dist / 12.0)
        base_np[y_idx, x_idx] = (1.0 - alpha_blend) * base_np[y_idx, x_idx] + alpha_blend * clean_row[x_idx]

clean_bottle_img = Image.fromarray(base_np.astype(np.uint8), mode='RGB')

# Add 3D metallic gold KrowN crown
# Crown dimensions on the bottle
target_cw = 175
caspect = crown.height / crown.width
target_ch = int(target_cw * caspect)
crown_resized = crown.resize((target_cw, target_ch), Image.Resampling.LANCZOS)

# Position crown on center of the bottle (x around 495, y around 380)
crown_x = (w - target_cw) // 2 - 8
crown_y = 380

# Clean gold text: K R O W N / SUPPLY CO.
from PIL import ImageDraw, ImageFont
try:
    font_krown = ImageFont.truetype('arialbd.ttf', 32)
    font_sub = ImageFont.truetype('arial.ttf', 16)
except:
    font_krown = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# Overlay crown
clean_bottle_rgba = clean_bottle_img.convert('RGBA')

# Contact shadow for the crown onto the powder-coat
crown_alpha = crown_resized.split()[3]
shadow_mask = crown_alpha.filter(ImageFilter.GaussianBlur(radius=4.0))
crown_shadow = Image.new('RGBA', (target_cw, target_ch), (0, 0, 0, 160))
crown_shadow.putalpha(shadow_mask)

crown_canvas = Image.new('RGBA', (w, h), (0, 0, 0, 0))
crown_canvas.paste(crown_shadow, (crown_x + 1, crown_y + 3), mask=shadow_mask)
crown_canvas.paste(crown_resized, (crown_x, crown_y), mask=crown_resized)

draw = ImageDraw.Draw(crown_canvas)
text_gold = (212, 175, 55, 240)
gold_specular = (245, 225, 130, 255)

# Text positioning
text_krown = "K  R  O  W  N"
text_sub = "S U P P L Y   C O ."

bbox1 = draw.textbbox((0, 0), text_krown, font=font_krown)
tw1 = bbox1[2] - bbox1[0]
tx1 = (w - tw1) // 2 - 8
ty1 = crown_y + target_ch + 20

# Draw subtle metallic bevel on text
draw.text((tx1 + 1, ty1 + 1), text_krown, fill=(20, 15, 5, 180), font=font_krown)
draw.text((tx1, ty1), text_krown, fill=text_gold, font=font_krown)
draw.text((tx1, ty1 - 1), text_krown, fill=gold_specular, font=font_krown)

bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
tw2 = bbox2[2] - bbox2[0]
tx2 = (w - tw2) // 2 - 8
ty2 = ty1 + 42

draw.text((tx2 + 1, ty2 + 1), text_sub, fill=(20, 15, 5, 180), font=font_sub)
draw.text((tx2, ty2), text_sub, fill=(225, 195, 100, 220), font=font_sub)

result = Image.alpha_composite(clean_bottle_rgba, crown_canvas)

# Now composite the surgical steel wire whisk ball onto the counter
# Position: right of the bottle, on the table (x around 660, y around 700)
# Whisk dimensions
ww, wh = whisk.size
target_ww = 160
target_wh = int(target_ww * wh / ww)
whisk_resized = whisk.resize((target_ww, target_wh), Image.Resampling.LANCZOS)
whisk_np = np.array(whisk_resized, dtype=np.float32)

# Create mask for whisk wires:
# The whisk background in test_whisk_crop3.jpg is dark desk (R,G,B < 35)
# Stainless steel wires have metallic highlights (R,G,B > 65)
wire_brightness = np.maximum.reduce([whisk_np[:, :, 0], whisk_np[:, :, 1], whisk_np[:, :, 2]])
whisk_alpha = np.clip((wire_brightness - 32) / 28.0 * 255.0, 0, 255).astype(np.uint8)
whisk_alpha_img = Image.fromarray(whisk_alpha, mode='L')
whisk_rgba = whisk_resized.convert('RGBA')
whisk_rgba.putalpha(whisk_alpha_img)

# Contact shadow for the whisk ball
whisk_shadow = Image.new('RGBA', (target_ww, target_wh), (10, 10, 12, 180))
whisk_shadow_mask = whisk_alpha_img.filter(ImageFilter.GaussianBlur(radius=5.0))
whisk_shadow.putalpha(whisk_shadow_mask)

whisk_x = 675
whisk_y = 710

result.paste(whisk_shadow, (whisk_x - 3, whisk_y + 8), mask=whisk_shadow_mask)
result.paste(whisk_rgba, (whisk_x, whisk_y), mask=whisk_alpha_img)

final_img = result.convert('RGB')
final_img.save('test_luxury_krown_shaker.jpg', quality=95)
print("Saved test_luxury_krown_shaker.jpg successfully!")
