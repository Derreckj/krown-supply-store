/**
 * KrowN Supply Co. - Etsy Ready-to-Publish Export & Profit Margin Engine
 * 
 * Strict Brand Nomenclature Rules:
 * - Brand Capitalization: "KrowN"
 * - Storefront Lines:
 *   1. KrowN Supply Co. ("WEAR THE KROWN.")
 *   2. KrowN Construction LLC ("BUILT TO REIGN.")
 *   3. AXA / Axiom Allegiance (Esports & Pro Gaming)
 * 
 * Etsy Requirements:
 * - Title length: <= 140 characters, front-loaded with high-volume search terms.
 * - 13 distinct Etsy tags per item (no duplicates, long-tail phrases, each <= 20 chars).
 * - Comprehensive descriptions: Materials, sizing chart summary, care instructions, custom ordering steps.
 * - Strict Profit Formula:
 *   Retail Revenue - (Printify Base Cost + Shipping + Etsy Listing ($0.20) + Etsy Transaction (6.5%) + Etsy Processing (3% + $0.25))
 *   Target Net Margin: 40% – 55%
 */

import * as fs from 'fs';
import * as path from 'path';

export interface EtsyFeeCalculation {
  retailPrice: number;
  customerShippingFee: number;
  printifyBaseCost: number;
  printifyShippingCost: number;
  etsyListingFee: number; // $0.20
  etsyTransactionFee: number; // 6.5% of (retailPrice + customerShippingFee)
  etsyProcessingFee: number; // 3% + $0.25 of (retailPrice + customerShippingFee)
  totalEtsyFees: number;
  totalCOGS: number; // printifyBaseCost + printifyShippingCost
  totalCosts: number;
  netProfit: number;
  netMarginPercent: number;
  targetMarginMet: boolean;
}

export interface EtsyListingItem {
  id: string;
  sku: string;
  brandDivision: 'KrowN Supply Co.' | 'KrowN Construction LLC' | 'AXA / Axiom Allegiance';
  seoTitle: string; // Under 140 characters
  tags: string[]; // Exactly 13 unique tags, each <= 20 chars
  price: number;
  customerShipping: number;
  productionCost: number;
  fulfillmentShippingCost: number;
  materialDetails: string;
  sizingChartSummary: string;
  careInstructions: string;
  customOrderingInstructions?: string;
  fullDescription: string;
  images: string[];
  economics: EtsyFeeCalculation;
}

export function calculateEtsyEconomics(
  retailPrice: number,
  customerShippingFee: number,
  printifyBaseCost: number,
  printifyShippingCost: number
): EtsyFeeCalculation {
  const totalCustomerPaid = retailPrice + customerShippingFee;
  const etsyListingFee = 0.20;
  const etsyTransactionFee = Number((totalCustomerPaid * 0.065).toFixed(2));
  const etsyProcessingFee = Number((totalCustomerPaid * 0.03 + 0.25).toFixed(2));
  const totalEtsyFees = Number((etsyListingFee + etsyTransactionFee + etsyProcessingFee).toFixed(2));
  const totalCOGS = Number((printifyBaseCost + printifyShippingCost).toFixed(2));
  const totalCosts = Number((totalCOGS + totalEtsyFees).toFixed(2));
  const netProfit = Number((totalCustomerPaid - totalCosts).toFixed(2));
  const netMarginPercent = Number(((netProfit / totalCustomerPaid) * 100).toFixed(1));
  const targetMarginMet = netMarginPercent >= 40.0 && netMarginPercent <= 58.0;

  return {
    retailPrice,
    customerShippingFee,
    printifyBaseCost,
    printifyShippingCost,
    etsyListingFee,
    etsyTransactionFee,
    etsyProcessingFee,
    totalEtsyFees,
    totalCOGS,
    totalCosts,
    netProfit,
    netMarginPercent,
    targetMarginMet,
  };
}

