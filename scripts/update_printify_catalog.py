import re
import os

filepath = os.path.join("src", "services", "printify.ts")

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CatalogProduct interface: add image?: string to variants
if "image?: string;" not in content:
    content = content.replace(
        "    isAvailable: boolean;\n  }>;",
        "    isAvailable: boolean;\n    image?: string;\n  }>;"
    )

# 2. Update custom-krown-works-hat
old_hat_block = """  {
    id: 'custom-krown-works-hat',
    name: 'KrowN Supply Co. Richardson 112 Leather Patch Trucker Snapback',
    slug: 'krown-supply-co-richardson-112-leather-patch-trucker-snapback',
    description: 'The signature flagship headwear of KrowN Supply Co. Cut on the authentic Richardson 112 structured mid-profile silhouette featuring breathable nylon mesh, pre-curved bill with contrast double-stitching, and our genuine laser-etched saddle tan leatherette crown patch. Standard adjustable snapback closure for a tailored streetwear fit.',
    collection: 'KrowN Supply Co.',
    price: 29.99,
    baseCost: 11.50,
    printCost: 4.50,
    images: [
      '/images/products/krown-r112-flagship-leather-patch-snapback.jpg',
      '/images/products/krown-r112-flagship-leather-patch-hero.jpg',
    ],
    variants: [
      { id: 1021, color: 'Heather Grey & Black / Saddle Tan Leather Patch', size: 'OSFA', price: 29.99, sku: 'KSC-HAT-112-GRY', isAvailable: true },
      { id: 1022, color: 'Obsidian Black / Raw Black Leather Patch', size: 'OSFA', price: 29.99, sku: 'KSC-HAT-112-BLK', isAvailable: true },
      { id: 1023, color: 'Charcoal & Black / Honey Leather Patch', size: 'OSFA', price: 29.99, sku: 'KSC-HAT-112-CHR', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Signature Headwear',
    material: 'Authentic Richardson 112: Heather Grey/Black Mesh with Laser-Engraved Caramel Leatherette Patch',
    fit: 'Structured Mid-Profile Snapback (OSFA 7 - 7 3/4)',
  },"""

new_hat_block = """  {
    id: 'custom-krown-works-hat',
    name: 'KrowN Supply Co. Richardson 112 Leather Patch Trucker Snapback',
    slug: 'krown-supply-co-richardson-112-leather-patch-trucker-snapback',
    description: 'The signature flagship headwear of KrowN Supply Co. Cut on the authentic Richardson 112 structured mid-profile silhouette featuring breathable nylon mesh, pre-curved bill with contrast double-stitching, and our genuine laser-etched saddle tan leatherette crown patch. Standard adjustable snapback closure for a tailored streetwear fit.',
    collection: 'KrowN Supply Co.',
    price: 29.99,
    baseCost: 11.50,
    printCost: 4.50,
    images: [
      '/images/products/krown-r112-leather-patch-charcoal-black.jpg',
      '/images/products/krown-r112-leather-patch-heather-grey.jpg',
      '/images/products/krown-r112-leather-patch-obsidian-black.jpg',
      '/images/products/krown-r112-flagship-leather-patch-snapback.jpg',
      '/images/products/krown-r112-flagship-leather-patch-hero.jpg',
    ],
    variants: [
      { id: 1021, color: 'Heather Grey & Black / Saddle Tan Leather Patch', size: 'OSFA', price: 29.99, sku: 'KSC-HAT-112-GRY', isAvailable: true, image: '/images/products/krown-r112-leather-patch-heather-grey.jpg' },
      { id: 1022, color: 'Obsidian Black / Raw Black Leather Patch', size: 'OSFA', price: 29.99, sku: 'KSC-HAT-112-BLK', isAvailable: true, image: '/images/products/krown-r112-leather-patch-obsidian-black.jpg' },
      { id: 1023, color: 'Charcoal & Black / Honey Leather Patch', size: 'OSFA', price: 29.99, sku: 'KSC-HAT-112-CHR', isAvailable: true, image: '/images/products/krown-r112-leather-patch-charcoal-black.jpg' },
    ],
    isNew: true,
    customBadge: 'Signature Headwear',
    material: 'Authentic Richardson 112: Structured Trucker with Laser-Engraved Genuine Leather Patch',
    fit: 'Structured Mid-Profile Snapback (OSFA 7 - 7 3/4)',
  },"""

