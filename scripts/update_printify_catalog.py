import re

file_path = "src/services/printify.ts"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. krown-streetwear-set images & variants
content = content.replace(
    "    images: [\n      '/images/products/krown-streetwear-set-black.jpg',",
    "    images: [\n      '/images/products/krown-streetwear-set-v2.jpg',"
)

# 2. custom-krown-works-hat images order
old_hat_imgs = """    images: [
      '/images/products/krown-r112-leather-patch-charcoal-black.jpg',
      '/images/products/krown-r112-leather-patch-heather-grey.jpg',
      '/images/products/krown-r112-leather-patch-obsidian-black.jpg',
      '/images/products/krown-r112-flagship-leather-patch-snapback.jpg',
      '/images/products/krown-r112-flagship-leather-patch-hero.jpg',
    ],"""
new_hat_imgs = """    images: [
      '/images/products/krown-r112-leather-patch-heather-grey.jpg',
      '/images/products/krown-r112-leather-patch-obsidian-black.jpg',
      '/images/products/krown-r112-leather-patch-charcoal-black.jpg',
      '/images/products/krown-r112-flagship-leather-patch-snapback.jpg',
      '/images/products/krown-r112-flagship-leather-patch-hero.jpg',
    ],"""
content = content.replace(old_hat_imgs, new_hat_imgs)

# 3. krown-shorts-01 images
content = content.replace(
    "    images: [\n      '/images/products/krown-french-terry-shorts.jpg',\n    ],",
    "    images: [\n      '/images/products/krown-french-terry-shorts-v2.jpg',\n    ],"
)

# 4. krown-shaker-01 primary image & variant
content = content.replace(
    "      '/images/products/krown-shaker-obsidian-steel.jpg',",
    "      '/images/products/krown-shaker-obsidian-steel-v2.jpg',"
)

# 5. kc-beanie-01 images
content = content.replace(
    "    images: [\n      '/images/products/krown-construction-cuffed-beanie.png',",
    "    images: [\n      '/images/products/krown-beanie-since-2018.jpg',"
)

# 6. kc-shaker-01 primary image & variant
content = content.replace(
    "      '/images/products/kc-shaker-highvis-steel.jpg',",
    "      '/images/products/kc-shaker-highvis-steel-v2.jpg',"
)

# 7. axiom-mug-01 image
content = content.replace(
    "    id: 'axiom-mug-01',\n    name: 'Axiom Owl Two-Tone Ceramic Gaming Mug (15oz)',\n    slug: 'axiom-owl-two-tone-gaming-mug-15oz',\n    description: 'Fuel your late-night ranked grinds. Heavyweight 15oz ceramic mug boasting a midnight obsidian exterior paired with vibrant electric lime interior glaze and handle. Features the 3D Axiom Owl esports crest on the front and the official motto inscribed on the reverse: \"YOU CANNOT BE TRULY HUMBLE, UNLESS YOU TRULY BELIEVE THAT LIFE CAN AND WILL GO ON WITHOUT YOU\". Microwave and dishwasher safe.',\n    collection: 'AXA / Axiom Allegiance',\n    price: 19.99,\n    baseCost: 5.80,\n    printCost: 4.20,\n    images: [\n      '/images/products/axiom-mug-smokey-crest-15oz.png',\n    ],",
    "    id: 'axiom-mug-01',\n    name: 'Axiom Owl Two-Tone Ceramic Gaming Mug (15oz)',\n    slug: 'axiom-owl-two-tone-gaming-mug-15oz',\n    description: 'Fuel your late-night ranked grinds. Heavyweight 15oz ceramic mug boasting a midnight obsidian exterior paired with vibrant electric lime interior glaze and handle. Features the 3D Axiom Owl esports crest on the front and the official motto inscribed on the reverse: \"YOU CANNOT BE TRULY HUMBLE, UNLESS YOU TRULY BELIEVE THAT LIFE CAN AND WILL GO ON WITHOUT YOU\". Microwave and dishwasher safe.',\n    collection: 'AXA / Axiom Allegiance',\n    price: 19.99,\n    baseCost: 5.80,\n    printCost: 4.20,\n    images: [\n      '/images/products/axiom-mug-clean-photoreal-15oz.jpg',\n    ],"
)

