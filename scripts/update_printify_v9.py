import os
import re

printify_path = 'src/services/printify.ts'
with open(printify_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Beanie category fix
# Change collection from 'KrowN Construction' to 'KrowN Supply Co.'
text = re.sub(
    r"(id:\s*'kc-beanie-01',.*?collection:\s*)'KrowN Construction'",
    r"\1'KrowN Supply Co.'",
    text,
    flags=re.DOTALL
)

# 2. kc-shaker-01 update to v9
text = text.replace('/images/products/kc-shaker-photoreal-v8.jpg', '/images/products/kc-shaker-photoreal-v9.jpg')
text = text.replace('/images/products/kc-shaker-steelcore-v8.jpg', '/images/products/kc-shaker-steelcore-v9.jpg')
text = text.replace('/images/products/kc-shaker-tradesman-v8.jpg', '/images/products/kc-shaker-tradesman-v9.jpg')

# 3. krown-mat-01 desk mat
# Replace desk mat images and variants
mat_pattern = re.compile(r"(\s*id:\s*'krown-mat-01',.*?)images:\s*\[.*?\](.*?)variants:\s*\[.*?\]", re.DOTALL)

new_mat_images = """images: [
      '/images/products/axiom-mat-original-banner-v9.jpg',
      '/images/products/axiom-mat-volcanic-flame-v9.jpg',
      '/images/products/axiom-mat-cyber-neon-v9.jpg',
      '/images/products/axiom-mat-original-banner-flat-v9.jpg',
    ]"""

new_mat_variants = """variants: [
      // Option 1: Official Axiom Banner (Green & Purple Flame)
      { id: 3101, color: 'Official Axiom Banner (Green & Purple Flame)', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-MAT-BAN-360', isAvailable: true, image: '/images/products/axiom-mat-original-banner-v9.jpg' },
      { id: 3102, color: 'Official Axiom Banner (Green & Purple Flame)', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-MAT-BAN-450', isAvailable: true, image: '/images/products/axiom-mat-original-banner-v9.jpg' },
      { id: 3103, color: 'Official Axiom Banner (Green & Purple Flame)', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-MAT-BAN-800', isAvailable: true, image: '/images/products/axiom-mat-original-banner-v9.jpg' },
      { id: 3104, color: 'Official Axiom Banner (Green & Purple Flame)', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-MAT-BAN-900', isAvailable: true, image: '/images/products/axiom-mat-original-banner-v9.jpg' },
      { id: 3105, color: 'Official Axiom Banner (Green & Purple Flame)', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-MAT-BAN-1200', isAvailable: true, image: '/images/products/axiom-mat-original-banner-v9.jpg' },

      // Option 2: Volcanic Crimson Ember Flame Edition
      { id: 3111, color: 'Volcanic Crimson Ember Flame Edition', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-MAT-VOL-360', isAvailable: true, image: '/images/products/axiom-mat-volcanic-flame-v9.jpg' },
      { id: 3112, color: 'Volcanic Crimson Ember Flame Edition', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-MAT-VOL-450', isAvailable: true, image: '/images/products/axiom-mat-volcanic-flame-v9.jpg' },
      { id: 3113, color: 'Volcanic Crimson Ember Flame Edition', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-MAT-VOL-800', isAvailable: true, image: '/images/products/axiom-mat-volcanic-flame-v9.jpg' },
      { id: 3114, color: 'Volcanic Crimson Ember Flame Edition', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-MAT-VOL-900', isAvailable: true, image: '/images/products/axiom-mat-volcanic-flame-v9.jpg' },
      { id: 3115, color: 'Volcanic Crimson Ember Flame Edition', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-MAT-VOL-1200', isAvailable: true, image: '/images/products/axiom-mat-volcanic-flame-v9.jpg' },

      // Option 3: Cyber Neon Mascot Edition
      { id: 3121, color: 'Cyber Neon Mascot Edition', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-MAT-NEO-360', isAvailable: true, image: '/images/products/axiom-mat-cyber-neon-v9.jpg' },
      { id: 3122, color: 'Cyber Neon Mascot Edition', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-MAT-NEO-450', isAvailable: true, image: '/images/products/axiom-mat-cyber-neon-v9.jpg' },
      { id: 3123, color: 'Cyber Neon Mascot Edition', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-MAT-NEO-800', isAvailable: true, image: '/images/products/axiom-mat-cyber-neon-v9.jpg' },
      { id: 3124, color: 'Cyber Neon Mascot Edition', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-MAT-NEO-900', isAvailable: true, image: '/images/products/axiom-mat-cyber-neon-v9.jpg' },
      { id: 3125, color: 'Cyber Neon Mascot Edition', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-MAT-NEO-1200', isAvailable: true, image: '/images/products/axiom-mat-cyber-neon-v9.jpg' },
    ]"""

def replace_mat(m):
    return f"{m.group(1)}{new_mat_images}{m.group(2)}{new_mat_variants}"

text = mat_pattern.sub(replace_mat, text, count=1)

# 4. axiom-wrist-rest-01
wrist_pattern = re.compile(r"(\s*id:\s*'axiom-wrist-rest-01',.*?)images:\s*\[.*?\](.*?)variants:\s*\[.*?\]", re.DOTALL)

new_wrist_images = """images: [
      '/images/products/axiom-wrist-rest-classic-green-v9.jpg',
      '/images/products/axiom-wrist-rest-new-font-v9.jpg',
      '/images/products/axiom-wrist-rest-stealth-v9.jpg',
    ]"""

new_wrist_variants = """variants: [
      // Option 1: Original Green Banner Edition (Classic Gothic Text)
      { id: 4301, color: 'Original Green Banner Edition (Classic Gothic)', size: 'Compact 60% (11.4" x 2.9")', price: 19.99, sku: 'AXM-WRIST-GRN-60', isAvailable: true, image: '/images/products/axiom-wrist-rest-classic-green-v9.jpg' },
      { id: 4302, color: 'Original Green Banner Edition (Classic Gothic)', size: 'Tenkeyless TKL 80% (14.2" x 2.9")', price: 21.99, sku: 'AXM-WRIST-GRN-TKL', isAvailable: true, image: '/images/products/axiom-wrist-rest-classic-green-v9.jpg' },
      { id: 4303, color: 'Original Green Banner Edition (Classic Gothic)', size: 'Full-Size 100% (17.5" x 2.9")', price: 23.99, sku: 'AXM-WRIST-GRN-FULL', isAvailable: true, image: '/images/products/axiom-wrist-rest-classic-green-v9.jpg' },

      // Option 2: Tournament Edition (New Esports Font & Crest)
      { id: 4311, color: 'Tournament Edition (New Esports Font & Crest)', size: 'Compact 60% (11.4" x 2.9")', price: 19.99, sku: 'AXM-WRIST-NEW-60', isAvailable: true, image: '/images/products/axiom-wrist-rest-new-font-v9.jpg' },
      { id: 4312, color: 'Tournament Edition (New Esports Font & Crest)', size: 'Tenkeyless TKL 80% (14.2" x 2.9")', price: 21.99, sku: 'AXM-WRIST-NEW-TKL', isAvailable: true, image: '/images/products/axiom-wrist-rest-new-font-v9.jpg' },
      { id: 4313, color: 'Tournament Edition (New Esports Font & Crest)', size: 'Full-Size 100% (17.5" x 2.9")', price: 23.99, sku: 'AXM-WRIST-NEW-FULL', isAvailable: true, image: '/images/products/axiom-wrist-rest-new-font-v9.jpg' },

      // Option 3: Stealth Blackout Edition
      { id: 4321, color: 'Stealth Blackout Tournament Edition', size: 'Compact 60% (11.4" x 2.9")', price: 19.99, sku: 'AXM-WRIST-STL-60', isAvailable: true, image: '/images/products/axiom-wrist-rest-stealth-v9.jpg' },
      { id: 4322, color: 'Stealth Blackout Tournament Edition', size: 'Tenkeyless TKL 80% (14.2" x 2.9")', price: 21.99, sku: 'AXM-WRIST-STL-TKL', isAvailable: true, image: '/images/products/axiom-wrist-rest-stealth-v9.jpg' },
      { id: 4323, color: 'Stealth Blackout Tournament Edition', size: 'Full-Size 100% (17.5" x 2.9")', price: 23.99, sku: 'AXM-WRIST-STL-FULL', isAvailable: true, image: '/images/products/axiom-wrist-rest-stealth-v9.jpg' },
    ]"""

def replace_wrist(m):
    return f"{m.group(1)}{new_wrist_images}{m.group(2)}{new_wrist_variants}"

text = wrist_pattern.sub(replace_wrist, text, count=1)

# 5. Add axiom-beanie-01 if not already present
if 'axiom-beanie-01' not in text:
    axiom_beanie_entry = """  {
    id: 'axiom-beanie-01',
    name: 'Axiom Allegiance Heavy Ribbed Tournament Cuffed Beanie',
    slug: 'axiom-allegiance-heavy-ribbed-tournament-cuffed-beanie',
    description: 'Tournament-ready cold-weather headwear for Axiom Allegiance. Built from ultra-thick 4-gauge hypoallergenic acrylic with a snug 3-inch foldover cuff. Decorated with a centered, high-density embroidered Axiom Owl tournament crest with reinforced perimeter stitching.',
    collection: 'AXA / Axiom Allegiance',
    price: 24.99,
    baseCost: 7.50,
    printCost: 4.00,
    images: [
      '/images/products/axiom-beanie-obsidian-lime-v9.jpg',
      '/images/products/axiom-beanie-purple-green-v9.jpg',
      '/images/products/axiom-beanie-volcanic-v9.jpg',
    ],
    variants: [
      { id: 4401, color: 'Midnight Obsidian / Toxic Green Owl Crest', size: 'One Size (OSFA)', price: 24.99, sku: 'AXM-BN-OBS-GRN', isAvailable: true, image: '/images/products/axiom-beanie-obsidian-lime-v9.jpg' },
      { id: 4402, color: 'Royal Purple & Electric Green Dual-Tone', size: 'One Size (OSFA)', price: 24.99, sku: 'AXM-BN-PRP-GRN', isAvailable: true, image: '/images/products/axiom-beanie-purple-green-v9.jpg' },
      { id: 4403, color: 'Volcanic Crimson / Ember Owl Crest', size: 'One Size (OSFA)', price: 24.99, sku: 'AXM-BN-VOL-RED', isAvailable: true, image: '/images/products/axiom-beanie-volcanic-v9.jpg' },
    ],
    isNew: true,
    material: '100% Hypoallergenic Acrylic • High-Density Direct Embroidery',
    fit: 'Classic Cuffed Snug Fit (One Size Fits Most)',
  },
"""
    target_ins = "  {\n    id: 'axiom-stickers-01',"
    text = text.replace(target_ins, axiom_beanie_entry + target_ins)

    mapping_entry = """  'axiom-beanie-01': {
    blueprintId: 342, // Ribbed Knit Cuffed Beanie
    printProviderId: 29,
    variantMap: { 'One Size (OSFA)': 34201 },
    category: 'Headwear',
  },
  'axiom-stickers-01':"""
    text = text.replace("  'axiom-stickers-01':", mapping_entry)

with open(printify_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated src/services/printify.ts successfully!')