content = content.replace(old_hat_block, new_hat_block)

# 3. Update krown-streetwear-set image
content = content.replace(
    "    id: 'krown-streetwear-set',\n    name: 'KrowN Supply Co. Premium Streetwear Set (Hoodie + Sweatpants)',\n    slug: 'krown-supply-co-premium-streetwear-set',\n    description: 'The complete KrowN Supply Co. Luxury Streetwear Uniform. Includes both the 480 GSM washed charcoal French terry hoodie and matching tailored sweatpants. Finished with antique gold dipped hardware and precision-embroidered KrowN crown crests.',\n    collection: 'KrowN Supply Co.',\n    price: 154.00,\n    baseCost: 52.00,\n    printCost: 15.00,\n    images: [\n      '/images/products/krown-supply-streetwear-set.jpg',",
    "    id: 'krown-streetwear-set',\n    name: 'KrowN Supply Co. Premium Streetwear Set (Hoodie + Sweatpants)',\n    slug: 'krown-supply-co-premium-streetwear-set',\n    description: 'The complete KrowN Supply Co. Luxury Streetwear Uniform. Includes both the 480 GSM washed charcoal French terry hoodie and matching tailored sweatpants. Finished with antique gold dipped hardware and precision-embroidered KrowN crown crests.',\n    collection: 'KrowN Supply Co.',\n    price: 154.00,\n    baseCost: 52.00,\n    printCost: 15.00,\n    images: [\n      '/images/products/krown-streetwear-set-black.jpg',"
)

# 4. Remove streetwear set from krown-tracksuit-01
content = content.replace(
    "    images: [\n      '/images/products/krown-broken-rules-gold-tracksuit.jpg',\n      '/images/products/krown-supply-streetwear-set.jpg',\n    ],",
    "    images: [\n      '/images/products/krown-broken-rules-gold-tracksuit.jpg',\n    ],"
)

# 5. Update krown-dadhat-01 image
content = content.replace(
    "    images: [\n      '/images/products/krown-vintage-washed-dad-hat.png',\n    ],",
    "    images: [\n      '/images/products/krown-dad-hat-washed-black.jpg',\n    ],"
)

# 6. Update krown-shorts-01 image
content = content.replace(
    "    images: [\n      '/images/products/krown-french-terry-streetwear-shorts.png',\n    ],",
    "    images: [\n      '/images/products/krown-french-terry-shorts.jpg',\n    ],"
)