# 8. Remove axiom-mug-02 completely
mug_02_pattern = re.compile(r'  \{\s*id:\s*\'axiom-mug-02\'.*?\n  \},\n', re.DOTALL)
content = mug_02_pattern.sub('', content)

# 9. axiom-dad-hat-01 images
old_dad_hat = """  {
    id: 'axiom-dad-hat-01',
    name: 'Axiom Allegiance Vintage Washed Chino Dad Hat',
    slug: 'axiom-allegiance-vintage-washed-dad-hat',
    description: 'Relaxed, low-profile unstructured 6-panel dad hat cut from 100% garment-washed cotton chino twill. Features low-profile direct embroidery of the official Axiom Owl mascot and Gothic wordmark, matching fabric strap with brass buckle slider, and pre-curved bill. Everyday comfort meets high-tier esports styling.',
    collection: 'AXA / Axiom Allegiance',
    price: 24.99,
    baseCost: 9.00,
    printCost: 3.50,
    images: [
      '/images/products/axiom-dad-hat-washed-black.jpg',
      '/images/products/axiom-headwear-collection-showcase.jpg',
      '/images/products/axiom-hat-model-lookbook.jpg',
    ],
    variants: [
      { id: 5301, color: 'Vintage Washed Black', size: 'One Size (Adjustable Brass Slider)', price: 24.99, sku: 'AXM-DAD-WSH-BLK', isAvailable: true },
      { id: 5302, color: 'Midnight Dark Purple', size: 'One Size (Adjustable Brass Slider)', price: 24.99, sku: 'AXM-DAD-WSH-PRP', isAvailable: true },
      { id: 5303, color: 'Dark Charcoal Slate', size: 'One Size (Adjustable Brass Slider)', price: 24.99, sku: 'AXM-DAD-WSH-CHR', isAvailable: true },
    ],"""

new_dad_hat = """  {
    id: 'axiom-dad-hat-01',
    name: 'Axiom Allegiance Vintage Washed Chino Dad Hat',
    slug: 'axiom-allegiance-vintage-washed-dad-hat',
    description: 'Relaxed, low-profile unstructured 6-panel dad hat cut from 100% garment-washed cotton chino twill. Features low-profile direct embroidery of the official Axiom Owl mascot (clean, zero crown) and Gothic wordmark, matching fabric strap with brass buckle slider, and pre-curved bill. Everyday comfort meets high-tier esports styling.',
    collection: 'AXA / Axiom Allegiance',
    price: 24.99,
    baseCost: 9.00,
    printCost: 3.50,
    images: [
      '/images/products/axiom-dad-hat-washed-black-v2.jpg',
      '/images/products/axiom-hat-model-lookbook-v2.jpg',
      '/images/products/axiom-headwear-collection-showcase.jpg',
    ],
    variants: [
      { id: 5301, color: 'Vintage Washed Black', size: 'One Size (Adjustable Brass Slider)', price: 24.99, sku: 'AXM-DAD-WSH-BLK', isAvailable: true, image: '/images/products/axiom-dad-hat-washed-black-v2.jpg' },
      { id: 5302, color: 'Midnight Dark Purple', size: 'One Size (Adjustable Brass Slider)', price: 24.99, sku: 'AXM-DAD-WSH-PRP', isAvailable: true, image: '/images/products/axiom-dad-hat-washed-black-v2.jpg' },
      { id: 5303, color: 'Dark Charcoal Slate', size: 'One Size (Adjustable Brass Slider)', price: 24.99, sku: 'AXM-DAD-WSH-CHR', isAvailable: true, image: '/images/products/axiom-dad-hat-washed-black-v2.jpg' },
    ],"""
