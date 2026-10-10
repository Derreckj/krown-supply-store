from PIL import Image, ImageFilter, ImageDraw, ImageFont
import numpy as np

# Load clean blank bottle
bottle_base = Image.open('test_clean_blank_bottle.jpg').convert('RGBA')
w, h = bottle_base.size

# Load pure 3D gold crown
crown = Image.open('test_pure_gold_crown.png').convert('RGBA')

# Load isolated whisk
whisk = Image.open('test_isolated_whisk.png').convert('RGBA')

# 1. Place 3D gold crown
# Proportions: 180px wide
target_cw = 180
caspect = crown.height / crown.width
target_ch = int(target_cw * caspect)
crown_resized = crown.resize((target_cw, target_ch), Image.Resampling.LANCZOS)

crown_x = (w - target_cw) // 2 - 8
crown_y = 360

# Drop shadow for crown onto the matte black bottle
crown_alpha = crown_resized.split()[3]
shadow_mask = crown_alpha.filter(ImageFilter.GaussianBlur(radius=4.0))
crown_shadow = Image.new('RGBA', (target_cw, target_ch), (0, 0, 0, 180))
crown_shadow.putalpha(shadow_mask)

crown_canvas = Image.new('RGBA', (w, h), (0, 0, 0, 0))
crown_canvas.paste(crown_shadow, (crown_x + 1, crown_y + 4), mask=shadow_mask)
crown_canvas.paste(crown_resized, (crown_x, crown_y), mask=crown_resized)

# 2. Add luxury gold typography
draw = ImageDraw.Draw(crown_canvas)
try:
    font_krown = ImageFont.truetype('arialbd.ttf', 30)
    font_sub = ImageFont.truetype('arial.ttf', 15)
except:
    font_krown = ImageFont.load_default()
    font_sub = ImageFont.load_default()

text_krown = "K  R  O  W  N"
text_sub = "S U P P L Y   C O ."

bbox1 = draw.textbbox((0, 0), text_krown, font=font_krown)
tw1 = bbox1[2] - bbox1[0]
tx1 = (w - tw1) // 2 - 8
ty1 = crown_y + target_ch + 18

draw.text((tx1 + 1, ty1 + 1), text_krown, fill=(10, 8, 4, 200), font=font_krown)
draw.text((tx1, ty1), text_krown, fill=(218, 182, 60, 255), font=font_krown)
draw.text((tx1, ty1 - 1), text_krown, fill=(245, 225, 140, 220), font=font_krown)

bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
tw2 = bbox2[2] - bbox2[0]
tx2 = (w - tw2) // 2 - 8
ty2 = ty1 + 38

draw.text((tx2 + 1, ty2 + 1), text_sub, fill=(10, 8, 4, 200), font=font_sub)
draw.text((tx2, ty2), text_sub, fill=(205, 175, 80, 230), font=font_sub)

result = Image.alpha_composite(bottle_base, crown_canvas)

# 3. Add isolated whisk ball onto the counter
target_ww = 165
waspect = whisk.height / whisk.width
target_wh = int(target_ww * waspect)
whisk_resized = whisk.resize((target_ww, target_wh), Image.Resampling.LANCZOS)

whisk_x = 680
whisk_y = 710

# Contact shadow on counter
shadow_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow_layer)
# Elliptical contact shadow
s_draw.ellipse([whisk_x + 10, whisk_y + target_wh - 25, whisk_x + target_ww - 10, whisk_y + target_wh + 15], fill=(8, 9, 12, 190))
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8.0))

result = Image.alpha_composite(result, shadow_layer)
result.paste(whisk_resized, (whisk_x, whisk_y), mask=whisk_resized.split()[3])

final_rgb = result.convert('RGB')
final_rgb.save('test_krown_luxury_shaker_final.jpg', quality=96)
print("Saved test_krown_luxury_shaker_final.jpg")