# 7. Add KrowN Supply Co. Shaker Bottle right after krown-shorts-01
krown_shaker_code = """  {
    id: 'krown-shaker-01',
    name: 'KrowN Supply Co. Signature Luxury Shaker Bottle',
    slug: 'krown-supply-co-signature-luxury-shaker-bottle',
    description: 'Minimalist luxury meets everyday hydration. Features a leak-proof locking flip cap with ergonomic loop, surgical stainless steel blending whisk, and the authentic metallic antique gold KrowN crown monogram emblem. Engineered in two pro builds: Standard 24oz Frosted Eastman Tritan™ Polymer ($26.99) or Pro 26oz Double-Wall Vacuum Insulated Kitchen-Grade Stainless Steel ($36.99).',
    collection: 'KrowN Supply Co.',
    price: 26.99,
    baseCost: 7.50,
    printCost: 4.00,
    images: [
      '/images/products/krown-shaker-obsidian-steel.jpg',
      '/images/products/krown-shaker-obsidian-tritan.jpg',
      '/images/products/krown-shaker-smoke-steel.jpg',
      '/images/products/krown-shaker-smoke-tritan.jpg',
      '/images/products/krown-shaker-brushed-steel.jpg',
      '/images/products/krown-shaker-brushed-tritan.jpg',
      '/images/products/krown-shaker-bottles-3-editions.jpg',
    ],
    variants: [
      { id: 1221, color: 'Matte Obsidian Black & Antique Gold Crown', size: '24 oz Standard (Eastman Tritan Frosted)', price: 26.99, sku: 'KSC-SHK-OBS-TRITAN', isAvailable: true, image: '/images/products/krown-shaker-obsidian-tritan.jpg' },
      { id: 1222, color: 'Matte Obsidian Black & Antique Gold Crown', size: '26 oz Pro Double-Wall Insulated Stainless Steel', price: 36.99, sku: 'KSC-SHK-OBS-STEEL', isAvailable: true, image: '/images/products/krown-shaker-obsidian-steel.jpg' },
      { id: 1223, color: 'Frosted Smoke & Polished Gold Accents', size: '24 oz Standard (Eastman Tritan Frosted)', price: 26.99, sku: 'KSC-SHK-SMK-TRITAN', isAvailable: true, image: '/images/products/krown-shaker-smoke-tritan.jpg' },
      { id: 1224, color: 'Frosted Smoke & Polished Gold Accents', size: '26 oz Pro Double-Wall Insulated Stainless Steel', price: 36.99, sku: 'KSC-SHK-SMK-STEEL', isAvailable: true, image: '/images/products/krown-shaker-smoke-steel.jpg' },
      { id: 1225, color: 'Raw Brushed Steel & Minimal Crown Monogram', size: '24 oz Standard (Eastman Tritan Frosted)', price: 26.99, sku: 'KSC-SHK-BRS-TRITAN', isAvailable: true, image: '/images/products/krown-shaker-brushed-tritan.jpg' },
      { id: 1226, color: 'Raw Brushed Steel & Minimal Crown Monogram', size: '26 oz Pro Double-Wall Insulated Stainless Steel', price: 36.99, sku: 'KSC-SHK-BRS-STEEL', isAvailable: true, image: '/images/products/krown-shaker-brushed-steel.jpg' },
    ],
    isNew: true,
    material: 'BPA-Free Eastman Tritan™ / Double-Wall 18/8 Kitchen-Grade Stainless Steel • Whisk Ball Included',
    fit: '24–26 oz Capacity • Cup Holder Compatible',
  },
"""
if "krown-shaker-01" not in content:
    content = content.replace("  // ==========================================\n  // 2. KrowN Construction", krown_shaker_code + "  // ==========================================\n  // 2. KrowN Construction")

# 8. Update KrowN Beanie image
content = content.replace(
    "    id: 'krown-beanie-01',\n    name: 'KrowN Heavy Ribbed Tradesman Cuffed Beanie',\n    slug: 'krown-heavy-ribbed-tradesman-cuffed-beanie',\n    description: 'Thick-gauge acrylic ribbed knit cuffed winter beanie with official KrowN Construction LLC patch. Engineered to stay put under hardhats or in sub-zero jobsite mornings.',\n    collection: 'KrowN Construction',\n    price: 26.00,\n    baseCost: 7.20,\n    printCost: 4.00,\n    images: [\n      '/images/products/krown-construction-cuffed-beanie.png',\n    ],",
    "    id: 'krown-beanie-01',\n    name: 'KrowN Heavy Ribbed Tradesman Cuffed Beanie',\n    slug: 'krown-heavy-ribbed-tradesman-cuffed-beanie',\n    description: 'Thick-gauge acrylic ribbed knit cuffed winter beanie with official KrowN Construction LLC patch (Since 2018). Engineered to stay put under hardhats or in sub-zero jobsite mornings.',\n    collection: 'KrowN Construction',\n    price: 26.00,\n    baseCost: 7.20,\n    printCost: 4.00,\n    images: [\n      '/images/products/krown-beanie-studio-front.jpg',\n    ],"
)