content = content.replace(old_dad_hat, new_dad_hat)

# 10. krown-mat-01 variant image linking
old_mat_vars = """    variants: [
      // Option 1: Volcanic Obsidian Battlestation
      { id: 3101, color: 'Volcanic Obsidian Battlestation', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-MAT-VOL-360', isAvailable: true },
      { id: 3102, color: 'Volcanic Obsidian Battlestation', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-MAT-VOL-450', isAvailable: true },
      { id: 3103, color: 'Volcanic Obsidian Battlestation', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-MAT-VOL-800', isAvailable: true },
      { id: 3104, color: 'Volcanic Obsidian Battlestation', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-MAT-VOL-900', isAvailable: true },
      { id: 3105, color: 'Volcanic Obsidian Battlestation', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-MAT-VOL-1200', isAvailable: true },

      // Option 2: Official Axiom Banner
      { id: 3111, color: 'Official Axiom Banner', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-MAT-BAN-360', isAvailable: true },
      { id: 3112, color: 'Official Axiom Banner', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-MAT-BAN-450', isAvailable: true },
      { id: 3113, color: 'Official Axiom Banner', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-MAT-BAN-800', isAvailable: true },
      { id: 3114, color: 'Official Axiom Banner', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-MAT-BAN-900', isAvailable: true },
      { id: 3115, color: 'Official Axiom Banner', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-MAT-BAN-1200', isAvailable: true },
    ],"""

new_mat_vars = """    variants: [
      // Option 1: Volcanic Obsidian Battlestation
      { id: 3101, color: 'Volcanic Obsidian Battlestation', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-MAT-VOL-360', isAvailable: true, image: '/images/products/axiom-owl-desk-mat-photorealistic.jpg' },
      { id: 3102, color: 'Volcanic Obsidian Battlestation', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-MAT-VOL-450', isAvailable: true, image: '/images/products/axiom-owl-desk-mat-photorealistic.jpg' },
      { id: 3103, color: 'Volcanic Obsidian Battlestation', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-MAT-VOL-800', isAvailable: true, image: '/images/products/axiom-owl-desk-mat-photorealistic.jpg' },
      { id: 3104, color: 'Volcanic Obsidian Battlestation', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-MAT-VOL-900', isAvailable: true, image: '/images/products/axiom-owl-desk-mat-photorealistic.jpg' },
      { id: 3105, color: 'Volcanic Obsidian Battlestation', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-MAT-VOL-1200', isAvailable: true, image: '/images/products/axiom-owl-desk-mat-photorealistic.jpg' },

      // Option 2: Official Axiom Banner
      { id: 3111, color: 'Official Axiom Banner', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-MAT-BAN-360', isAvailable: true, image: '/images/products/axiom-owl-realistic-axa-face-desk-mat.jpg' },
      { id: 3112, color: 'Official Axiom Banner', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-MAT-BAN-450', isAvailable: true, image: '/images/products/axiom-owl-realistic-axa-face-desk-mat.jpg' },
      { id: 3113, color: 'Official Axiom Banner', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-MAT-BAN-800', isAvailable: true, image: '/images/products/axiom-owl-realistic-axa-face-desk-mat.jpg' },
      { id: 3114, color: 'Official Axiom Banner', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-MAT-BAN-900', isAvailable: true, image: '/images/products/axiom-owl-realistic-axa-face-desk-mat.jpg' },
      { id: 3115, color: 'Official Axiom Banner', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-MAT-BAN-1200', isAvailable: true, image: '/images/products/axiom-owl-realistic-axa-face-desk-mat.jpg' },
    ],"""
content = content.replace(old_mat_vars, new_mat_vars)