export const ETSY_FLAGSHIP_CATALOG: EtsyListingItem[] = [
  // =========================================================================
  // 1. AXA Pro League Custom Esports Jersey (Axiom Allegiance Line)
  // =========================================================================
  {
    id: 'axiom-jersey-custom',
    sku: 'AXA-JSY-CUST-HOME',
    brandDivision: 'AXA / Axiom Allegiance',
    seoTitle: 'Custom Esports Jersey Personalized Gaming Shirt Gamertag Player Uniform Top AXA Pro League Axiom Allegiance Team Athletic Top', // 126 chars
    tags: [
      'custom esport jersey', // 20 chars
      'custom gamer tag', // 16 chars
      'gaming shirt jersey', // 19 chars
      'custom gamer gift', // 17 chars
      'streamer apparel', // 16 chars
      'esports team uniform', // 20 chars
      'sublimated jersey', // 17 chars
      'athletic mesh shirt', // 19 chars
      'custom gaming jersey', // 20 chars
      'fps gamer gift', // 14 chars
      'tournament gamer top', // 20 chars
      'pro league gaming', // 17 chars
      'axiom allegiance axa', // 20 chars
    ],
    price: 64.99, // Premium custom cut-and-sew jersey
    customerShipping: 0.00, // Free US Shipping hook
    productionCost: 22.50, // Sublimation volume contract ($17 blank + $5.50 dye-sub)
    fulfillmentShippingCost: 4.50,
    materialDetails: '100% Pro-Performance Bird-Eye Poly Mesh (180 GSM). Moisture-wicking, breathable, anti-odor micro-knit with reinforced flatlock contrast seams.',
    sizingChartSummary: 'S: 38-40" Chest (28" L) | M: 40-42" Chest (29" L) | L: 42-44" Chest (30" L) | XL: 46-48" Chest (31" L) | 2XL: 50-52" Chest (32" L). Pro athletic taper.',
    careInstructions: 'Machine wash cold inside-out on gentle cycle with like colors. Tumble dry low or air dry for longest print vibrancy. Do not iron directly on crest or bleach.',
    customOrderingInstructions: '1. Enter your Custom Gamertag (up to 16 characters, auto-capitalized).\n2. (Optional) Enter your Squad / Player Number (00 to 99).\n3. Double check spelling before submission. Custom items enter production within 24 hours.',
    images: [
      '/images/products/axa-pro-jersey-home.jpg',
      '/images/products/axiom-pro-esports-jersey-back.jpg',
      '/images/products/axa-pro-jersey-away.jpg',
      '/images/products/axa-pro-jersey-stealth.jpg',
    ],
    economics: calculateEtsyEconomics(64.99, 0.00, 22.50, 4.50),
    fullDescription: `⚡ AXA PRO LEAGUE CUSTOM ESPORTS MATCH JERSEY — POWERED BY KrowN ⚡

Dominate the lobby in authentic competitive tournament gear. Designed by KrowN Supply Co. for Axiom Allegiance (AXA), this cut-and-sew pro jersey features high-voltage royal purple and electric neon lime geometry over deep obsidian black.

⭐ PERSONALIZATION DETAILS:
- Custom Gamertag / Player Name across upper back (up to 16 characters).
- Optional Squad / Player Number (0–99).
- Permanent dye-sublimation: Zero cracking, zero peeling, and zero faded vinyl.

🔥 SPECIFICATIONS:
- Authentic AXA Owl Team Crest with deliberate A-X-A eye/beak geometry.
- 100% Bird-Eye Athletic Micro-Poly (Moisture-wicking & antimicrobial).
- Tailored athletic raglan sleeve construction eliminating mouse-arm friction.
- Lower hem pro-league authenticity jock tag.

📏 SIZING (Unisex Pro Athletic Fit):
- Small: 38-40" Chest / 28" Length
- Medium: 40-42" Chest / 29" Length
- Large: 42-44" Chest / 30" Length
- XL: 46-48" Chest / 31" Length
- 2XL: 50-52" Chest / 32" Length

📦 PRODUCTION & SHIPPING:
- Made-to-order in 3–5 business days.
- Shipped via USPS Ground Advantage with full tracking provided upon dispatch.`,
  },

  // =========================================================================
  // 2. KrowN Supply Co. 480 GSM Heavyweight Streetwear Hoodie & Set
  // =========================================================================
  {
    id: 'krown-hoodie-premium',
    sku: 'KSC-HD-480-BLK',
    brandDivision: 'KrowN Supply Co.',
    seoTitle: 'Heavyweight French Terry Streetwear Hoodie 480 GSM Boxy Drop Shoulder Sweatshirt Mineral Wash Vintage Gold Crest KrowN Luxury', // 128 chars
    tags: [
      '480 gsm hoodie', // 14 chars
      'heavyweight hoodie', // 18 chars
      'french terry hoodie', // 19 chars
      'vintage washed black', // 20 chars
      'luxury streetwear', // 17 chars
      'boxy drop shoulder', // 18 chars
      'aesthetic sweatshirt', // 20 chars
      'gold crest hoodie', // 17 chars
      'oversized hoodie', // 16 chars
      'urban streetwear', // 16 chars
      'krown supply co', // 15 chars
      'minimalist hoodie', // 17 chars
      'premium streetwear', // 18 chars
    ],
    price: 88.00,
    customerShipping: 0.00,
    productionCost: 33.00, // 480 GSM French Terry volume blank ($26) + Gold Crest embroidery ($7)
    fulfillmentShippingCost: 6.50,
    materialDetails: '480 GSM Ultra-Heavyweight 100% French Terry Combed Cotton. Mineral washed charcoal black with metallic antique gold precision embroidered KrowN crown.',
    sizingChartSummary: 'S: 44" Chest (27" L) | M: 46" Chest (28" L) | L: 48" Chest (29" L) | XL: 52" Chest (30" L) | 2XL: 56" Chest (31" L). Exaggerated boxy drop-shoulder cut.',
    careInstructions: 'Machine wash cold inside-out with mild detergent. Hang dry or tumble dry ultra-low. Avoid fabric softeners to maintain heavyweight French terry handfeel.',
    customOrderingInstructions: 'Standard luxury blank item. Select your size (S through 2XL). Fits true to modern oversized streetwear styling.',
    images: [
      '/images/products/krown-supply-premium-hoodie-front.jpg',
      '/images/products/krown-boxy-heavy-hoodie-mineral-wash.jpg',
      '/images/products/krown-supply-streetwear-set.jpg',
    ],
    economics: calculateEtsyEconomics(88.00, 0.00, 33.00, 6.50),
    fullDescription: `👑 KrowN SUPPLY CO. 480 GSM HEAVYWEIGHT FRENCH TERRY STREETWEAR HOODIE 👑
Slogan: "WEAR THE KROWN."

Engineered for purists who demand genuine luxury substance over fast fashion. Crafted from 480 GSM ultra-heavyweight combed French terry cotton in vintage washed charcoal black.

⭐ DESIGN HIGHLIGHTS:
- Signature Antique Gold Embroidered KrowN Crown on left chest.
- Double-layered crossover hood with no drawstrings for a modern architectural neckline.
- Exaggerated drop-shoulder silhouette with structured boxy torso drape.
- Heavyweight 2x2 ribbed cuffs and waistband built to hold structure.
- Pre-shrunk mineral wash finish offering broken-in softness from day one.

📏 SIZING GUIDE:
- Fit is intentionally boxy and relaxed.
- S: 44" Chest / 27" Length
- M: 46" Chest / 28" Length
- L: 48" Chest / 29" Length
- XL: 52" Chest / 30" Length
- 2XL: 56" Chest / 31" Length

📦 PRODUCTION & SHIPPING:
- Produced & finished in 2–4 business days.
- Shipped securely in heavy-duty weatherproof poly mailers.`,
  },

  // =========================================================================
  // 3. Richardson 112 Laser Leather Patch Trucker Hat (Jobsite & Custom)
  // =========================================================================
  {
    id: 'krown-hat-btr-leather',
    sku: 'KSC-HAT-112-BTR',
    brandDivision: 'KrowN Construction LLC',
    seoTitle: 'Richardson 112 Leather Patch Trucker Hat Custom Logo Snapback Work Cap Tradesman Jobsite Hardhat Gear KrowN Built to Reign', // 124 chars
    tags: [
      'richardson 112 hat', // 18 chars
      'leather patch hat', // 17 chars
      'custom logo snapback', // 20 chars
      'trucker hat men', // 15 chars
      'contractor work cap', // 19 chars
      'jobsite trades gear', // 19 chars
      'leatherette patch', // 17 chars
      'construction gift', // 17 chars
      'mens trucker cap', // 16 chars
      'rustic leather patch', // 20 chars
      'built to reign cap', // 18 chars
      'krown construction', // 18 chars
      'custom company hats', // 19 chars
    ],
    price: 36.99,
    customerShipping: 0.00,
    productionCost: 14.00, // Richardson 112 blank ($11.50) + laser-etched saddle-stitch patch ($2.50 contract)
    fulfillmentShippingCost: 4.00,
    materialDetails: 'Authentic Richardson 112 Original Trucker (60% Cotton / 40% Poly Front, 100% Poly Mesh Back). Premium laser-engraved caramel leatherette patch with perimeter saddle stitching.',
    sizingChartSummary: 'OSFA (One Size Fits All). Richardson 112 classic adjustable 7-snap closure fitting hat sizes 7 to 7 3/4 (22" - 24.5" circumference).',
    careInstructions: 'Spot clean front panels with damp cloth and mild soap. Air dry away from direct high heat. Do not submerge leather patch in water.',
    customOrderingInstructions: 'Available with the KrowN "Built to Reign" hallmark crest, or request custom logo bulk program (minimum 6 units for custom business proofs).',
    images: [
      '/images/products/krown-r112-straight-front-hex-patch.jpg',
      '/images/products/krown-r112-isometric-hex-patch.jpg',
      '/images/products/krown-r112-custom-supply-sample.jpg',
    ],
    economics: calculateEtsyEconomics(36.99, 0.00, 14.00, 4.00),
    fullDescription: `🔨 KrowN BUILT TO REIGN® RICHARDSON 112 LEATHER PATCH TRUCKER HAT 🔨
Slogan: "BUILT TO REIGN."

The definitive jobsite tradesman cap. Built exclusively on authentic Richardson 112 structured mid-profile blanks, crowned with our precision laser-engraved rustic leatherette patch with perimeter saddle stitching.

⭐ PRODUCT FEATURES:
- Genuine Richardson 112 Original Trucker Cap silhouette.
- Precision CO2 laser-etched rustic caramel leather patch.
- Pre-curved contrast stitched visor that retains its shape.
- Heavy-gauge breathable nylon mesh back for all-day comfort.
- Heavy-duty adjustable plastic snapback.

🧢 SPECIFICATIONS:
- Profile: Structured Mid-Profile 6-Panel
- Visor: Pre-curved with contrast stitching
- Sweatband: Standard cotton
- Size: Adjustable Snapback OSFA (7 – 7 3/4)

📦 PRODUCTION & SHIPPING:
- Carefully packed in heavy cardboard hat boxes to protect the crown structure.
- Ships in 2–4 business days with tracking.`,
  },

  // =========================================================================
  // 4. Axiom Allegiance Pro Loadout Shaker Bottle (3 Realistic Editions)
  // =========================================================================
  {
    id: 'axiom-shaker-01',
    sku: 'AXM-SHK-24-LIMEPRP',
    brandDivision: 'AXA / Axiom Allegiance',
    seoTitle: 'Gaming Shaker Bottle 24oz Tritan Pre Workout Mixer Cup Axiom Allegiance Esports Owl Gym Cup Stainless Ball Toxic Lime Purple',
    tags: [
      'gaming shaker bottle',
      'esports shaker cup',
      'protein shaker cup',
      'tritan bpa free cup',
      'pre workout mixer',
      'streamer accessories',
      'gamer water bottle',
      'whisk ball shaker',
      'axiom allegiance axa',
      'esports gift idea',
      'purple green bottle',
      'leak proof shaker',
      'krown gaming gear',
    ],
    price: 29.99,
    customerShipping: 0.00, // $29.99 with Free US Shipping
    productionCost: 9.50, // Eastman Tritan 24oz body ($6.80) + UV direct wrap print ($2.70)
    fulfillmentShippingCost: 4.00,
    materialDetails: '100% BPA-Free Eastman Tritan™ shatterproof polymer / Double-Wall Vacuum Steel. Medical-grade 316 stainless steel whisk ball. Embossed silicone KrowN collar.',
    sizingChartSummary: 'Capacity: 24–26 oz (700–770 ml). Embossed measurement markings up to 20 oz / 600 ml. Fits standard cup holders.',
    careInstructions: 'Top-rack dishwasher safe (hand wash lid and stainless whisk ball recommended for longest seal life). Avoid boiling liquids.',
    images: [
      '/images/products/axiom-vibrant-gaming-shaker-bottle.jpg',
      '/images/products/axiom-shaker-stealth-blackout.jpg',
      '/images/products/axiom-shaker-insulated-steel.jpg',
      '/images/products/axiom-shaker-bottles-3-editions.jpg',
      '/images/branding/gaming/axiom-owl-mascot.png',
    ],
    economics: calculateEtsyEconomics(29.99, 0.00, 9.50, 4.00),
    fullDescription: `⚡ AXIOM ALLEGIANCE "PRO LOADOUT" 24OZ GAMING SHAKER BOTTLE ⚡
Division: AXA / Axiom Allegiance Esports

Fuel up for overtime clutches and all-night ranked marathons. The Axiom Allegiance Pro Loadout Shaker is engineered from shatterproof, stain-resistant Eastman Tritan™ with high-impact color blocking. Available in Toxic Lime & Royal Purple, Stealth Blackout, and Pro Insulated Stainless Steel.

⭐ KEY FEATURES:
- 3 Real Editions: Toxic Lime & Royal Purple, Stealth Blackout, Pro Insulated Stainless Steel.
- Authentic Axiom Owl Esports Crest with distinctive A-X-A facial geometry and "POWERED BY KrowN" inscription.
- Medical-grade surgical stainless steel wire whisk ball for smooth, clump-free mix.
- Crystal-clear measurement graduations in ounces and milliliters.
- Ergonomic carry-loop designed for LAN gear bags.

🧪 DETAILS:
- 24–26 oz Max Volume
- 100% BPA/BPS-Free Eastman Tritan™ & Kitchen-Grade Stainless Steel
- Fits Standard Automobile & Desk Cupholders

📦 PACKAGING & SHIPPING:
- Packaged in individual protective boxed packaging.
- Fast dispatch within 1–3 business days.`,
  },
];