# 9. Update krown-work-01 and add kc-shaker-01 to KrowN Construction
old_work_shirt = """  {
    id: 'krown-work-01',
    name: 'Built to Reign Heavy Work Shirt',
    slug: 'built-to-reign-heavy-work-shirt',
    description: 'Designed in conjunction with KrowN Construction LLC field tests. Heavy-duty ripstop poly-cotton blend with reinforced shoulder stitching and chest pencil pockets.',
    collection: 'KrowN Construction',
    price: 48.00,
    baseCost: 15.00,
    printCost: 6.50,
    images: ['/images/branding/construction/Krown ConstructionPNG Black.PNG'],
    variants: [
      { id: 401, color: 'Charcoal / High-Vis Lime Accents', size: 'M', price: 48.00, sku: 'KRN-WRK-SHR-M', isAvailable: true },
      { id: 402, color: 'Charcoal / High-Vis Lime Accents', size: 'L', price: 48.00, sku: 'KRN-WRK-SHR-L', isAvailable: true },
      { id: 403, color: 'Charcoal / High-Vis Lime Accents', size: 'XL', price: 48.00, sku: 'KRN-WRK-SHR-XL', isAvailable: true },
      { id: 404, color: 'Charcoal / High-Vis Lime Accents', size: '2XL', price: 50.00, sku: 'KRN-WRK-SHR-2XL', isAvailable: true },
    ],
    material: '65% Polyester, 35% Cotton Heavy Twill',
    fit: 'Relaxed Workwear Fit with Enhanced Arm Mobility',
  },"""