# 11. Remove krown-mousepad-01 completely
mousepad_pattern = re.compile(r'  \{\s*id:\s*\'krown-mousepad-01\'.*?\n  \},\n', re.DOTALL)
content = mousepad_pattern.sub('', content)

# 12. axiom-sweatpants-pro images & variants
old_joggers = """    images: [
      '/images/products/axiom-sweatpants-pro-model-clean.jpg',
      '/images/products/axiom-sweatpants-pro-heavyweight-studio.jpg',
    ],
    variants: [
      { id: 4101, color: 'Obsidian Black / Purple & Green Cords', size: 'S', price: 68.00, sku: 'AXM-SWP-PRO-S', isAvailable: true },
      { id: 4102, color: 'Obsidian Black / Purple & Green Cords', size: 'M', price: 68.00, sku: 'AXM-SWP-PRO-M', isAvailable: true },
      { id: 4103, color: 'Obsidian Black / Purple & Green Cords', size: 'L', price: 68.00, sku: 'AXM-SWP-PRO-L', isAvailable: true },
      { id: 4104, color: 'Obsidian Black / Purple & Green Cords', size: 'XL', price: 68.00, sku: 'AXM-SWP-PRO-XL', isAvailable: true },
      { id: 4105, color: 'Obsidian Black / Purple & Green Cords', size: '2XL', price: 68.00, sku: 'AXM-SWP-PRO-2XL', isAvailable: true },
      { id: 4106, color: 'Obsidian Black / Purple & Green Cords', size: '3XL', price: 74.00, sku: 'AXM-SWP-PRO-3XL', isAvailable: true },
    ],"""

new_joggers = """    images: [
      '/images/products/axiom-sweatpants-pro-model-v2.jpg',
      '/images/products/axiom-sweatpants-pro-heavyweight-studio.jpg',
    ],
    variants: [
      { id: 4101, color: 'Obsidian Black / Purple & Green Cords', size: 'S', price: 68.00, sku: 'AXM-SWP-PRO-S', isAvailable: true, image: '/images/products/axiom-sweatpants-pro-model-v2.jpg' },
      { id: 4102, color: 'Obsidian Black / Purple & Green Cords', size: 'M', price: 68.00, sku: 'AXM-SWP-PRO-M', isAvailable: true, image: '/images/products/axiom-sweatpants-pro-model-v2.jpg' },
      { id: 4103, color: 'Obsidian Black / Purple & Green Cords', size: 'L', price: 68.00, sku: 'AXM-SWP-PRO-L', isAvailable: true, image: '/images/products/axiom-sweatpants-pro-model-v2.jpg' },
      { id: 4104, color: 'Obsidian Black / Purple & Green Cords', size: 'XL', price: 68.00, sku: 'AXM-SWP-PRO-XL', isAvailable: true, image: '/images/products/axiom-sweatpants-pro-model-v2.jpg' },
      { id: 4105, color: 'Obsidian Black / Purple & Green Cords', size: '2XL', price: 68.00, sku: 'AXM-SWP-PRO-2XL', isAvailable: true, image: '/images/products/axiom-sweatpants-pro-model-v2.jpg' },
      { id: 4106, color: 'Obsidian Black / Purple & Green Cords', size: '3XL', price: 74.00, sku: 'AXM-SWP-PRO-3XL', isAvailable: true, image: '/images/products/axiom-sweatpants-pro-model-v2.jpg' },
    ],"""
content = content.replace(old_joggers, new_joggers)

# 13. Remove krown-tee-01 completely
tee_pattern = re.compile(r'  \{\s*id:\s*\'krown-tee-01\'.*?\n  \},\n', re.DOTALL)
content = tee_pattern.sub('', content)

# 14. Also clean up any mock map entries for removed products
content = re.sub(r'  \'krown-mousepad-01\':\s*\{.*?\},\n', '', content, flags=re.DOTALL)
content = re.sub(r'  \'axiom-mug-02\':\s*\{.*?\},\n', '', content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("printify.ts successfully updated!")
