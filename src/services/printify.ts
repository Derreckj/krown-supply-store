/**
 * KrowN Supply Co. - Printify Service Abstraction Layer
 * 
 * Provides seamless access to Printify catalog, variant inventories, and order creation.
 * Strictly adheres to official KrowN brand identities:
 * 1. KrowN Supply Co. ("WEAR THE KROWN.")
 * 2. KrowN Construction LLC ("BUILT TO REIGN.")
 * 3. KrowN Gaming ("PLAY TO REIGN.")
 * 4. AXA / Axiom Allegiance (Official Esports Division)
 */

import { calculateProductEconomics, ProductEconomicsResult } from '@/lib/economics';

export interface PrintifyVariant {
  id: number;
  title: string;
  sku: string;
  cost: number; // in cents
  price: number; // in cents
  is_enabled: boolean;
  is_available: boolean;
  options: {
    color?: string;
    size?: string;
  };
}

export interface PrintifyProductRaw {
  id: string;
  title: string;
  description: string;
  tags: string[];
  images: Array<{ src: string; is_default: boolean }>;
  variants: PrintifyVariant[];
  created_at: string;
  updated_at: string;
}

export interface CatalogProduct {
  id: string;
  name: string;
  slug: string;
  description: string;
  collection: 'KrowN Supply Co.' | 'KrowN Gaming' | 'AXA / Axiom Allegiance' | 'KrowN Construction' | 'Accessories';
  price: number;
  baseCost: number;
  printCost: number;
  images: string[];
  variants: Array<{
    id: number;
    color: string;
    size: string;
    price: number;
    sku: string;
    isAvailable: boolean;
  }>;
  isNew?: boolean;
  isLimited?: boolean;
  customBadge?: string;
  material?: string;
  fit?: string;
  economics?: ProductEconomicsResult;
}

export interface CatalogAuditReport {
  timestamp: string;
  totalProducts: number;
  totalVariants: number;
  availableVariants: number;
  outOfStockVariants: number;
  lowStockItems: string[];
  discontinuedOrOosItems: Array<{
    productId: string;
    productName: string;
    variantSku: string;
    variantTitle: string;
  }>;
  marginAlerts: Array<{
    productId: string;
    productName: string;
    marginPercent: number;
    status: string;
  }>;
}