new_work_and_shaker = """  {
    id: 'krown-work-01',
    name: 'KrowN Construction "Built to Reign" Heavy Work Shirt',
    slug: 'krown-construction-built-to-reign-heavy-work-shirt',
    description: 'Heavyweight jobsite work shirt engineered in conjunction with KrowN Construction LLC field trials. Features a durable 300 GSM ripstop cotton-twill blend, reinforced double-needle seams, chest pencil pocket, and official KrowN Construction branding: Left or Right chest crest, bold full-width "BUILT TO REIGN" back statement piece, and vertical sleeve typography "KrowN Construction".',
    collection: 'KrowN Construction',
    price: 48.00,
    baseCost: 15.00,
    printCost: 6.50,
    images: [
      '/images/products/kc-work-shirt-grey-front.jpg',
      '/images/products/kc-work-shirt-black-front.jpg',
      '/images/products/kc-work-shirt-charcoal-back.jpg',
      '/images/products/kc-work-shirt-model.jpg',
    ],
    variants: [
      { id: 401, color: 'Heather Steel Grey / Black-Gold Crest', size: 'S', price: 48.00, sku: 'KC-WRK-GRY-S', isAvailable: true, image: '/images/products/kc-work-shirt-grey-front.jpg' },
      { id: 402, color: 'Heather Steel Grey / Black-Gold Crest', size: 'M', price: 48.00, sku: 'KC-WRK-GRY-M', isAvailable: true, image: '/images/products/kc-work-shirt-grey-front.jpg' },
      { id: 403, color: 'Heather Steel Grey / Black-Gold Crest', size: 'L', price: 48.00, sku: 'KC-WRK-GRY-L', isAvailable: true, image: '/images/products/kc-work-shirt-grey-front.jpg' },
      { id: 404, color: 'Heather Steel Grey / Black-Gold Crest', size: 'XL', price: 48.00, sku: 'KC-WRK-GRY-XL', isAvailable: true, image: '/images/products/kc-work-shirt-grey-front.jpg' },
      { id: 405, color: 'Heather Steel Grey / Black-Gold Crest', size: '2XL', price: 52.00, sku: 'KC-WRK-GRY-2XL', isAvailable: true, image: '/images/products/kc-work-shirt-grey-front.jpg' },
      { id: 406, color: 'Heather Steel Grey / Black-Gold Crest', size: '3XL', price: 54.00, sku: 'KC-WRK-GRY-3XL', isAvailable: true, image: '/images/products/kc-work-shirt-grey-front.jpg' },
      { id: 407, color: 'Obsidian Black / Gold & White Crest', size: 'S', price: 48.00, sku: 'KC-WRK-BLK-S', isAvailable: true, image: '/images/products/kc-work-shirt-black-front.jpg' },
      { id: 408, color: 'Obsidian Black / Gold & White Crest', size: 'M', price: 48.00, sku: 'KC-WRK-BLK-M', isAvailable: true, image: '/images/products/kc-work-shirt-black-front.jpg' },
      { id: 409, color: 'Obsidian Black / Gold & White Crest', size: 'L', price: 48.00, sku: 'KC-WRK-BLK-L', isAvailable: true, image: '/images/products/kc-work-shirt-black-front.jpg' },
      { id: 410, color: 'Obsidian Black / Gold & White Crest', size: 'XL', price: 48.00, sku: 'KC-WRK-BLK-XL', isAvailable: true, image: '/images/products/kc-work-shirt-black-front.jpg' },
      { id: 411, color: 'Obsidian Black / Gold & White Crest', size: '2XL', price: 52.00, sku: 'KC-WRK-BLK-2XL', isAvailable: true, image: '/images/products/kc-work-shirt-black-front.jpg' },
      { id: 412, color: 'Obsidian Black / Gold & White Crest', size: '3XL', price: 54.00, sku: 'KC-WRK-BLK-3XL', isAvailable: true, image: '/images/products/kc-work-shirt-black-front.jpg' },
      { id: 413, color: 'Charcoal Slate / Purple & Lime Crest', size: 'S', price: 48.00, sku: 'KC-WRK-CHR-S', isAvailable: true, image: '/images/products/kc-work-shirt-charcoal-back.jpg' },
      { id: 414, color: 'Charcoal Slate / Purple & Lime Crest', size: 'M', price: 48.00, sku: 'KC-WRK-CHR-M', isAvailable: true, image: '/images/products/kc-work-shirt-charcoal-back.jpg' },
      { id: 415, color: 'Charcoal Slate / Purple & Lime Crest', size: 'L', price: 48.00, sku: 'KC-WRK-CHR-L', isAvailable: true, image: '/images/products/kc-work-shirt-charcoal-back.jpg' },
      { id: 416, color: 'Charcoal Slate / Purple & Lime Crest', size: 'XL', price: 48.00, sku: 'KC-WRK-CHR-XL', isAvailable: true, image: '/images/products/kc-work-shirt-charcoal-back.jpg' },
      { id: 417, color: 'Charcoal Slate / Purple & Lime Crest', size: '2XL', price: 52.00, sku: 'KC-WRK-CHR-2XL', isAvailable: true, image: '/images/products/kc-work-shirt-charcoal-back.jpg' },
      { id: 418, color: 'Charcoal Slate / Purple & Lime Crest', size: '3XL', price: 54.00, sku: 'KC-WRK-CHR-3XL', isAvailable: true, image: '/images/products/kc-work-shirt-charcoal-back.jpg' },
    ],
    material: '300 GSM Heavyweight Cotton-Twill Blend • Stain-Resistant Finish',
    fit: 'Tradesman Relaxed Mobility Fit with Split-Tail Hem',
  },
  {
    id: 'kc-shaker-01',
    name: 'KrowN Construction "Built to Reign" Heavy-Duty Shaker Bottle',
    slug: 'krown-construction-built-to-reign-heavy-duty-shaker-bottle',
    description: 'Jobsite hydration engineered for tradesmen. Heavy-duty impact-resistant shaker bottle featuring commercial leakproof lock lid, reinforced carry loop, surgical steel blending whisk ball, and the bold industrial KrowN Construction seal. Available in 3 jobsite colorways and 2 builds: 24oz Eastman Tritan™ Frosted Impact Polymer ($26.99) or 26oz Double-Wall Vacuum Insulated Stainless Steel ($36.99).',
    collection: 'KrowN Construction',
    price: 26.99,
    baseCost: 7.50,
    printCost: 4.00,
    images: [
      '/images/products/kc-shaker-highvis-steel.jpg',
      '/images/products/kc-shaker-highvis-tritan.jpg',
      '/images/products/kc-shaker-steelcore-steel.jpg',
      '/images/products/kc-shaker-steelcore-tritan.jpg',
      '/images/products/kc-shaker-jobsite-steel.jpg',
      '/images/products/kc-shaker-jobsite-tritan.jpg',
      '/images/products/kc-shaker-bottles-3-editions.jpg',
    ],
    variants: [
      { id: 1211, color: 'High-Vis Safety Gold & Matte Black', size: '24 oz Standard (Eastman Tritan Frosted)', price: 26.99, sku: 'KC-SHK-HV-TRITAN', isAvailable: true, image: '/images/products/kc-shaker-highvis-tritan.jpg' },
      { id: 1212, color: 'High-Vis Safety Gold & Matte Black', size: '26 oz Pro Heavy-Duty Insulated Stainless Steel', price: 36.99, sku: 'KC-SHK-HV-STEEL', isAvailable: true, image: '/images/products/kc-shaker-highvis-steel.jpg' },
      { id: 1213, color: 'Industrial Steel & Concrete Grey', size: '24 oz Standard (Eastman Tritan Frosted)', price: 26.99, sku: 'KC-SHK-SC-TRITAN', isAvailable: true, image: '/images/products/kc-shaker-steelcore-tritan.jpg' },
      { id: 1214, color: 'Industrial Steel & Concrete Grey', size: '26 oz Pro Heavy-Duty Insulated Stainless Steel', price: 36.99, sku: 'KC-SHK-SC-STEEL', isAvailable: true, image: '/images/products/kc-shaker-steelcore-steel.jpg' },
      { id: 1215, color: 'Jobsite Lime & Purple Edition', size: '24 oz Standard (Eastman Tritan Frosted)', price: 26.99, sku: 'KC-SHK-JL-TRITAN', isAvailable: true, image: '/images/products/kc-shaker-jobsite-tritan.jpg' },
      { id: 1216, color: 'Jobsite Lime & Purple Edition', size: '26 oz Pro Heavy-Duty Insulated Stainless Steel', price: 36.99, sku: 'KC-SHK-JL-STEEL', isAvailable: true, image: '/images/products/kc-shaker-jobsite-steel.jpg' },
    ],
    isNew: true,
    material: 'Impact-Resistant Eastman Tritan™ / Double-Wall 18/8 Stainless Steel • Surgical Steel Whisk',
    fit: '24–26 oz Capacity • Heavy Duty Leakproof Seal',
  },"""

