from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

prod_dir = 'public/images/products'

# 1. Fix axiom-shaker-bottles-4-editions.jpg prices at bottom
im4 = Image.open(os.path.join(prod_dir, 'axiom-shaker-bottles-4-editions.jpg')).convert('RGB')
w4, h4 = im4.size # 1600, 1000

draw4 = ImageDraw.Draw(im4)
try:
    font_price = ImageFont.truetype('impact.ttf', 38)
except:
    try:
        font_price = ImageFont.truetype('arialbd.ttf', 34)
    except:
        font_price = ImageFont.load_default()

# Erase the cutoff ".99" text at the bottom: y ~ 900 to 960
draw4.rectangle([0, 890, w4, 970], fill=(0, 0, 0))

# Correct prices matching variants:
# Column 1 (Signature Tritan 24oz): $24.99 (center ~ 200)
# Column 2 (Signature Pro Steel 26oz): $34.99 (center ~ 600)
# Column 3 (Stealth Tritan 24oz): $24.99 (center ~ 1000)
# Column 4 (Stealth Pro Steel 26oz): $34.99 (center ~ 1400)

prices = ["$24.99", "$34.99", "$24.99", "$34.99"]
centers = [200, 600, 1000, 1400]

for p_text, cx in zip(prices, centers):
    bbox = draw4.textbbox((0, 0), p_text, font=font_price)
    pw = bbox[2] - bbox[0]
    draw4.text((cx - pw // 2, 905), p_text, fill=(255, 255, 255), font=font_price)

im4.save(os.path.join(prod_dir, 'axiom-shaker-bottles-4-editions.jpg'), quality=96)
print("Fixed axiom-shaker-bottles-4-editions.jpg with correct prices!")

# 2. Fix axiom-shaker-bottles-3-editions.jpg
# Replace "POWERED BY KROWN" with "POWERED BY AXIOM" and clean the collar
im3 = Image.open(os.path.join(prod_dir, 'axiom-shaker-bottles-3-editions.jpg')).convert('RGB')
w3, h3 = im3.size # 1600, 1000
draw3 = ImageDraw.Draw(im3)

try:
    font_bold = ImageFont.truetype('arialbd.ttf', 24)
    font_sub = ImageFont.truetype('arial.ttf', 14)
except:
    font_bold = ImageFont.load_default()
    font_sub = ImageFont.load_default()

# Bottle 1 (left): center x ~ 265, "POWERED BY KROWN" is around y: 645 to 685
# Bottle 3 (right): center x ~ 1335, "POWERED BY KROWN" is around y: 645 to 685

# Inpaint Bottle 1 text area:
arr3 = np.array(im3, dtype=np.float32)
# Sample dark frosted smoke background around x: 200..330, y: 640..695
for y in range(645, 690):
    for x in range(195, 335):
        # Matte smoke bottle color is around (18, 20, 22)
        arr3[y, x] = [18, 20, 22]

# Bottle 3 (steel): x: 1265..1405, y: 645..690
# Sample brushed steel texture from just above (y=635)
steel_row = np.array(arr3[635, 1265:1405, :])
for y in range(645, 690):
    for x in range(1265, 1405):
        arr3[y, x] = arr3[635, x]

# Collar inpainting on Bottle 1 (x: 230..300, y: 235..260): clean purple silicone
for y in range(238, 258):
    for x in range(230, 305):
        arr3[y, x] = arr3[232, x]

# Collar inpainting on Bottle 3 (x: 1300..1375, y: 235..260)
for y in range(238, 258):
    for x in range(1300, 1375):
        arr3[y, x] = arr3[232, x]

im3_cleaned = Image.fromarray(arr3.astype(np.uint8), mode='RGB')
draw3_clean = ImageDraw.Draw(im3_cleaned)

# Draw clean "POWERED BY AXIOM" on Bottle 1
bbox1 = draw3_clean.textbbox((0, 0), "POWERED BY", font=font_sub)
w_sub1 = bbox1[2] - bbox1[0]
draw3_clean.text((265 - w_sub1 // 2, 650), "POWERED BY", fill=(160, 165, 175), font=font_sub)

bbox1_ax = draw3_clean.textbbox((0, 0), "AXIOM", font=font_bold)
w_ax1 = bbox1_ax[2] - bbox1_ax[0]
draw3_clean.text((265 - w_ax1 // 2, 665), "AXIOM", fill=(255, 255, 255), font=font_bold)

# Draw clean "POWERED BY AXIOM" on Bottle 3
bbox3 = draw3_clean.textbbox((0, 0), "POWERED BY", font=font_sub)
w_sub3 = bbox3[2] - bbox3[0]
draw3_clean.text((1335 - w_sub3 // 2, 650), "POWERED BY", fill=(120, 125, 135), font=font_sub)

bbox3_ax = draw3_clean.textbbox((0, 0), "AXIOM", font=font_bold)
w_ax3 = bbox3_ax[2] - bbox3_ax[0]
draw3_clean.text((1335 - w_ax3 // 2, 665), "AXIOM", fill=(45, 48, 55), font=font_bold)

im3_cleaned.save(os.path.join(prod_dir, 'axiom-shaker-bottles-3-editions.jpg'), quality=96)
print("Fixed axiom-shaker-bottles-3-editions.jpg with clean AXIOM branding!")