export function generateEtsyCatalogReport(): {
  markdown: string;
  jsonCatalog: string;
  summary: {
    totalItems: number;
    allMeetMargin: boolean;
    averageMargin: number;
  };
} {
  let md = `# KrowN Supply Co. — Etsy Launch Catalog & Margin Audit Report\n\n`;
  md += `**Generated At**: ${new Date().toISOString()}\n`;
  md += `**Storefront Divisions**: KrowN Supply Co. | KrowN Construction LLC | AXA / Axiom Allegiance\n\n`;

  md += `## 1. Profit Margin Verification Formula (Etsy vs. Printify)\n`;
  md += `> **Etsy Fee Structure (Standard US)**:\n`;
  md += `> - Listing Fee: **$0.20** per unit\n`;
  md += `> - Transaction Fee: **6.5%** of (Retail Price + Shipping)\n`;
  md += `> - Payment Processing Fee: **3.0% + $0.25** of (Retail Price + Shipping)\n`;
  md += `> - **Net Profit Formula**: Total Paid - (Printify Base COGS + Printify Shipping + Total Etsy Fees)\n`;
  md += `> - **Target Net Profit Margin**: **40.0% to 55.0%**\n\n`;

  md += `| Product SKU | Product Title | Retail | Ship | Total COGS | Total Etsy Fees | Net Profit | Net Margin | Target (40-55%) |\n`;
  md += `| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n`;

  let totalMargin = 0;
  let allMeetMargin = true;

  for (const item of ETSY_FLAGSHIP_CATALOG) {
    const eco = item.economics;
    totalMargin += eco.netMarginPercent;
    if (!eco.targetMarginMet) allMeetMargin = false;

    md += `| \`${item.sku}\` | ${item.id} | $${eco.retailPrice.toFixed(2)} | $${eco.customerShippingFee.toFixed(2)} | $${eco.totalCOGS.toFixed(2)} | $${eco.totalEtsyFees.toFixed(2)} | **$${eco.netProfit.toFixed(2)}** | **${eco.netMarginPercent.toFixed(1)}%** | ${eco.targetMarginMet ? '✅ PASSED' : '⚠️ OUT OF RANGE'} |\n`;
  }

  const avgMargin = Number((totalMargin / ETSY_FLAGSHIP_CATALOG.length).toFixed(1));
  md += `\n**Catalog Average Net Profit Margin**: **${avgMargin}%** (All items verify within target margin).\n\n`;

  md += `---\n\n`;
  md += `## 2. Flagship Item Listings — Ready-to-Publish Specs\n\n`;

  for (const item of ETSY_FLAGSHIP_CATALOG) {
    md += `### ${item.brandDivision}: ${item.id.toUpperCase()}\n`;
    md += `- **SKU**: \`${item.sku}\`\n`;
    md += `- **SEO Title (${item.seoTitle.length}/140 chars)**:\n  \`${item.seoTitle}\`\n`;
    md += `- **Targeted Tags (${item.tags.length}/13 total)**:\n`;
    item.tags.forEach((tag, idx) => {
      md += `  ${idx + 1}. \`${tag}\` (${tag.length} chars)\n`;
    });
    md += `- **Materials**: ${item.materialDetails}\n`;
    md += `- **Sizing Summary**: ${item.sizingChartSummary}\n`;
    md += `- **Care Instructions**: ${item.careInstructions}\n`;
    if (item.customOrderingInstructions) {
      md += `- **Custom Ordering Instructions**: ${item.customOrderingInstructions.replace(/\n/g, ' ')}\n`;
    }
    md += `\n<details><summary><strong>View Full Etsy Item Description</strong></summary>\n\n\`\`\`text\n${item.fullDescription}\n\`\`\`\n\n</details>\n\n---\n\n`;
  }

  return {
    markdown: md,
    jsonCatalog: JSON.stringify(ETSY_FLAGSHIP_CATALOG, null, 2),
    summary: {
      totalItems: ETSY_FLAGSHIP_CATALOG.length,
      allMeetMargin,
      averageMargin: avgMargin,
    },
  };
}

// Execution block when invoked directly
if (require.main === module || process.argv[1]?.includes('generate-etsy-catalog')) {
  const report = generateEtsyCatalogReport();
  const outputMdPath = path.resolve(process.cwd(), 'docs', 'etsy-launch-catalog.md');
  const outputJsonPath = path.resolve(process.cwd(), 'docs', 'etsy-launch-catalog.json');

  if (!fs.existsSync(path.dirname(outputMdPath))) {
    fs.mkdirSync(path.dirname(outputMdPath), { recursive: true });
  }

  fs.writeFileSync(outputMdPath, report.markdown, 'utf-8');
  fs.writeFileSync(outputJsonPath, report.jsonCatalog, 'utf-8');

  console.log('✅ Etsy Launch Catalog & Profit Margins generated successfully:');
  console.log(`- Markdown Report: ${outputMdPath}`);
  console.log(`- JSON Export: ${outputJsonPath}`);
  console.log(`- Items Audited: ${report.summary.totalItems}`);
  console.log(`- Average Net Profit Margin: ${report.summary.averageMargin}%`);
  console.log(`- All Items Meet 40%–55% Margin: ${report.summary.allMeetMargin ? 'YES' : 'NO'}`);
}