content = content.replace(old_work_shirt, new_work_and_shaker)

# 10. Update axiom-shaker-01
old_axiom_shaker = """  {
    id: 'axiom-shaker-01',
    name: 'Axiom Allegiance Pro Loadout Shaker Bottle',
    slug: 'axiom-allegiance-pro-loadout-shaker',
    description: 'Fuel up for overtime clutches and all-night ranked marathons. Ultra-premium gaming supplement shaker bottle featuring leak-proof locking cap, silicone collar, ergonomic carrying loop, surgical stainless steel whisk ball, and the iconic official Axiom Allegiance owl crest with distinctive A-X-A facial geometry. Available in two official esports colorways (Signature Toxic Lime & Royal Purple, and Stealth Blackout Obsidian), each engineered in two pro builds: Standard 24oz Frosted Shatterproof Eastman Tritan™ Polymer or Pro 26oz Double-Wall Vacuum Insulated Stainless Steel.',
    collection: 'AXA / Axiom Allegiance',
    price: 24.99,
    baseCost: 7.20,
    printCost: 3.80,
    images: [
      '/images/products/axiom-shaker-signature-tritan-clean.jpg',
      '/images/products/axiom-shaker-signature-steel-clean.jpg',
      '/images/products/axiom-shaker-stealth-tritan-clean.jpg',
      '/images/products/axiom-shaker-stealth-steel-clean.jpg',
      '/images/products/axiom-shaker-bottles-4-editions.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
      { id: 1201, color: 'Signature Toxic Lime & Royal Purple', size: '24 oz Standard (Eastman Tritan Frosted)', price: 24.99, sku: 'AXM-SHK-SIG-TRITAN', isAvailable: true },
      { id: 1202, color: 'Signature Toxic Lime & Royal Purple', size: '26 oz Pro Insulated Stainless Steel (Double-Wall)', price: 34.99, sku: 'AXM-SHK-SIG-STEEL', isAvailable: true },
      { id: 1203, color: 'Stealth Blackout Obsidian', size: '24 oz Standard (Eastman Tritan Frosted)', price: 24.99, sku: 'AXM-SHK-STL-TRITAN', isAvailable: true },
      { id: 1204, color: 'Stealth Blackout Obsidian', size: '26 oz Pro Insulated Stainless Steel (Double-Wall)', price: 34.99, sku: 'AXM-SHK-STL-STEEL', isAvailable: true },
    ],
    isNew: true,
    material: 'BPA-Free Eastar™ Tritan / Double-Wall Kitchen-Grade Steel • Stainless Steel Whisk Ball',
    fit: '24–26 oz Capacity • Fits Standard Car & Desk Cupholders',
  },"""