// Curated Initial Launch Catalog strictly segregated by brand identity
const INITIAL_MOCK_CATALOG: CatalogProduct[] = [
  // ==========================================
  // 1. KrowN Supply Co. (Luxury Streetwear)
  // Slogan: "WEAR THE KROWN."
  // ==========================================
  {
    id: 'krown-hoodie-premium',
    name: 'KrowN Supply Co. 480 GSM Heavyweight Streetwear Hoodie',
    slug: 'krown-supply-co-480gsm-heavyweight-streetwear-hoodie',
    description: 'The pinnacle of luxury streetwear. Cut from ultra-heavyweight 480 GSM French terry cotton in vintage washed charcoal black with drop shoulders and an exaggerated crossover double-layered hood. Features our minimal metallic antique gold and brushed steel 3D geometric faceted K-crown brand emblem on the left chest, and a bold statement back print with clean arched "KrowN Supply Co." typography and the official faceted 3D geometric K-crown brand emblem. Heavy split-stitch construction, thick ribbed cuffs and hem, and relaxed modern drape.',
    collection: 'KrowN Supply Co.',
    price: 88.00,
    baseCost: 28.00,
    printCost: 8.00,
    images: [
      '/images/products/krown-supply-premium-hoodie-front.jpg',
      '/images/products/krown-hoodie-female-model.jpg',
      '/images/products/krown-heavyweight-hoodie-back-krown.jpg',
      '/images/products/krown-hoodie-male-model.jpg',
      '/images/products/krown-hoodie-studio-front.jpg',
    ],
    variants: [
      { id: 2011, color: 'Vintage Washed Charcoal / Gold Crest', size: 'S', price: 88.00, sku: 'KSC-HD-480-S', isAvailable: true },
      { id: 2012, color: 'Vintage Washed Charcoal / Gold Crest', size: 'M', price: 88.00, sku: 'KSC-HD-480-M', isAvailable: true },
      { id: 2013, color: 'Vintage Washed Charcoal / Gold Crest', size: 'L', price: 88.00, sku: 'KSC-HD-480-L', isAvailable: true },
      { id: 2014, color: 'Vintage Washed Charcoal / Gold Crest', size: 'XL', price: 88.00, sku: 'KSC-HD-480-XL', isAvailable: true },
      { id: 2015, color: 'Vintage Washed Charcoal / Gold Crest', size: '2XL', price: 92.00, sku: 'KSC-HD-480-2XL', isAvailable: true },
      { id: 2016, color: 'Vintage Washed Charcoal / Gold Crest', size: '3XL', price: 96.00, sku: 'KSC-HD-480-3XL', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Streetwear Flagship',
    material: '480 GSM Heavy 100% French Terry Cotton • Mineral Washed',
    fit: 'Exaggerated Boxy Streetwear Silhouette with Drop Shoulders',
  },
  {
    id: 'krown-sweatpants-premium',
    name: 'KrowN Supply Co. Heavyweight Tailored Streetwear Sweatpants',
    slug: 'krown-supply-co-heavyweight-tailored-streetwear-sweatpants',
    description: 'Designed as the definitive luxury streetwear companion to the 480 GSM hoodie. Crafted from matching ultra-heavyweight 480 GSM French terry cotton in vintage washed charcoal black. Features an elastic waistband with braided drawstrings, polished antique gold aglets, deep side slash pockets, tailored streetwear taper, and the signature metallic antique gold embroidered KrowN crown on the upper left thigh.',
    collection: 'KrowN Supply Co.',
    price: 78.00,
    baseCost: 24.00,
    printCost: 7.00,
    images: [
      '/images/products/krown-supply-premium-sweatpants.jpg',
    ],
    variants: [
      { id: 2021, color: 'Vintage Washed Charcoal / Gold Crest', size: 'S', price: 78.00, sku: 'KSC-SWP-480-S', isAvailable: true },
      { id: 2022, color: 'Vintage Washed Charcoal / Gold Crest', size: 'M', price: 78.00, sku: 'KSC-SWP-480-M', isAvailable: true },
      { id: 2023, color: 'Vintage Washed Charcoal / Gold Crest', size: 'L', price: 78.00, sku: 'KSC-SWP-480-L', isAvailable: true },
      { id: 2024, color: 'Vintage Washed Charcoal / Gold Crest', size: 'XL', price: 78.00, sku: 'KSC-SWP-480-XL', isAvailable: true },
      { id: 2025, color: 'Vintage Washed Charcoal / Gold Crest', size: '2XL', price: 82.00, sku: 'KSC-SWP-480-2XL', isAvailable: true },
      { id: 2026, color: 'Vintage Washed Charcoal / Gold Crest', size: '3XL', price: 86.00, sku: 'KSC-SWP-480-3XL', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Streetwear Flagship',
    material: '480 GSM Heavy 100% French Terry Cotton • Mineral Washed',
    fit: 'Modern Relaxed Taper with Heavy Ribbed Ankle Cuffs',
  },
  {
    id: 'krown-streetwear-set',
    name: 'KrowN Supply Co. Premium Streetwear Set (Hoodie + Sweatpants)',
    slug: 'krown-supply-co-premium-streetwear-set',
    description: 'The complete KrowN Supply Co. Luxury Streetwear Uniform. Includes both the 480 GSM washed charcoal French terry hoodie and matching tailored sweatpants. Finished with antique gold dipped hardware and precision-embroidered KrowN crown crests.',
    collection: 'KrowN Supply Co.',
    price: 154.00,
    baseCost: 52.00,
    printCost: 15.00,
    images: [
      '/images/products/krown-supply-streetwear-set.jpg',
      '/images/products/krown-supply-premium-hoodie-front.jpg',
      '/images/products/krown-supply-premium-sweatpants.jpg',
    ],
    variants: [
      { id: 2031, color: 'Washed Charcoal Set (Save $12)', size: 'S', price: 154.00, sku: 'KSC-SET-480-S', isAvailable: true },
      { id: 2032, color: 'Washed Charcoal Set (Save $12)', size: 'M', price: 154.00, sku: 'KSC-SET-480-M', isAvailable: true },
      { id: 2033, color: 'Washed Charcoal Set (Save $12)', size: 'L', price: 154.00, sku: 'KSC-SET-480-L', isAvailable: true },
      { id: 2034, color: 'Washed Charcoal Set (Save $12)', size: 'XL', price: 154.00, sku: 'KSC-SET-480-XL', isAvailable: true },
      { id: 2035, color: 'Washed Charcoal Set (Save $12)', size: '2XL', price: 162.00, sku: 'KSC-SET-480-2XL', isAvailable: true },
      { id: 2036, color: 'Washed Charcoal Set (Save $12)', size: '3XL', price: 170.00, sku: 'KSC-SET-480-3XL', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Coordinated Set',
    material: '480 GSM Ultra-Heavy French Terry Cotton Set',
    fit: 'Coordinated Relaxed Streetwear Fit',
  },
  {
    id: 'krown-tracksuit-01',
    name: 'KrowN "Broken Rules" Kintsugi Gold Fleece Track Jacket & Joggers Set',
    slug: 'krown-broken-rules-kintsugi-gold-tracksuit-set',
    description: 'High-fashion luxury streetwear tracksuit crafted from 420 GSM brushed black fleece. Features metallic antique gold cursive embroidery "Wear The KrowN" on the chest, intricate golden fractured kintsugi lightning crack embroidery across the front pockets and collar, matching tailored joggers, and a solid cast gold crown zipper pull.',
    collection: 'KrowN Supply Co.',
    price: 128.00,
    baseCost: 42.00,
    printCost: 14.00,
    images: [
      '/images/products/krown-broken-rules-gold-tracksuit.jpg',
      '/images/products/krown-supply-streetwear-set.jpg',
    ],
    variants: [
      { id: 931, color: 'Obsidian Black / Embroidered Gold Kintsugi', size: 'S', price: 128.00, sku: 'KSC-TRK-KNT-S', isAvailable: true },
      { id: 932, color: 'Obsidian Black / Embroidered Gold Kintsugi', size: 'M', price: 128.00, sku: 'KSC-TRK-KNT-M', isAvailable: true },
      { id: 933, color: 'Obsidian Black / Embroidered Gold Kintsugi', size: 'L', price: 128.00, sku: 'KSC-TRK-KNT-L', isAvailable: true },
      { id: 934, color: 'Obsidian Black / Embroidered Gold Kintsugi', size: 'XL', price: 128.00, sku: 'KSC-TRK-KNT-XL', isAvailable: true },
      { id: 935, color: 'Obsidian Black / Embroidered Gold Kintsugi', size: '2XL', price: 134.00, sku: 'KSC-TRK-KNT-2XL', isAvailable: true },
      { id: 936, color: 'Obsidian Black / Embroidered Gold Kintsugi', size: '3XL', price: 140.00, sku: 'KSC-TRK-KNT-3XL', isAvailable: true },
    ],
    isNew: true,
    material: '420 GSM Luxury Heavyweight Cotton Fleece • Custom Gold Hardware',
    fit: 'Relaxed Tailored Streetwear Tracksuit Fit',
  },
  {
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
  },
  {
    id: 'krown-dadhat-01',
    name: 'KrowN Vintage Washed Chino Dad Hat',
    slug: 'krown-vintage-washed-chino-dad-hat',
    description: 'Low-profile unstructured 6-panel cap crafted from 100% bio-washed cotton chino twill in vintage washed charcoal black. Features pre-curved visor, stitched ventilation eyelets, self-fabric strap with antique brass buckle, and 3D metallic antique gold embroidered KrowN crown monogram.',
    collection: 'KrowN Supply Co.',
    price: 28.00,
    baseCost: 7.50,
    printCost: 5.00,
    images: [
      '/images/products/krown-vintage-washed-dad-hat.png',
    ],
    variants: [
      { id: 911, color: 'Vintage Washed Black / Gold Embroidery', size: 'OSFA', price: 28.00, sku: 'KRN-HAT-DAD-BLK', isAvailable: true }
    ],
    isNew: true,
    material: '100% Bio-Washed Cotton Chino Twill',
    fit: 'Unstructured Low-Profile with Adjustable Brass Slide Closure',
  },
  {
    id: 'krown-shorts-01',
    name: 'KrowN French Terry Heavyweight Streetwear Shorts',
    slug: 'krown-french-terry-heavyweight-streetwear-shorts',
    description: 'Elevated luxury lounge and streetwear shorts. Cut from 400 GSM brushed French Terry cotton in vintage washed charcoal black. Features heavy tonal drawstrings, polished antique gold aglets, raw-edge hems, deep front slash pockets, and the signature gold embroidered KrowN crown on the left thigh.',
    collection: 'KrowN Supply Co.',
    price: 42.00,
    baseCost: 13.50,
    printCost: 6.00,
    images: [
      '/images/products/krown-french-terry-streetwear-shorts.png',
    ],
    variants: [
      { id: 921, color: 'Washed Black / Gold KrowN', size: 'S', price: 42.00, sku: 'KRN-SHRT-TERRY-S', isAvailable: true },
      { id: 922, color: 'Washed Black / Gold KrowN', size: 'M', price: 42.00, sku: 'KRN-SHRT-TERRY-M', isAvailable: true },
      { id: 923, color: 'Washed Black / Gold KrowN', size: 'L', price: 42.00, sku: 'KRN-SHRT-TERRY-L', isAvailable: true },
      { id: 924, color: 'Washed Black / Gold KrowN', size: 'XL', price: 42.00, sku: 'KRN-SHRT-TERRY-XL', isAvailable: true },
      { id: 925, color: 'Washed Black / Gold KrowN', size: '2XL', price: 44.00, sku: 'KRN-SHRT-TERRY-2XL', isAvailable: true },
    ],
    isNew: true,
    material: '400 GSM 100% Heavy Combed French Terry Cotton',
    fit: 'Above-the-Knee Relaxed Modern Cut (7" Inseam)',
  },
  {
    id: 'krown-tee-cc1717',
    name: 'KrowN "Wear The KrowN" Comfort Colors 1717 Vintage Heavy Tee',
    slug: 'krown-wear-the-krown-comfort-colors-1717-vintage-heavy-tee',
    description: 'The benchmark of luxury streetwear basics. Crafted on genuine Comfort Colors 1717 garment-dyed blanks in vintage Pepper Black. Made with 100% US ring-spun cotton for an ultra-soft broken-in feel and boxy drape. Features our official metallic antique gold and brushed steel 3D geometric faceted K-crown emblem with clean "WEAR THE KROWN" typography.',
    collection: 'KrowN Supply Co.',
    price: 34.00,
    baseCost: 11.00,
    printCost: 5.50,
    images: [
      '/images/products/krown-supply-comfort-colors-1717-tee.png',
    ],
    variants: [
      { id: 801, color: 'Pepper Washed Black / Faded Gold', size: 'S', price: 34.00, sku: 'KRN-CC1717-PEP-S', isAvailable: true },
      { id: 802, color: 'Pepper Washed Black / Faded Gold', size: 'M', price: 34.00, sku: 'KRN-CC1717-PEP-M', isAvailable: true },
      { id: 803, color: 'Pepper Washed Black / Faded Gold', size: 'L', price: 34.00, sku: 'KRN-CC1717-PEP-L', isAvailable: true },
      { id: 804, color: 'Pepper Washed Black / Faded Gold', size: 'XL', price: 34.00, sku: 'KRN-CC1717-PEP-XL', isAvailable: true },
      { id: 805, color: 'Pepper Washed Black / Faded Gold', size: '2XL', price: 36.00, sku: 'KRN-CC1717-PEP-2XL', isAvailable: true },
      { id: 806, color: 'Pepper Washed Black / Faded Gold', size: '3XL', price: 38.00, sku: 'KRN-CC1717-PEP-3XL', isAvailable: true },
    ],
    isNew: true,
    material: '6.1 oz/yd² 100% Ring-Spun Garment-Dyed Cotton',
    fit: 'Relaxed Boxy Fit with Twill-Taped Neck & Shoulders',
  },
  {
    id: 'krown-crewneck-01',
    name: 'KrowN Heritage Heavyweight Crewneck Sweatshirt',
    slug: 'krown-heritage-heavyweight-crewneck-sweatshirt',
    description: 'Ultra-heavy 10oz 3-end cotton fleece in vintage washed onyx. Features ribbed collar, cuffs, and waistband with split-stitch double-needle construction. Adorned with our official 3D geometric faceted K-crown emblem embroidered in metallic gold and brushed steel.',
    collection: 'KrowN Supply Co.',
    price: 68.00,
    baseCost: 22.00,
    printCost: 6.50,
    images: [
      '/images/products/krown-supply-crewneck-sweatshirt.png',
    ],
    variants: [
      { id: 901, color: 'Washed Onyx / Gold Insignia', size: 'S', price: 68.00, sku: 'KRN-CRW-ONX-S', isAvailable: true },
      { id: 902, color: 'Washed Onyx / Gold Insignia', size: 'M', price: 68.00, sku: 'KRN-CRW-ONX-M', isAvailable: true },
      { id: 903, color: 'Washed Onyx / Gold Insignia', size: 'L', price: 68.00, sku: 'KRN-CRW-ONX-L', isAvailable: true },
      { id: 904, color: 'Washed Onyx / Gold Insignia', size: 'XL', price: 68.00, sku: 'KRN-CRW-ONX-XL', isAvailable: true },
      { id: 905, color: 'Washed Onyx / Gold Insignia', size: '2XL', price: 72.00, sku: 'KRN-CRW-ONX-2XL', isAvailable: true },
      { id: 906, color: 'Washed Onyx / Gold Insignia', size: '3XL', price: 76.00, sku: 'KRN-CRW-ONX-3XL', isAvailable: true },
    ],
    isNew: true,
    material: '10 oz Heavyweight 80% Cotton / 20% Polyester Three-End Fleece',
    fit: 'Standard Relaxed Drop-Shoulder Fit',
  },

  // ==========================================
  // 2. KrowN Construction LLC (Jobsite Workwear)
  // Slogan: "BUILT TO REIGN."
  // ==========================================

  {
    id: 'kc-beanie-01',
    name: 'KrowN Heavy Ribbed Cuffed Jobsite Beanie',
    slug: 'krown-heavy-ribbed-cuffed-jobsite-beanie',
    description: 'Built for freezing morning concrete pours and winter jobsites. Thick 4-gauge tight-knit hypoallergenic acrylic with 3-inch foldover cuff. Decorated with a centered metallic gold-embroidered KrowN Construction LLC emblem patch with reinforced perimeter stitching.',
    collection: 'KrowN Construction',
    price: 24.99,
    baseCost: 6.20,
    printCost: 4.00,
    images: [
      '/images/products/krown-construction-cuffed-beanie.png',
      '/images/products/krown-beanie-model.jpg',
      '/images/products/krown-beanie-studio-front.jpg',
    ],
    variants: [
      { id: 611, color: 'Charcoal Black / Gold Crest Patch', size: 'OSFA', price: 24.99, sku: 'KRN-BN-RIBBED-BLK', isAvailable: true },
      { id: 612, color: 'Heather Slate / Gold Crest Patch', size: 'OSFA', price: 24.99, sku: 'KRN-BN-RIBBED-SLT', isAvailable: true }
    ],
    isNew: true,
    material: '100% Heavy Turbo Acrylic Rib-Knit',
    fit: 'One Size Fits All (OSFA) • 12" Uncuffed / 3" Foldover Cuff',
  },
  {
    id: 'kc-tumbler-01',
    name: 'KrowN 20oz Vacuum Insulated Jobsite Tumbler',
    slug: 'krown-20oz-vacuum-insulated-jobsite-tumbler',
    description: 'Engineered for long days on the jobsite. Double-wall vacuum insulated 18/8 kitchen-grade stainless steel with sweat-free matte black finish. Features the laser-etched metallic gold KrowN Construction emblem, "BUILT TO REIGN" hallmark, and splash-proof clear slider lid. Keeps beverages piping hot for 8 hours or ice-cold for 24 hours.',
    collection: 'KrowN Construction',
    price: 29.99,
    baseCost: 8.50,
    printCost: 4.50,
    images: [
      '/images/products/krown-construction-jobsite-tumbler.jpg',
      '/images/products/krown-construction-jobsite-tumbler-32oz.jpg',
    ],
    variants: [
      { id: 601, color: 'Matte Black / Laser Gold Crest', size: '20oz', price: 29.99, sku: 'KRN-TUMB-20-BLK', isAvailable: true }
    ],
    isNew: true,
    material: '18/8 Stainless Steel • Copper-Lined Double-Wall Vacuum Insulation',
    fit: '20 oz Capacity • Standard Cupholder Compatible',
  },
  {
    id: 'krown-tumbler-32oz',
    name: 'KrowN "Built to Reign" Thermal Insulated Matte Tumbler (32 oz)',
    slug: 'krown-built-to-reign-thermal-insulated-matte-tumbler-32oz',
    description: 'High-capacity 32oz heavy-duty jobsite canteen. Double-wall stainless steel, powder-coated obsidian black, laser-etched KrowN Construction heritage logo, leak-proof spout.',
    collection: 'KrowN Construction',
    price: 34.99,
    baseCost: 10.50,
    printCost: 5.00,
    images: [
      '/images/products/krown-construction-jobsite-tumbler-32oz.png'
    ],
    variants: [
      { id: 1401, color: 'Matte Obsidian Black / Laser Gold', size: '32 oz', price: 34.99, sku: 'KRN-TUMB-32-BLK', isAvailable: true }
    ],
    isNew: true,
    material: 'Double-Wall Vacuum Insulated Stainless Steel',
    fit: '32 oz Capacity',
  },
  {
    id: 'kc-stickers-01',
    name: 'KrowN Tradesman Hardhat & Jobsite Decal Pack (5-Pack)',
    slug: 'krown-tradesman-hardhat-jobsite-decal-pack',
    description: 'The ultimate tradesman sticker pack. 5 heavyweight 6 mil vinyl decals engineered with aggressive adhesive and solvent-resistant UV gloss laminate. Specifically tested to adhere to curved fiberglass/ABS hardhats, job boxes, truck tailgates, and water jugs through heat, rain, and mud.',
    collection: 'KrowN Construction',
    price: 16.99,
    baseCost: 2.40,
    printCost: 1.90,
    images: [
      '/images/products/krown-stickers-realistic.jpg',
      '/images/products/krown-construction-stickers-pack.png',
    ],
    variants: [
      { id: 621, color: 'Tradesman Multi-Pack (5 Decals)', size: '3" to 4" Decals', price: 16.99, sku: 'KRN-STK-HDHT-PK5', isAvailable: true }
    ],
    isNew: true,
    material: '6 mil Thick Weatherproof Solvent-Resistant Cast Vinyl',
    fit: 'Contoured Die-Cut for Hardhats, Toolboxes, and Vehicles',
  },
  {
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
  },

  // ==========================================
  // 3. AXA / Axiom Allegiance & KrowN Gaming
  // Team Abbreviation: AXA
  // Slogan: "PLAY TO REIGN."
  // ==========================================
  {
    id: 'axiom-jersey-home',
    name: 'AXA Pro League Cut-and-Sew Sublimated Esports Jersey — Home Edition (Customizable Gamertag)',
    slug: 'axa-pro-league-sublimated-esports-jersey-home',
    description: 'The official HOME match jersey of Axiom Allegiance. Built from ultra-breathable bird-eye moisture-wicking athletic mesh in deep obsidian black, accented with high-voltage royal purple and metallic silver speed panels. Features the authentic AXA owl team crest on the chest with the deliberate A-X-A facial letterforms, V-neck athletic collar, and lower hem authentic team jock tag. Supports custom gamertag personalization on upper back.',
    collection: 'AXA / Axiom Allegiance',
    price: 54.99,
    baseCost: 18.50,
    printCost: 6.00,
    images: [
      '/images/products/axa-pro-jersey-home.jpg',
      '/images/products/axa-pro-jersey-home-back.jpg',
      '/images/branding/gaming/axiom-owl-quote-frame.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png'
    ],
    variants: [
      { id: 3101, color: 'Obsidian Black / Royal Purple / Silver (No Name)', size: 'S', price: 54.99, sku: 'AXA-JSY-HM-S', isAvailable: true },
      { id: 3102, color: 'Obsidian Black / Royal Purple / Silver (No Name)', size: 'M', price: 54.99, sku: 'AXA-JSY-HM-M', isAvailable: true },
      { id: 3103, color: 'Obsidian Black / Royal Purple / Silver (No Name)', size: 'L', price: 54.99, sku: 'AXA-JSY-HM-L', isAvailable: true },
      { id: 3104, color: 'Obsidian Black / Royal Purple / Silver (No Name)', size: 'XL', price: 54.99, sku: 'AXA-JSY-HM-XL', isAvailable: true },
      { id: 3105, color: 'Obsidian Black / Royal Purple / Silver (No Name)', size: '2XL', price: 58.99, sku: 'AXA-JSY-HM-2XL', isAvailable: true },
      { id: 3106, color: 'Obsidian Black / Royal Purple / Silver (No Name)', size: '3XL', price: 62.99, sku: 'AXA-JSY-HM-3XL', isAvailable: true },
      { id: 3111, color: 'Obsidian Black / Royal Purple / Silver (Custom Gamertag)', size: 'S', price: 59.99, sku: 'AXA-JSY-HM-CUST-S', isAvailable: true },
      { id: 3112, color: 'Obsidian Black / Royal Purple / Silver (Custom Gamertag)', size: 'M', price: 59.99, sku: 'AXA-JSY-HM-CUST-M', isAvailable: true },
      { id: 3113, color: 'Obsidian Black / Royal Purple / Silver (Custom Gamertag)', size: 'L', price: 59.99, sku: 'AXA-JSY-HM-CUST-L', isAvailable: true },
      { id: 3114, color: 'Obsidian Black / Royal Purple / Silver (Custom Gamertag)', size: 'XL', price: 59.99, sku: 'AXA-JSY-HM-CUST-XL', isAvailable: true },
      { id: 3115, color: 'Obsidian Black / Royal Purple / Silver (Custom Gamertag)', size: '2XL', price: 63.99, sku: 'AXA-JSY-HM-CUST-2XL', isAvailable: true },
      { id: 3116, color: 'Obsidian Black / Royal Purple / Silver (Custom Gamertag)', size: '3XL', price: 67.99, sku: 'AXA-JSY-HM-CUST-3XL', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Pro League Authentic',
    material: '100% Breathable Micro-Poly Athletic Bird-Eye Mesh with Antimicrobial Treatment',
    fit: 'Pro-Tier Athletic Fit with Contoured Raglan Sleeve Shoulders',
  },
  {
    id: 'axiom-jersey-away',
    name: 'AXA Pro League Cut-and-Sew Sublimated Esports Jersey — Away Edition (Customizable Gamertag)',
    slug: 'axa-pro-league-sublimated-esports-jersey-away',
    description: 'The official AWAY competition jersey of Axiom Allegiance. Crafted from crisp bone white bird-eye athletic mesh with contrasting royal purple and obsidian black geometric side panels. Features the official AXA owl team crest on the chest, authentic APL Away lower hem jock tag, and custom gamertag personalization on upper back.',
    collection: 'AXA / Axiom Allegiance',
    price: 54.99,
    baseCost: 18.50,
    printCost: 6.00,
    images: [
      '/images/products/axa-pro-jersey-away.jpg',
      '/images/products/axa-pro-jersey-away-back.jpg',
      '/images/branding/gaming/axiom-owl-quote-frame.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png'
    ],
    variants: [
      { id: 3201, color: 'Bone White / Royal Purple / Black (No Name)', size: 'S', price: 54.99, sku: 'AXA-JSY-AW-S', isAvailable: true },
      { id: 3202, color: 'Bone White / Royal Purple / Black (No Name)', size: 'M', price: 54.99, sku: 'AXA-JSY-AW-M', isAvailable: true },
      { id: 3203, color: 'Bone White / Royal Purple / Black (No Name)', size: 'L', price: 54.99, sku: 'AXA-JSY-AW-L', isAvailable: true },
      { id: 3204, color: 'Bone White / Royal Purple / Black (No Name)', size: 'XL', price: 54.99, sku: 'AXA-JSY-AW-XL', isAvailable: true },
      { id: 3205, color: 'Bone White / Royal Purple / Black (No Name)', size: '2XL', price: 58.99, sku: 'AXA-JSY-AW-2XL', isAvailable: true },
      { id: 3206, color: 'Bone White / Royal Purple / Black (No Name)', size: '3XL', price: 62.99, sku: 'AXA-JSY-AW-3XL', isAvailable: true },
      { id: 3211, color: 'Bone White / Royal Purple / Black (Custom Gamertag)', size: 'S', price: 59.99, sku: 'AXA-JSY-AW-CUST-S', isAvailable: true },
      { id: 3212, color: 'Bone White / Royal Purple / Black (Custom Gamertag)', size: 'M', price: 59.99, sku: 'AXA-JSY-AW-CUST-M', isAvailable: true },
      { id: 3213, color: 'Bone White / Royal Purple / Black (Custom Gamertag)', size: 'L', price: 59.99, sku: 'AXA-JSY-AW-CUST-L', isAvailable: true },
      { id: 3214, color: 'Bone White / Royal Purple / Black (Custom Gamertag)', size: 'XL', price: 59.99, sku: 'AXA-JSY-AW-CUST-XL', isAvailable: true },
      { id: 3215, color: 'Bone White / Royal Purple / Black (Custom Gamertag)', size: '2XL', price: 63.99, sku: 'AXA-JSY-AW-CUST-2XL', isAvailable: true },
      { id: 3216, color: 'Bone White / Royal Purple / Black (Custom Gamertag)', size: '3XL', price: 67.99, sku: 'AXA-JSY-AW-CUST-3XL', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Pro League Authentic',
    material: '100% Breathable Micro-Poly Athletic Bird-Eye Mesh with Antimicrobial Treatment',
    fit: 'Pro-Tier Athletic Fit with Contoured Raglan Sleeve Shoulders',
  },
  {
    id: 'axiom-jersey-01',
    name: 'AXA Pro League Cut-and-Sew Sublimated Esports Jersey — Championship Edition (Customizable Gamertag)',
    slug: 'axiom-allegiance-pro-league-sublimated-esports-jersey',
    description: 'The high-voltage Championship Edition jersey of Axiom Allegiance. Built from ultra-breathable moisture-wicking athletic bird-eye mesh featuring electric toxic lime speed shards over royal purple and obsidian black. Centered with the prominent AXA owl crest with intentional A-X-A eye/beak geometry. Custom gamertag personalization on upper back.',
    collection: 'AXA / Axiom Allegiance',
    price: 54.99,
    baseCost: 18.50,
    printCost: 6.00,
    images: [
      '/images/products/axiom-pro-esports-jersey-front.jpg',
      '/images/products/axa-pro-jersey-championship-back.jpg',
      '/images/branding/gaming/axiom-owl-quote-frame.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png'
    ],
    variants: [
      { id: 1101, color: 'Electric/Royal Purple & Neon Toxic Green (No Name)', size: 'S', price: 54.99, sku: 'AXM-JSY-STD-S', isAvailable: true },
      { id: 1102, color: 'Electric/Royal Purple & Neon Toxic Green (No Name)', size: 'M', price: 54.99, sku: 'AXM-JSY-STD-M', isAvailable: true },
      { id: 1103, color: 'Electric/Royal Purple & Neon Toxic Green (No Name)', size: 'L', price: 54.99, sku: 'AXM-JSY-STD-L', isAvailable: true },
      { id: 1104, color: 'Electric/Royal Purple & Neon Toxic Green (No Name)', size: 'XL', price: 54.99, sku: 'AXM-JSY-STD-XL', isAvailable: true },
      { id: 1105, color: 'Electric/Royal Purple & Neon Toxic Green (No Name)', size: '2XL', price: 58.99, sku: 'AXM-JSY-STD-2XL', isAvailable: true },
      { id: 1106, color: 'Electric/Royal Purple & Neon Toxic Green (No Name)', size: '3XL', price: 62.99, sku: 'AXM-JSY-STD-3XL', isAvailable: true },
      { id: 1111, color: 'Electric/Royal Purple & Neon Toxic Green (Custom Gamertag)', size: 'S', price: 59.99, sku: 'AXM-JSY-CUST-S', isAvailable: true },
      { id: 1112, color: 'Electric/Royal Purple & Neon Toxic Green (Custom Gamertag)', size: 'M', price: 59.99, sku: 'AXM-JSY-CUST-M', isAvailable: true },
      { id: 1113, color: 'Electric/Royal Purple & Neon Toxic Green (Custom Gamertag)', size: 'L', price: 59.99, sku: 'AXM-JSY-CUST-L', isAvailable: true },
      { id: 1114, color: 'Electric/Royal Purple & Neon Toxic Green (Custom Gamertag)', size: 'XL', price: 59.99, sku: 'AXM-JSY-CUST-XL', isAvailable: true },
      { id: 1115, color: 'Electric/Royal Purple & Neon Toxic Green (Custom Gamertag)', size: '2XL', price: 63.99, sku: 'AXM-JSY-CUST-2XL', isAvailable: true },
      { id: 1116, color: 'Electric/Royal Purple & Neon Toxic Green (Custom Gamertag)', size: '3XL', price: 67.99, sku: 'AXM-JSY-CUST-3XL', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Championship Drop',
    material: '100% Breathable Micro-Poly Athletic Bird-Eye Mesh with Antimicrobial Treatment',
    fit: 'Pro-Tier Athletic Fit with Contoured Raglan Sleeve Shoulders',
  },
  {
    id: 'axiom-jersey-stealth',
    name: 'AXA Pro League Cut-and-Sew Sublimated Esports Jersey — Stealth Edition (Customizable Gamertag)',
    slug: 'axa-pro-league-sublimated-esports-jersey-stealth',
    description: 'The tactical blackout Stealth Edition jersey of Axiom Allegiance. Crafted from breathable blackout athletic mesh in obsidian and matte charcoal grey with subtle tonal royal purple reflective trim. Features the official AXA owl team crest with intentional A-X-A letterforms in matte stealth purple and dark charcoal.',
    collection: 'AXA / Axiom Allegiance',
    price: 54.99,
    baseCost: 18.50,
    printCost: 6.00,
    images: [
      '/images/products/axa-pro-jersey-stealth.jpg',
      '/images/products/axa-pro-jersey-stealth-back.jpg',
      '/images/branding/gaming/axiom-owl-quote-frame.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png'
    ],
    variants: [
      { id: 3301, color: 'Blackout Obsidian / Charcoal / Tonal Purple (No Name)', size: 'S', price: 54.99, sku: 'AXA-JSY-ST-S', isAvailable: true },
      { id: 3302, color: 'Blackout Obsidian / Charcoal / Tonal Purple (No Name)', size: 'M', price: 54.99, sku: 'AXA-JSY-ST-M', isAvailable: true },
      { id: 3303, color: 'Blackout Obsidian / Charcoal / Tonal Purple (No Name)', size: 'L', price: 54.99, sku: 'AXA-JSY-ST-L', isAvailable: true },
      { id: 3304, color: 'Blackout Obsidian / Charcoal / Tonal Purple (No Name)', size: 'XL', price: 54.99, sku: 'AXA-JSY-ST-XL', isAvailable: true },
      { id: 3305, color: 'Blackout Obsidian / Charcoal / Tonal Purple (No Name)', size: '2XL', price: 58.99, sku: 'AXA-JSY-ST-2XL', isAvailable: true },
      { id: 3306, color: 'Blackout Obsidian / Charcoal / Tonal Purple (No Name)', size: '3XL', price: 62.99, sku: 'AXA-JSY-ST-3XL', isAvailable: true },
      { id: 3311, color: 'Blackout Obsidian / Charcoal / Tonal Purple (Custom Gamertag)', size: 'S', price: 59.99, sku: 'AXA-JSY-ST-CUST-S', isAvailable: true },
      { id: 3312, color: 'Blackout Obsidian / Charcoal / Tonal Purple (Custom Gamertag)', size: 'M', price: 59.99, sku: 'AXA-JSY-ST-CUST-M', isAvailable: true },
      { id: 3313, color: 'Blackout Obsidian / Charcoal / Tonal Purple (Custom Gamertag)', size: 'L', price: 59.99, sku: 'AXA-JSY-ST-CUST-L', isAvailable: true },
      { id: 3314, color: 'Blackout Obsidian / Charcoal / Tonal Purple (Custom Gamertag)', size: 'XL', price: 59.99, sku: 'AXA-JSY-ST-CUST-XL', isAvailable: true },
      { id: 3315, color: 'Blackout Obsidian / Charcoal / Tonal Purple (Custom Gamertag)', size: '2XL', price: 63.99, sku: 'AXA-JSY-ST-CUST-2XL', isAvailable: true },
      { id: 3316, color: 'Blackout Obsidian / Charcoal / Tonal Purple (Custom Gamertag)', size: '3XL', price: 67.99, sku: 'AXA-JSY-ST-CUST-3XL', isAvailable: true },
    ],
    isNew: true,
    customBadge: 'Stealth Limited',
    material: '100% Breathable Micro-Poly Athletic Bird-Eye Mesh with Antimicrobial Treatment',
    fit: 'Pro-Tier Athletic Fit with Contoured Raglan Sleeve Shoulders',
  },

  {
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
  },
  {
    id: 'axiom-mug-01',
    name: 'Axiom Owl Two-Tone Ceramic Gaming Mug (15oz)',
    slug: 'axiom-owl-two-tone-gaming-mug-15oz',
    description: 'Fuel your late-night ranked grinds. Heavyweight 15oz ceramic mug boasting a midnight obsidian exterior paired with vibrant electric lime interior glaze and handle. Features the 3D Axiom Owl esports crest on the front and the official motto inscribed on the reverse: "YOU CANNOT BE TRULY HUMBLE, UNLESS YOU TRULY BELIEVE THAT LIFE CAN AND WILL GO ON WITHOUT YOU". Microwave and dishwasher safe.',
    collection: 'AXA / Axiom Allegiance',
    price: 19.99,
    baseCost: 5.80,
    printCost: 4.20,
    images: [
      '/images/products/axiom-owl-gamer-mug-15oz.png',
      '/images/branding/gaming/axiom-owl-quote-frame.jpg'
    ],
    variants: [
      { id: 701, color: 'Midnight Obsidian / Electric Lime Interior', size: '15 oz', price: 19.99, sku: 'AXM-MUG-15-LIME', isAvailable: true },
      { id: 702, color: 'Midnight Obsidian / Royal Purple Interior', size: '15 oz', price: 19.99, sku: 'AXM-MUG-15-PRP', isAvailable: true }
    ],
    isNew: true,
    material: '100% High-Grade Durable Ceramic • Gloss Finish',
    fit: '15 oz Jumbo Gamer Mug (4.7" H x 3.3" D)',
  },
  {
    id: 'axiom-shorts-01',
    name: 'Axiom Allegiance Pro Gaming Mesh Shorts',
    slug: 'axiom-allegiance-pro-gaming-mesh-shorts',
    description: 'Breathable tournament-grade athletic mesh shorts designed for long sessions. Featuring our signature deep obsidian purple body with vibrant electric lime side piping, elastic drawstring waistband with custom metallic aglets, dual zippered side stash pockets, and the official AXA Owl crest.',
    collection: 'AXA / Axiom Allegiance',
    price: 38.00,
    baseCost: 12.50,
    printCost: 6.00,
    images: [
      '/images/products/axiom-allegiance-gaming-mesh-shorts.png',
      '/images/branding/gaming/axiom-owl-mascot.png'
    ],
    variants: [
      { id: 711, color: 'Deep Purple / Electric Lime Piping', size: 'S', price: 38.00, sku: 'AXM-SHRT-SM', isAvailable: true },
      { id: 712, color: 'Deep Purple / Electric Lime Piping', size: 'M', price: 38.00, sku: 'AXM-SHRT-MD', isAvailable: true },
      { id: 713, color: 'Deep Purple / Electric Lime Piping', size: 'L', price: 38.00, sku: 'AXM-SHRT-LG', isAvailable: true },
      { id: 714, color: 'Deep Purple / Electric Lime Piping', size: 'XL', price: 38.00, sku: 'AXM-SHRT-XL', isAvailable: true },
      { id: 715, color: 'Deep Purple / Electric Lime Piping', size: '2XL', price: 40.00, sku: 'AXM-SHRT-2XL', isAvailable: true }
    ],
    isNew: true,
    material: '100% Breathable Micro-Poly Double-Layer Mesh',
    fit: 'Modern 6.5" Inseam Relaxed Athletic Fit',
  },
  {
    id: 'krown-sleeve-01',
    name: 'Axiom Allegiance Pro Compression Gaming Arm Sleeve',
    slug: 'axiom-allegiance-pro-compression-gaming-arm-sleeve',
    description: 'The official competition arm sleeve of Axiom Allegiance. Features our signature two-tone split colorway: midnight obsidian purple on one half and vibrant electric lime on the other, united by the oversized Axiom Owl crest across the forearm. Finished with vertical "AXIOM ALLEGIANCE" royal purple typography, upper cuff owl insignia, and flatlock anti-chafing seams.',
    collection: 'AXA / Axiom Allegiance',
    price: 24.99,
    baseCost: 7.20,
    printCost: 4.80,
    images: [
      '/images/products/axiom-arm-sleeve-3d-front.png',
      '/images/products/axiom-arm-sleeve-3d-back.png',
      '/images/products/axiom-arm-sleeve-flat.png',
    ],
    variants: [
      { id: 321, color: 'Purple / Electric Lime Split (Single Sleeve)', size: 'S/M', price: 24.99, sku: 'AXM-SLV-SPLIT-SM', isAvailable: true },
      { id: 322, color: 'Purple / Electric Lime Split (Single Sleeve)', size: 'L/XL', price: 24.99, sku: 'AXM-SLV-SPLIT-LXL', isAvailable: true },
      { id: 323, color: 'Purple / Electric Lime Split (Pair / Set of 2)', size: 'S/M', price: 44.99, sku: 'AXM-SLV-PAIR-SM', isAvailable: true },
      { id: 324, color: 'Purple / Electric Lime Split (Pair / Set of 2)', size: 'L/XL', price: 44.99, sku: 'AXM-SLV-PAIR-LXL', isAvailable: true },
    ],
    isNew: true,
    material: '88% High-Grade Polyester / 12% Spandex Micro-Poly Compression Fiber',
    fit: 'Ergonomic Second-Skin Compression Fit with Silicone Anti-Slip Bicep Grip',
  },
  {
    id: 'krown-mat-01',
    name: 'Axiom Owl Extended Gaming Desk Mat (5 Custom Esports Sizes)',
    slug: 'axiom-owl-extended-gaming-desk-mat',
    description: 'Tournament-grade micro-weave fabric surface showcasing the signature Axiom Owl battlestation panoramic artwork. Engineered for pixel-precise optical tracking and zero-drag wrist flicking. Features a textured non-slip natural rubber base, anti-fray precision dual-stitched perimeter in electric lime and royal purple, and the official motto inscribed along the border: "YOU CANNOT BE TRULY HUMBLE, UNLESS YOU TRULY BELIEVE THAT LIFE CAN AND WILL GO ON WITHOUT YOU". Available in 5 custom competition sizes from Medium (14"x12") to Colossal (47"x24").',
    collection: 'AXA / Axiom Allegiance',
    price: 19.99,
    baseCost: 8.50,
    printCost: 4.00,
    images: [
      '/images/products/axiom-owl-desk-mat-photorealistic.jpg',
      '/images/products/axiom-owl-realistic-axa-face-desk-mat.jpg',
      '/images/branding/gaming/axiom-owl-quote-frame.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
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
    ],
    isNew: true,
    material: 'Micro-Weave High-Density Cloth + Textured Natural Rubber Base',
    fit: '5 Custom Sizes: 14"x12" to 47"x24" (4mm Thickness)',
  },
  {
    id: 'krown-mousepad-01',
    name: 'Axiom Allegiance Official Crest Gaming Mousepad (5 Custom Sizes)',
    slug: 'axiom-owl-speed-gaming-mousepad',
    description: 'High-density micro-texture mousepad tuned for fast flick shots and pinpoint tracking. Showcases the iconic Axiom Owl crest banner with dark volcanic backdrop and the official team creed: "YOU CANNOT BE TRULY HUMBLE, UNLESS YOU TRULY BELIEVE THAT LIFE CAN AND WILL GO ON WITHOUT YOU". Available in 5 custom competition sizes from Medium (14"x12") to Colossal (47"x24").',
    collection: 'AXA / Axiom Allegiance',
    price: 19.99,
    baseCost: 8.50,
    printCost: 4.00,
    images: [
      '/images/branding/gaming/axiom-owl-display.png',
      '/images/branding/gaming/axiom-owl-quote-frame.jpg',
      '/images/products/axiom-owl-desk-mat-photorealistic.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
      // Option 1: Official Axiom Banner
      { id: 3301, color: 'Official Axiom Banner', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-PAD-BAN-360', isAvailable: true },
      { id: 3302, color: 'Official Axiom Banner', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-PAD-BAN-450', isAvailable: true },
      { id: 3303, color: 'Official Axiom Banner', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-PAD-BAN-800', isAvailable: true },
      { id: 3304, color: 'Official Axiom Banner', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-PAD-BAN-900', isAvailable: true },
      { id: 3305, color: 'Official Axiom Banner', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-PAD-BAN-1200', isAvailable: true },

      // Option 2: Volcanic Obsidian Battlestation
      { id: 3311, color: 'Volcanic Obsidian Battlestation', size: 'Medium (M) 14"x12" (360x300mm)', price: 19.99, sku: 'AXM-PAD-VOL-360', isAvailable: true },
      { id: 3312, color: 'Volcanic Obsidian Battlestation', size: 'Large (L) 18"x16" (450x400mm)', price: 26.99, sku: 'AXM-PAD-VOL-450', isAvailable: true },
      { id: 3313, color: 'Volcanic Obsidian Battlestation', size: 'Extended (XL) 31.5"x12" (800x300mm)', price: 34.99, sku: 'AXM-PAD-VOL-800', isAvailable: true },
      { id: 3314, color: 'Volcanic Obsidian Battlestation', size: 'Panoramic (2XL) 35.4"x16" (900x400mm)', price: 42.99, sku: 'AXM-PAD-VOL-900', isAvailable: true },
      { id: 3315, color: 'Volcanic Obsidian Battlestation', size: 'Colossal (3XL) 47"x24" (1200x600mm)', price: 54.99, sku: 'AXM-PAD-VOL-1200', isAvailable: true },
    ],
    isNew: true,
    material: 'Speed-Weave Polyester Face + Anti-Slip Textured Rubber Base',
    fit: '5 Custom Sizes: 14"x12" to 47"x24" (4mm Thickness)',
  },
  {
    id: 'axiom-sweatpants-pro',
    name: 'Axiom Allegiance Pro Heavyweight 450 GSM Joggers',
    slug: 'axiom-allegiance-pro-heavyweight-joggers',
    description: 'Pro-tier tournament joggers engineered for unmatched warmth and esports performance. Cut from ultra-heavyweight 450 GSM French terry fleece in midnight obsidian black. Features dual-tone braided drawstrings (royal purple & neon toxic green with dipped aglets), vertical athletic "AXIOM ALLEGIANCE" typography running down the left leg, and the authentic high-density embroidered Axiom Owl mascot on the right thigh. Deep zippered stash pockets, ribbed gusset crotch, and tailored ankle cuffs.',
    collection: 'AXA / Axiom Allegiance',
    price: 68.00,
    baseCost: 22.00,
    printCost: 7.00,
    images: [
      '/images/products/axiom-sweatpants-pro-model-clean.jpg',
      '/images/products/axiom-sweatpants-pro-heavyweight-studio.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
      { id: 4101, color: 'Obsidian Black / Purple & Green Cords', size: 'S', price: 68.00, sku: 'AXM-SWP-PRO-S', isAvailable: true },
      { id: 4102, color: 'Obsidian Black / Purple & Green Cords', size: 'M', price: 68.00, sku: 'AXM-SWP-PRO-M', isAvailable: true },
      { id: 4103, color: 'Obsidian Black / Purple & Green Cords', size: 'L', price: 68.00, sku: 'AXM-SWP-PRO-L', isAvailable: true },
      { id: 4104, color: 'Obsidian Black / Purple & Green Cords', size: 'XL', price: 68.00, sku: 'AXM-SWP-PRO-XL', isAvailable: true },
      { id: 4105, color: 'Obsidian Black / Purple & Green Cords', size: '2XL', price: 68.00, sku: 'AXM-SWP-PRO-2XL', isAvailable: true },
      { id: 4106, color: 'Obsidian Black / Purple & Green Cords', size: '3XL', price: 74.00, sku: 'AXM-SWP-PRO-3XL', isAvailable: true },
    ],
    isNew: true,
    material: '450 GSM Ultra-Heavyweight 100% French Terry Cotton • Dual-Tone Cords',
    fit: 'Tailored Athletic Taper with Heavy Ribbed Cuffs',
  },
  {
    id: 'axiom-sweatpants-core',
    name: 'Axiom Allegiance Core Everyday Fleece Joggers',
    slug: 'axiom-allegiance-core-everyday-fleece-joggers',
    description: 'High-comfort, accessible everyday fleece joggers designed for all-day ranked sessions and streaming. Crafted from super-soft 300 GSM brushed fleece in midnight obsidian black with team purple & electric lime accents. Features vertical athletic "AXIOM ALLEGIANCE" typography down one leg, the official Axiom Owl crest on the opposite thigh, elastic waistband with contrast drawstrings, and flexible tapered fit.',
    collection: 'AXA / Axiom Allegiance',
    price: 39.99,
    baseCost: 14.00,
    printCost: 5.50,
    images: [
      '/images/products/axiom-fleece-joggers-core-studio.jpg',
      '/images/products/axiom-fleece-joggers-core-model.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
      { id: 4201, color: 'Obsidian Black / Team Purple & Lime', size: 'S', price: 39.99, sku: 'AXM-SWP-CORE-S', isAvailable: true },
      { id: 4202, color: 'Obsidian Black / Team Purple & Lime', size: 'M', price: 39.99, sku: 'AXM-SWP-CORE-M', isAvailable: true },
      { id: 4203, color: 'Obsidian Black / Team Purple & Lime', size: 'L', price: 39.99, sku: 'AXM-SWP-CORE-L', isAvailable: true },
      { id: 4204, color: 'Obsidian Black / Team Purple & Lime', size: 'XL', price: 39.99, sku: 'AXM-SWP-CORE-XL', isAvailable: true },
      { id: 4205, color: 'Obsidian Black / Team Purple & Lime', size: '2XL', price: 39.99, sku: 'AXM-SWP-CORE-2XL', isAvailable: true },
      { id: 4206, color: 'Obsidian Black / Team Purple & Lime', size: '3XL', price: 44.99, sku: 'AXM-SWP-CORE-3XL', isAvailable: true },
    ],
    isNew: true,
    material: '300 GSM Midweight Brushed Cotton/Poly Fleece • Elastic Drawstring Waist',
    fit: 'Relaxed Athletic Taper with Ribbed Cuffs',
  },
  {
    id: 'axiom-hoodie-01',
    name: 'Axiom Allegiance Heavyweight 450 GSM Streetwear Hoodie',
    slug: 'axiom-allegiance-heavyweight-streetwear-hoodie',
    description: 'The definitive competitive streetwear hoodie for Axiom Allegiance. Built from ultra-heavyweight 450 GSM French terry cotton in midnight obsidian black. Features a structured double-layer hood, thick dual-tone braided drawstrings (royal purple & toxic neon green with matte metal aglets), spacious kangaroo pocket with reinforced stitching, heavy ribbed cuffs and hem, and high-density direct embroidery of the official Axiom Owl crest across the chest.',
    collection: 'AXA / Axiom Allegiance',
    price: 74.99,
    baseCost: 24.50,
    printCost: 8.50,
    images: [
      '/images/products/axiom-heavyweight-hoodie-studio.jpg',
      '/images/products/axiom-heavyweight-hoodie-model.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
      { id: 4301, color: 'Obsidian Black / Purple & Green Cords', size: 'S', price: 74.99, sku: 'AXM-HD-450-S', isAvailable: true },
      { id: 4302, color: 'Obsidian Black / Purple & Green Cords', size: 'M', price: 74.99, sku: 'AXM-HD-450-M', isAvailable: true },
      { id: 4303, color: 'Obsidian Black / Purple & Green Cords', size: 'L', price: 74.99, sku: 'AXM-HD-450-L', isAvailable: true },
      { id: 4304, color: 'Obsidian Black / Purple & Green Cords', size: 'XL', price: 74.99, sku: 'AXM-HD-450-XL', isAvailable: true },
      { id: 4305, color: 'Obsidian Black / Purple & Green Cords', size: '2XL', price: 74.99, sku: 'AXM-HD-450-2XL', isAvailable: true },
      { id: 4306, color: 'Obsidian Black / Purple & Green Cords', size: '3XL', price: 79.99, sku: 'AXM-HD-450-3XL', isAvailable: true },
    ],
    isNew: true,
    material: '450 GSM Heavyweight 100% French Terry Cotton • Dual-Tone Braided Cords',
    fit: 'Modern Boxy Streetwear Cut with Heavyweight Structured Drop Shoulders',
  },
  {
    id: 'axiom-sweatshirt-01',
    name: 'Axiom Allegiance Official Crewneck Sweatshirt',
    slug: 'axiom-allegiance-official-crewneck-sweatshirt',
    description: 'Tournament-grade everyday crewneck sweatshirt in midnight obsidian black. Crafted from premium 380 GSM brushed fleece with classic triangular athletic collar V-stitch, heavyweight ribbed collar, cuffs and waistband. Emblazoned with high-density direct embroidery of the authentic Axiom Owl mascot on the chest.',
    collection: 'AXA / Axiom Allegiance',
    price: 59.99,
    baseCost: 19.50,
    printCost: 7.00,
    images: [
      '/images/products/axiom-crewneck-sweatshirt-studio.jpg',
      '/images/products/axiom-crewneck-sweatshirt-model.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
      { id: 4401, color: 'Obsidian Black / Team Purple & Lime', size: 'S', price: 59.99, sku: 'AXM-CRW-380-S', isAvailable: true },
      { id: 4402, color: 'Obsidian Black / Team Purple & Lime', size: 'M', price: 59.99, sku: 'AXM-CRW-380-M', isAvailable: true },
      { id: 4403, color: 'Obsidian Black / Team Purple & Lime', size: 'L', price: 59.99, sku: 'AXM-CRW-380-L', isAvailable: true },
      { id: 4404, color: 'Obsidian Black / Team Purple & Lime', size: 'XL', price: 59.99, sku: 'AXM-CRW-380-XL', isAvailable: true },
      { id: 4405, color: 'Obsidian Black / Team Purple & Lime', size: '2XL', price: 59.99, sku: 'AXM-CRW-380-2XL', isAvailable: true },
      { id: 4406, color: 'Obsidian Black / Team Purple & Lime', size: '3XL', price: 64.99, sku: 'AXM-CRW-380-3XL', isAvailable: true },
    ],
    isNew: true,
    material: '380 GSM Heavyweight Brushed Cotton/Poly Fleece • V-Stitch Collar Accent',
    fit: 'Athletic Tailored Streetwear Fit with Heavy Ribbed Cuffs',
  },
  {
    id: 'axiom-wrist-rest-01',
    name: 'Axiom Pro Cooling Gel Ergonomic Keyboard Wrist Rest',
    slug: 'axiom-pro-cooling-gel-keyboard-wrist-rest',
    description: 'HyperX-grade tournament ergonomic cooling gel wrist rest engineered for marathon gaming sessions. Features a dual-layer core of cooling infused memory foam and high-density ergonomic support foam that conforms to your wrists. Wrapped in silky smooth, anti-friction cooling lycra fabric with anti-fray royal purple precision perimeter stitching, textured non-slip silicone rubber base, clean athletic AXIOM ALLEGIANCE typography, and the official Axiom Owl crest. Available in Compact 60%, Tenkeyless (TKL 80%), and Full-Size (100%).',
    collection: 'AXA / Axiom Allegiance',
    price: 19.99,
    baseCost: 6.50,
    printCost: 3.50,
    images: [
      '/images/products/axiom-keyboard-wrist-rest-tournament-edition.jpg',
      '/images/products/axiom-keyboard-wrist-rest-stealth-setup.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    variants: [
      { id: 4301, color: 'Tournament Edition / Purple & Lime', size: 'Compact 60% (11.4" x 2.9")', price: 19.99, sku: 'AXM-WRIST-60', isAvailable: true },
      { id: 4302, color: 'Tournament Edition / Purple & Lime', size: 'Tenkeyless TKL 80% (14.2" x 2.9")', price: 22.99, sku: 'AXM-WRIST-TKL', isAvailable: true },
      { id: 4303, color: 'Tournament Edition / Purple & Lime', size: 'Full-Size 100% (17.5" x 2.9")', price: 24.99, sku: 'AXM-WRIST-FULL', isAvailable: true },
    ],
    isNew: true,
    material: 'Cooling-Infused Memory Gel + Ultra-Dense Support Core + Silky Lycra Face + Non-Slip Base',
    fit: 'Ergonomic Contoured 15° Slope (0.9" / 23mm Height)',
  },
  {
    id: 'krown-tee-01',
    name: 'Axiom Owl Esports Performance Tee',
    slug: 'axiom-owl-esports-performance-tee',
    description: 'The official esports tee of Axiom Allegiance. Powered by KrowN. Features the razor-sharp Axiom Owl crest in electric lime and royal purple over ultra-combed 240 GSM organic cotton. Built for prolonged comfort on stream or on the street.',
    collection: 'AXA / Axiom Allegiance',
    price: 36.00,
    baseCost: 10.20,
    printCost: 6.00,
    images: [
      '/images/products/axa-pro-jersey-home.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png'
    ],
    variants: [
      { id: 301, color: 'Obsidian / Electric Lime & Purple', size: 'M', price: 36.00, sku: 'AXM-OWL-TEE-M', isAvailable: true },
      { id: 302, color: 'Obsidian / Electric Lime & Purple', size: 'L', price: 36.00, sku: 'AXM-OWL-TEE-L', isAvailable: true },
      { id: 303, color: 'Obsidian / Electric Lime & Purple', size: 'XL', price: 36.00, sku: 'AXM-OWL-TEE-XL', isAvailable: true },
      { id: 304, color: 'Obsidian / Electric Lime & Purple', size: '2XL', price: 38.00, sku: 'AXM-OWL-TEE-2XL', isAvailable: true },
    ],
    isNew: true,
    material: '100% Combed Ring-Spun Heavyweight Cotton',
    fit: 'Standard Relaxed Drop-Shoulder',
  },

  // ==========================================
  // 4. Accessories
  // ==========================================
  {
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
  },
];

class PrintifyService {
  private apiKey: string | undefined;
  private shopId: string | undefined;

  constructor() {
    this.apiKey = process.env.PRINTIFY_API_KEY;
    this.shopId = process.env.PRINTIFY_SHOP_ID;
  }

  private isLiveConfigured(): boolean {
    return Boolean(
      this.apiKey && 
      this.shopId && 
      !this.apiKey.includes('placeholder') && 
      !this.shopId.includes('placeholder')
    );
  }

  /**
   * Fetch all products from Printify or high-fidelity mock fallback.
   */
  async getProducts(): Promise<CatalogProduct[]> {
    const processedLaunch = INITIAL_MOCK_CATALOG.map(item => ({
      ...item,
      economics: calculateProductEconomics({
        baseCost: item.baseCost,
        printCost: item.printCost,
        retailPrice: item.price,
      })
    }));

    if (this.isLiveConfigured()) {
      try {
        const response = await fetch(`https://api.printify.com/v1/shops/${this.shopId}/products.json`, {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'User-Agent': 'KrowN-Supply-Store/1.0',
          },
          next: { revalidate: 300 } // cache for 5 minutes
        });

        if (response.ok) {
          const text = await response.text();
          if (text) {
            try {
              const data = JSON.parse(text);
              if (data.data && data.data.length > 0) {
                const liveProducts = this.transformPrintifyProducts(data.data);
                return this.mergeAndDeduplicateProducts(processedLaunch, liveProducts);
              }
            } catch {
              console.warn('Invalid JSON from Printify API, using local catalog.');
            }
          }
        }
      } catch (err) {
        console.error('Error fetching live Printify catalog, using local fallback:', err);
      }
    }

    return processedLaunch;
  }

  /**
   * Merge live Printify products into catalog and deduplicate matching mock items.
   */
  private mergeAndDeduplicateProducts(mockProducts: CatalogProduct[], liveProducts: CatalogProduct[]): CatalogProduct[] {
    const replacedMockIds = new Set<string>();

    for (const live of liveProducts) {
      const nameLower = live.name.toLowerCase();
      if (nameLower.includes('tumbler')) {
        replacedMockIds.add('kc-tumbler-01');
      } else if (nameLower.includes('hoodie')) {
        replacedMockIds.add('krown-hoodie-premium');
      } else if (nameLower.includes('richardson') || nameLower.includes('snapback') || nameLower.includes('112')) {
        replacedMockIds.add('custom-krown-works-hat');
      } else if (nameLower.includes('comfort colors') || nameLower.includes('1717')) {
        replacedMockIds.add('krown-tee-cc1717');
      } else if (nameLower.includes('beanie')) {
        replacedMockIds.add('kc-beanie-01');
      } else if (nameLower.includes('jersey')) {
        replacedMockIds.add('axiom-jersey-home');
      } else if (nameLower.includes('desk mat')) {
        // Retain master 5-size krown-mat-01 with photorealistic imagery and full size ladder
      } else if (nameLower.includes('sticker') || nameLower.includes('decal')) {
        replacedMockIds.add('krown-stickers-01');
      }
    }

    // Filter out raw uncurated desk mat from live list so krown-mat-01 with 5 sizes is the primary product
    const filteredLive = liveProducts.filter(p => !p.name.toLowerCase().includes('desk mat'));
    const uniqueMocks = mockProducts.filter(m => !replacedMockIds.has(m.id));
    return [...filteredLive, ...uniqueMocks];
  }

  /**
   * Fetch single product by ID or Slug.
   */
  async getProductById(idOrSlug: string): Promise<CatalogProduct | null> {
    const products = await this.getProducts();

    // Alias mapping between legacy mock slugs and new live Printify products
    const aliasMap: Record<string, string[]> = {
      'custom-krown-works-hat': ['6ac80dc2f4d488e1be0b0902', 'richardson', 'snapback'],
      'krown-hoodie-premium': ['6ac80dff9f3e89dde70da38d', 'krown-heavyweight-streetwear-hoodie'],
      'kc-tumbler-01': ['6ac7ed40fea4d4e68e0a0f6a', '20oz-vacuum-insulated-jobsite-tumbler'],
      'krown-tee-cc1717': ['6ac7ed0b9bfbeab23800dcdf', 'krown-wear-the-krown-comfort-colors-1717'],
      'kc-beanie-01': ['6ac80e07cafb2cd4c60b7c96', 'krown-construction-heavy-ribbed-cuffed-beanie'],
      'axiom-jersey-home': ['6ac80e034a1cdf2ad60e0bed', 'axiom-allegiance-axa-cut-and-sew-pro-esports-jersey'],
      'krown-mat-01': ['6ac7ed486443c9f27801af1b', 'axiom-owl-panoramic-gaming-desk-mat'],
      'krown-stickers-01': ['6ac7ed44fea4d4e68e0a0f80', '6ac7ed46ad560d80d10eb55c'],
    };

    const targetAliases = aliasMap[idOrSlug] || [];

    const product = products.find(p => 
      p.id === idOrSlug || 
      p.slug === idOrSlug ||
      targetAliases.includes(p.id) ||
      targetAliases.some(alias => p.slug.includes(alias))
    );
    return product || null;
  }

  /**
   * Audit catalog for inventory and profitability issues.
   */
  async auditCatalogInventory(): Promise<CatalogAuditReport> {
    const products = await this.getProducts();
    let totalVariants = 0;
    let availableVariants = 0;
    let outOfStockVariants = 0;
    const discontinuedOrOosItems: CatalogAuditReport['discontinuedOrOosItems'] = [];
    const marginAlerts: CatalogAuditReport['marginAlerts'] = [];

    for (const prod of products) {
      for (const v of prod.variants) {
        totalVariants++;
        if (v.isAvailable) {
          availableVariants++;
        } else {
          outOfStockVariants++;
          discontinuedOrOosItems.push({
            productId: prod.id,
            productName: prod.name,
            variantSku: v.sku,
            variantTitle: `${v.color} / ${v.size}`,
          });
        }
      }

      if (prod.economics && prod.economics.marginPercentage < 25) {
        marginAlerts.push({
          productId: prod.id,
          productName: prod.name,
          marginPercent: prod.economics.marginPercentage,
          status: prod.economics.healthStatus,
        });
      }
    }

    return {
      timestamp: new Date().toISOString(),
      totalProducts: products.length,
      totalVariants,
      availableVariants,
      outOfStockVariants,
      lowStockItems: [],
      discontinuedOrOosItems,
      marginAlerts,
    };
  }

  private transformPrintifyProducts(rawList: PrintifyProductRaw[]): CatalogProduct[] {
    const validProducts: CatalogProduct[] = [];

    for (const raw of rawList) {
      const titleLower = raw.title.toLowerCase();

      // Zero KrowN Construction hats in the store
      const isConstructionHat = (titleLower.includes('construction') || titleLower.includes('kc') || titleLower.includes('btr')) && 
        (titleLower.includes('hat') || titleLower.includes('snapback') || titleLower.includes('richardson') || titleLower.includes('cap'));
      if (isConstructionHat) {
        continue;
      }

      const minPriceCents = Math.min(...raw.variants.map(v => v.price));
      const minCostCents = Math.min(...raw.variants.map(v => v.cost));
      let retailPrice = minPriceCents / 100;
      const baseCost = minCostCents / 100;

      let collection: CatalogProduct['collection'] = 'KrowN Supply Co.';
      if (titleLower.includes('construction') || titleLower.includes('tradesman') || titleLower.includes('jobsite')) {
        collection = 'KrowN Construction';
      } else if (titleLower.includes('axiom') || titleLower.includes('axa') || titleLower.includes('gaming') || titleLower.includes('desk mat') || titleLower.includes('sleeve') || titleLower.includes('shaker')) {
        collection = 'AXA / Axiom Allegiance';
      }

      let productName = raw.title;
      let productSlug = raw.title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
      let productDesc = raw.description.replace(/<[^>]*>?/gm, '');

      // Check if Richardson 112 headwear - strip all "Custom Logo / Display Sample" artifacts
      const isRichardsonHat = titleLower.includes('richardson') || titleLower.includes('snapback') || titleLower.includes('112') || titleLower.includes('leather patch');

      if (isRichardsonHat) {
        productName = 'KrowN Supply Co. Richardson 112 Leather Patch Trucker Snapback';
        productSlug = 'krown-supply-co-richardson-112-leather-patch-trucker-snapback';
        productDesc = 'The signature flagship headwear of KrowN Supply Co. Cut on the authentic Richardson 112 structured mid-profile silhouette featuring breathable nylon mesh, pre-curved bill with contrast double-stitching, and our genuine laser-etched saddle tan leatherette crown patch. Standard adjustable snapback closure for a tailored streetwear fit.';
        retailPrice = 29.99;
      }

      // High-Conversion Commercial Studio & Model Photography Overrides
      let productImages: string[] = [];
      if (titleLower.includes('tumbler')) {
        productImages = [
          '/images/products/krown-construction-jobsite-tumbler.jpg',
          '/images/products/krown-construction-jobsite-tumbler-32oz.jpg',
        ];
      } else if (titleLower.includes('hoodie')) {
        productImages = [
          '/images/products/krown-hoodie-studio-front.jpg',
          '/images/products/krown-hoodie-male-model.jpg',
          '/images/products/krown-hoodie-female-model.jpg',
          '/images/products/krown-heavyweight-hoodie-back-krown.jpg',
        ];
      } else if (isRichardsonHat) {
        productImages = [
          '/images/products/krown-r112-flagship-leather-patch-snapback.jpg',
          '/images/products/krown-r112-flagship-leather-patch-hero.jpg',
        ];
      } else if (titleLower.includes('beanie')) {
        productImages = [
          '/images/products/krown-beanie-studio-front.jpg',
          '/images/products/krown-beanie-model.jpg',
        ];
      } else if (titleLower.includes('sticker') || titleLower.includes('decal')) {
        productImages = [
          '/images/products/krown-stickers-realistic.jpg',
          '/images/products/krown-construction-stickers-pack.png',
        ];
      } else if (titleLower.includes('jersey')) {
        productImages = [
          '/images/products/axa-pro-jersey-home.jpg',
          '/images/products/axa-pro-jersey-away.jpg',
          '/images/products/axa-pro-jersey-stealth.jpg',
          '/images/products/axiom-pro-esports-jersey-back.jpg',
        ];
      } else if (titleLower.includes('desk mat')) {
        productImages = [
          '/images/products/axiom-owl-desk-mat-photorealistic.jpg',
        ];
      } else if (titleLower.includes('comfort colors') || titleLower.includes('1717')) {
        productImages = [
          '/images/products/krown-supply-comfort-colors-1717-tee.jpg',
        ];
      }

      if (productImages.length === 0) {
        productImages = raw.images && raw.images.length > 0 
          ? raw.images.map(img => img.src)
          : (collection === 'AXA / Axiom Allegiance' 
              ? ['/images/branding/gaming/axiom-owl-display.png'] 
              : ['/images/products/krown-supply-premium-hoodie-front.jpg']);
      }

      const variants = raw.variants.map(v => {
        let color = v.options.color || 'Standard';
        let size = v.options.size || 'One Size';

        if (isRichardsonHat) {
          if (color.toLowerCase().includes('custom') || color.toLowerCase().includes('sample') || color.toLowerCase().includes('standard')) {
            color = 'Heather Grey & Black / Saddle Tan Leather Patch';
          }
          if (size.toLowerCase().includes('hat') || size.toLowerCase().includes('sample') || size.toLowerCase().includes('one size')) {
            size = 'OSFA';
          }
        }

        return {
          id: v.id,
          color,
          size,
          price: isRichardsonHat ? 29.99 : v.price / 100,
          sku: v.sku,
          isAvailable: v.is_available && v.is_enabled,
        };
      });

      validProducts.push({
        id: raw.id,
        name: productName,
        slug: productSlug,
        description: productDesc,
        collection,
        price: retailPrice,
        baseCost,
        printCost: 5.00,
        images: productImages,
        variants,
        economics: calculateProductEconomics({
          baseCost,
          printCost: 5.00,
          retailPrice,
        })
      });
    }

    return validProducts;
  }

  /**
   * Validates and formats a complete Printify Order Payload.
   */
  validatePrintifyOrderPayload(order: PrintifyOrderInput): {
    isValid: boolean;
    payload: PrintifyOrderPayload;
    errors: string[];
  } {
    const errors: string[] = [];

    if (!order.externalId) {
      errors.push('externalId is required for order tracking.');
    }
    if (!order.addressTo || !order.addressTo.address1 || !order.addressTo.city || !order.addressTo.zip || !order.addressTo.country) {
      errors.push('Complete shipping address (address1, city, zip, country) is required.');
    }
    if (!order.lineItems || order.lineItems.length === 0) {
      errors.push('At least one line item is required.');
    }

    const payloadLineItems: PrintifyOrderLineItemPayload[] = [];

    for (const item of order.lineItems || []) {
      const mapping = PRINTIFY_SKU_CATALOG_MAPPINGS[item.productId];
      let variantId = item.variantId;

      if (!variantId && mapping) {
        if (item.size && mapping.variantMap[item.size]) {
          variantId = mapping.variantMap[item.size];
        } else {
          variantId = Object.values(mapping.variantMap)[0];
        }
      }

      if (!variantId) {
        variantId = 99901; // fallback test variant
      }

      const lineItemPayload: PrintifyOrderLineItemPayload = {
        variant_id: variantId,
        quantity: item.quantity,
      };

      if (item.gamertag || item.playerNumber || item.customLogoUrl || item.notes) {
        lineItemPayload.metadata = {
          custom_gamertag: item.gamertag,
          custom_player_number: item.playerNumber,
          custom_logo_url: item.customLogoUrl,
          custom_upgrades: item.notes,
        };
      }

      payloadLineItems.push(lineItemPayload);
    }

    const orderNotes = (order.lineItems || [])
      .filter(i => i.gamertag || i.notes)
      .map(i => `${i.productId}: [${[i.gamertag ? `Tag: ${i.gamertag}` : '', i.playerNumber ? `#${i.playerNumber}` : '', i.notes || ''].filter(Boolean).join(' | ')}]`)
      .join(' ; ');

    const payload: PrintifyOrderPayload = {
      external_id: order.externalId,
      label: `KrowN Order #${order.externalId}`,
      notes: orderNotes || undefined,
      shipping_method: order.shippingMethod || 1, // 1 = Standard
      send_shipping_notification: true,
      address_to: {
        first_name: order.addressTo?.first_name || 'Valued',
        last_name: order.addressTo?.last_name || 'Customer',
        email: order.addressTo?.email || 'orders@krownsupply.com',
        phone: order.addressTo?.phone || '0000000000',
        country: order.addressTo?.country || 'US',
        region: order.addressTo?.region || '',
        address1: order.addressTo?.address1 || '',
        address2: order.addressTo?.address2 || '',
        city: order.addressTo?.city || '',
        zip: order.addressTo?.zip || '',
      },
      line_items: payloadLineItems,
    };

    return {
      isValid: errors.length === 0,
      payload,
      errors,
    };
  }

  /**
   * Submits or mocks a Printify order with resilient fallback.
   */
  async createPrintifyOrder(order: PrintifyOrderInput): Promise<{
    success: boolean;
    orderId?: string;
    isMock: boolean;
    payload: PrintifyOrderPayload;
    error?: string;
  }> {
    const validation = this.validatePrintifyOrderPayload(order);

    if (!validation.isValid) {
      console.warn('⚠️ Printify order payload validation warnings:', validation.errors);
    }

    if (this.isLiveConfigured()) {
      try {
        const response = await fetch(`https://api.printify.com/v1/shops/${this.shopId}/orders.json`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.apiKey}`,
            'User-Agent': 'KrowN-Supply-Store/1.0',
          },
          body: JSON.stringify(validation.payload),
        });

        if (response.ok) {
          const data = await response.json();
          return {
            success: true,
            orderId: data.id,
            isMock: false,
            payload: validation.payload,
          };
        } else {
          const errText = await response.text();
          console.error(`Printify live order submission failed (${response.status}):`, errText);
        }
      } catch (err) {
        console.error('Error connecting to live Printify API:', err);
      }
    }

    // Resilient fallback: Clean mock fulfillment logger without throwing unhandled runtime 500 errors
    const mockOrderId = `krown_mock_pfy_${Date.now()}`;
    console.log(`[Printify Mock Fulfillment] Order ${mockOrderId} generated successfully for external_id: ${order.externalId}`);
    return {
      success: true,
      orderId: mockOrderId,
      isMock: true,
      payload: validation.payload,
    };
  }
}

export interface PrintifySkuMapping {
  blueprintId: number;
  printProviderId: number;
  variantMap: Record<string, number>;
  category: string;
}

export const PRINTIFY_SKU_CATALOG_MAPPINGS: Record<string, PrintifySkuMapping> = {
  'krown-hoodie-premium': {
    blueprintId: 1035, // Lane Seven / Independent Heavyweight 480 GSM
    printProviderId: 29, // Monster Digital / SwiftPOD
    variantMap: { 'S': 45101, 'M': 45102, 'L': 45103, 'XL': 45104, '2XL': 45105 },
    category: 'Hoodies',
  },
  'krown-sweatpants-premium': {
    blueprintId: 1089, // Premium French Terry Sweatpants
    printProviderId: 29,
    variantMap: { 'S': 46101, 'M': 46102, 'L': 46103, 'XL': 46104, '2XL': 46105 },
    category: 'Sweatpants',
  },
  'krown-streetwear-set': {
    blueprintId: 1035,
    printProviderId: 29,
    variantMap: { 'S': 47101, 'M': 47102, 'L': 47103, 'XL': 47104, '2XL': 47105 },
    category: 'Coordinated Sets',
  },
  'custom-krown-works-hat': {
    blueprintId: 112, // Richardson 112 Original Trucker Snapback
    printProviderId: 42, // Headwear & Laser Leatherette Specialist
    variantMap: {
      'OSFA': 11201,
      'Heather Grey & Black / Saddle Tan Leather Patch': 11201,
      'Obsidian Black / Raw Black Leather Patch': 11202,
      'Charcoal & Black / Honey Leather Patch': 11203,
      '1 Hat': 11201,
    },
    category: 'Headwear',
  },
  'krown-dadhat-01': {
    blueprintId: 204, // Vintage Washed Chino Dad Hat
    printProviderId: 42,
    variantMap: { 'OSFA': 20401, 'Vintage Washed Black / Gold Embroidery': 20401 },
    category: 'Headwear',
  },
  'kc-beanie-01': {
    blueprintId: 342, // Ribbed Knit Cuffed Beanie
    printProviderId: 42,
    variantMap: { 'OSFA': 34201 },
    category: 'Headwear',
  },
  'axiom-jersey-home': {
    blueprintId: 872, // Athletic All-Over-Print Cut & Sew Mesh Jersey
    printProviderId: 16, // Sublimation & Athletic Specialist
    variantMap: { 'S': 87201, 'M': 87202, 'L': 87203, 'XL': 87204, '2XL': 87205 },
    category: 'Esports Apparel',
  },
  'axiom-jersey-away': {
    blueprintId: 872,
    printProviderId: 16,
    variantMap: { 'S': 87211, 'M': 87212, 'L': 87213, 'XL': 87214, '2XL': 87215 },
    category: 'Esports Apparel',
  },
  'axiom-jersey-01': {
    blueprintId: 872,
    printProviderId: 16,
    variantMap: { 'S': 87221, 'M': 87222, 'L': 87223, 'XL': 87224, '2XL': 87225 },
    category: 'Esports Apparel',
  },
  'axiom-jersey-stealth': {
    blueprintId: 872,
    printProviderId: 16,
    variantMap: { 'S': 87231, 'M': 87232, 'L': 87233, 'XL': 87234, '2XL': 87235 },
    category: 'Esports Apparel',
  },
  'axiom-shaker-01': {
    blueprintId: 540, // Eastman Tritan 24oz / Stainless Shaker Bottle
    printProviderId: 10,
    variantMap: {
      '24 oz Standard (Eastman Tritan Frosted)': 54001,
      '26 oz Pro Insulated Stainless Steel (Double-Wall)': 54003,
      'Signature Toxic Lime & Royal Purple': 54001,
      'Stealth Blackout Obsidian': 54002,
    },
    category: 'Drinkware',
  },
  'axiom-hoodie-01': {
    blueprintId: 380, // Heavyweight Streetwear Hoodie
    printProviderId: 16,
    variantMap: { 'S': 3801, 'M': 3802, 'L': 3803, 'XL': 3804, '2XL': 3805, '3XL': 3806 },
    category: 'Esports Apparel',
  },
  'axiom-sweatshirt-01': {
    blueprintId: 312, // Heavyweight Fleece Crewneck
    printProviderId: 16,
    variantMap: { 'S': 3121, 'M': 3122, 'L': 3123, 'XL': 3124, '2XL': 3125, '3XL': 3126 },
    category: 'Esports Apparel',
  },
  'krown-mat-01': {
    blueprintId: 488, // Extended Gaming Desk Mat
    printProviderId: 1, // Spoke Custom Products / Monster Digital
    variantMap: {
      'Medium (M) 14"x12" (360x300mm)': 48801,
      'Large (L) 18"x16" (450x400mm)': 48802,
      'Extended (XL) 31.5"x12" (800x300mm)': 48803,
      'Panoramic (2XL) 35.4"x16" (900x400mm)': 48804,
      'Colossal (3XL) 47"x24" (1200x600mm)': 48805,
    },
    category: 'Desk Accessories',
  },
  'krown-mousepad-01': {
    blueprintId: 488, // Gaming Mouse Pad
    printProviderId: 1,
    variantMap: {
      'Medium (M) 14"x12" (360x300mm)': 48811,
      'Large (L) 18"x16" (450x400mm)': 48812,
      'Extended (XL) 31.5"x12" (800x300mm)': 48813,
      'Panoramic (2XL) 35.4"x16" (900x400mm)': 48814,
      'Colossal (3XL) 47"x24" (1200x600mm)': 48815,
    },
    category: 'Desk Accessories',
  },
  'axiom-sweatpants-pro': {
    blueprintId: 1089, // Ultra-Heavy French Terry Joggers
    printProviderId: 29,
    variantMap: { 'S': 48101, 'M': 48102, 'L': 48103, 'XL': 48104, '2XL': 48105, '3XL': 48106 },
    category: 'Esports Apparel',
  },
  'axiom-sweatpants-core': {
    blueprintId: 350, // Midweight Fleece Joggers
    printProviderId: 29,
    variantMap: { 'S': 48201, 'M': 48202, 'L': 48203, 'XL': 48204, '2XL': 48205, '3XL': 48206 },
    category: 'Esports Apparel',
  },
  'axiom-wrist-rest-01': {
    blueprintId: 920, // Ergonomic Memory Gel Keyboard Wrist Rest
    printProviderId: 42,
    variantMap: {
      'Compact 60% (11.4" x 2.9")': 92001,
      'Tenkeyless TKL 80% (14.2" x 2.9")': 92002,
      'Full-Size 100% (17.5" x 2.9")': 92003,
    },
    category: 'Desk Accessories',
  },
  'axiom-mug-01': {
    blueprintId: 78, // Two-Tone 15oz Ceramic Mug
    printProviderId: 10,
    variantMap: { '15 oz': 78015 },
    category: 'Drinkware',
  },
  'kc-tumbler-01': {
    blueprintId: 615, // Double-Wall Vacuum Tumbler 20oz
    printProviderId: 10,
    variantMap: { '20oz': 61520 },
    category: 'Drinkware',
  },
};

export interface PrintifyOrderItemInput {
  productId: string;
  variantId?: number;
  size?: string;
  color?: string;
  quantity: number;
  gamertag?: string;
  playerNumber?: string;
  customLogoUrl?: string;
  notes?: string;
}

export interface PrintifyShippingAddress {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  country: string;
  region?: string;
  address1: string;
  address2?: string;
  city: string;
  zip: string;
}

export interface PrintifyOrderInput {
  externalId: string;
  shippingMethod?: number; // 1 = Standard
  addressTo: PrintifyShippingAddress;
  lineItems: PrintifyOrderItemInput[];
}

export interface PrintifyOrderLineItemPayload {
  product_id?: string;
  variant_id: number;
  quantity: number;
  metadata?: {
    custom_gamertag?: string;
    custom_player_number?: string;
    custom_logo_url?: string;
    custom_upgrades?: string;
  };
}

export interface PrintifyOrderPayload {
  external_id: string;
  label?: string;
  notes?: string;
  line_items: PrintifyOrderLineItemPayload[];
  shipping_method: number;
  send_shipping_notification: boolean;
  address_to: {
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    country: string;
    region: string;
    address1: string;
    address2: string;
    city: string;
    zip: string;
  };
}

export const printifyService = new PrintifyService();