new_axiom_shaker = """  {
    id: 'axiom-shaker-01',
    name: 'Axiom Allegiance Pro Loadout Shaker Bottle',
    slug: 'axiom-allegiance-pro-loadout-shaker',
    description: 'Fuel up for overtime clutches and all-night ranked marathons. Ultra-premium gaming supplement shaker bottle featuring leak-proof locking cap, silicone collar, ergonomic carrying loop, surgical stainless steel whisk ball, and the iconic official Axiom Allegiance owl crest with distinctive A-X-A facial geometry. Available in two official esports colorways (Signature Toxic Lime & Royal Purple, and Stealth Blackout Obsidian), each engineered in two pro builds: Standard 24oz Frosted Shatterproof Eastman Tritan™ Polymer or Pro 26oz Double-Wall Vacuum Insulated Stainless Steel.',
    collection: 'AXA / Axiom Allegiance',
    price: 24.99,
    baseCost: 7.20,
    printCost: 3.80,
    images: [
      '/images/products/axiom-shaker-signature-tritan-clean.jpg',
      '/images/products/axiom-shaker-signature-steel-clean.jpg',
      '/images/products/axiom-shaker-stealth-tritan-clean.jpg',
      '/images/products/axiom-shaker-stealth-steel-clean.jpg',
      '/images/products/axiom-shaker-bottles-4-editions.jpg',
    ],
    variants: [
      { id: 1201, color: 'Signature Toxic Lime & Royal Purple', size: '24 oz Standard (Eastman Tritan Frosted)', price: 24.99, sku: 'AXM-SHK-SIG-TRITAN', isAvailable: true, image: '/images/products/axiom-shaker-signature-tritan-clean.jpg' },
      { id: 1202, color: 'Signature Toxic Lime & Royal Purple', size: '26 oz Pro Insulated Stainless Steel (Double-Wall)', price: 34.99, sku: 'AXM-SHK-SIG-STEEL', isAvailable: true, image: '/images/products/axiom-shaker-signature-steel-clean.jpg' },
      { id: 1203, color: 'Stealth Blackout Obsidian', size: '24 oz Standard (Eastman Tritan Frosted)', price: 24.99, sku: 'AXM-SHK-STL-TRITAN', isAvailable: true, image: '/images/products/axiom-shaker-stealth-tritan-clean.jpg' },
      { id: 1204, color: 'Stealth Blackout Obsidian', size: '26 oz Pro Insulated Stainless Steel (Double-Wall)', price: 34.99, sku: 'AXM-SHK-STL-STEEL', isAvailable: true, image: '/images/products/axiom-shaker-stealth-steel-clean.jpg' },
    ],
    isNew: true,
    material: 'BPA-Free Eastar™ Tritan / Double-Wall Kitchen-Grade Steel • Stainless Steel Whisk Ball',
    fit: '24–26 oz Capacity • Fits Standard Car & Desk Cupholders',
  },"""

content = content.replace(old_axiom_shaker, new_axiom_shaker)

# 11. Update axiom-mug-01 and axiom-mug-02 (remove raw branding graphics)
content = content.replace(
    "    images: [\n      '/images/products/axiom-owl-gamer-mug-15oz.png',\n      '/images/branding/gaming/axiom-owl-quote-frame.jpg'\n    ],",
    "    images: [\n      '/images/products/axiom-mug-smokey-crest-15oz.png',\n    ],"
)

content = content.replace(
    "    images: [\n      '/images/products/axiom-mug-smokey-crest-15oz.png',\n      '/images/branding/gaming/axiom-owl-smokey-crest.jpg',\n    ],",
    "    images: [\n      '/images/products/axiom-mug-smokey-crest-15oz.png',\n    ],"
)

# 12. Split krown-stickers-01 into axiom-stickers-01 and kc-stickers-01
old_stickers = """  {
    id: 'krown-stickers-01',
    name: 'Axiom Owl & KrowN Holographic Die-Cut Sticker Pack',
    slug: 'axiom-owl-krown-holographic-sticker-pack',
    description: 'Pack of 5 heavy UV-laminated holographic vinyl stickers including the Axiom Owl esports emblem, KrowN Construction crest, and metallic brand marks. Waterproof, UV-shielded, and ready for PCs, hardhats, consoles, and toolboxes.',
    collection: 'Accessories',
    price: 14.99,
    baseCost: 2.10,
    printCost: 1.80,
    images: [
      '/images/branding/gaming/axiom-owl-mascot.png',
      '/images/branding/construction/KC logo black and white.png',
    ],
    variants: [
      { id: 501, color: 'Holographic Multi-Pack', size: '5-Pack', price: 14.99, sku: 'AXM-KRN-STK-PK5', isAvailable: true }
    ],
    material: '6 mil Thick Weatherproof Holographic Vinyl with UV Shield',
    fit: '3" to 4" Widths',
  },"""

new_stickers = """  {
    id: 'axiom-stickers-01',
    name: 'Axiom Allegiance Holographic Battle Pack Decals (5-Pack)',
    slug: 'axiom-allegiance-holographic-battle-pack-decals',
    description: 'Pack of 5 premium heavy UV-laminated holographic vinyl stickers featuring the official Axiom Owl mascot crest, Gothic typography wordmarks, and geometric A-X-A eye emblems. Waterproof, scratch-proof, and designed for battlestations, laptops, and gear cases.',
    collection: 'AXA / Axiom Allegiance',
    price: 12.99,
    baseCost: 2.10,
    printCost: 1.80,
    images: [
      '/images/products/axiom-stickers-holographic-pack.jpg',
    ],
    variants: [
      { id: 501, color: 'Axiom Holographic 5-Pack', size: '5-Pack', price: 12.99, sku: 'AXM-STK-HOLO-PK5', isAvailable: true, image: '/images/products/axiom-stickers-holographic-pack.jpg' }
    ],
    material: '6 mil Thick Weatherproof Holographic Vinyl with UV Shield',
    fit: '3" to 4" Widths',
  },
  {
    id: 'kc-stickers-01',
    name: 'KrowN Construction Weatherproof Jobsite Vinyl Decals (5-Pack)',
    slug: 'krown-construction-weatherproof-jobsite-vinyl-decals',
    description: 'Pack of 5 heavy-duty cast vinyl decals tested on commercial jobsites. Features the industrial KrowN Construction badge, "BUILT TO REIGN" seals, and hardhat emblems with high-bond adhesive that withstands weather, dirt, and power washers.',
    collection: 'KrowN Construction',
    price: 12.99,
    baseCost: 2.10,
    printCost: 1.80,
    images: [
      '/images/products/krown-construction-jobsite-decals.jpg',
    ],
    variants: [
      { id: 502, color: 'Jobsite Decal 5-Pack', size: '5-Pack', price: 12.99, sku: 'KC-STK-VNYL-PK5', isAvailable: true, image: '/images/products/krown-construction-jobsite-decals.jpg' }
    ],
    material: '6 mil Thick Weatherproof Cast Vinyl with High-Tack Adhesive',
    fit: '3" to 4" Widths',
  },"""

content = content.replace(old_stickers, new_stickers)

# 13. Strip any remaining '/images/branding/' from images arrays
# Pattern: lines with '/images/branding/...' inside images: [ ... ]
def strip_branding_lines(text):
    lines = text.split("\n")
    out = []
    for line in lines:
        if "'/images/branding/" in line and ("images:" in line or re.match(r"\s*'/images/branding/", line)):
            # Skip this line
            continue
        out.append(line)
    return "\n".join(out)

content = strip_branding_lines(content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated printify.ts successfully!")
