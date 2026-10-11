'use client';

import React, { useState } from 'react';
import Link from 'next/link';

interface ProductPack {
  division: '01_KrowN_Supply_Co' | '02_KrowN_Construction' | '03_Axiom_Allegiance';
  name: string;
  slug: string;
  productBlank: string;
  decorationMethod: string;
  supplierRoute: string;
  singleLogoCheck: string;
  images: Array<{
    title: string;
    src: string;
    caption: string;
  }>;
}

const PRODUCT_PACKS: ProductPack[] = [
  // 03 AXIOM ALLEGIANCE
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Owl Two-Tone Ceramic Gaming Mug (15oz)',
    slug: 'axiom-mug-01',
    productBlank: 'Printify Blueprint 78 (15oz Two-Tone Ceramic Mug)',
    decorationMethod: 'Sublimated High-Gloss Ceramic Glaze (Exterior Black / Interior Lime)',
    supplierRoute: 'Printify Verified (District Photo / SPO)',
    singleLogoCheck: 'PASS: Exactly ONE authentic Axiom Owl mascot centered on mug face with glossy cylindrical reflections. Zero doubled horn outlines, zero ghosting.',
    images: [
      { title: '01 Studio Hero Front', src: '/images/products/axiom-mug-clean-photoreal-15oz-v3.jpg', caption: 'Clean studio presentation showing single authentic owl crest and centered typography.' },
      { title: '02 Battlestation Desk Setup', src: '/images/products/axiom-mug-desk-setup.jpg', caption: 'In-use battlestation desk setup with ambient purple lighting and tournament desk pad.' },
      { title: '03 Lime Glaze Interior Angle', src: '/images/products/axiom-mug-lime-interior.jpg', caption: 'Angled view highlighting the vibrant electric lime interior glaze and ergonomic handle.' },
      { title: '04 Crest & Glaze Macro', src: '/images/products/axiom-mug-crest-detail.jpg', caption: 'Macro zoom proving zero doubled lines, crisp original vector geometry, and glossy specular glaze.' },
      { title: '05 Scale & Specifications', src: '/images/products/axiom-mug-specifications.jpg', caption: 'Product dimension specifications: 15 oz capacity, dishwasher & microwave safe.' }
    ]
  },
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Allegiance Vintage Washed Chino Dad Hat',
    slug: 'axiom-dad-hat-01',
    productBlank: 'ValuCap VC300A / Yupoong 6245CM Unstructured Bio-Washed Chino Twill',
    decorationMethod: 'Direct High-Density Twill Embroidery (approx 2.2" wide)',
    supplierRoute: 'Printify Blueprint 7651 / 7659 (Underground Printing / Awkward Styles)',
    singleLogoCheck: 'PASS: Exactly ONE authentic Axiom Owl centered on lower front crown. Previously stacked second owl on crown 100% removed.',
    images: [
      { title: '01 Studio Hero Front', src: '/images/products/axiom-dad-hat-photoreal-v10.jpg', caption: 'Clean front view on slate display block with exactly ONE embroidered owl mascot.' },
      { title: '02 Worn Lookbook', src: '/images/products/axiom-dad-hat-worn-lookbook.jpg', caption: 'Lifestyle worn angle showing authentic low-profile unstructured crown drape.' },
      { title: '03 Side Profile & Curved Bill', src: '/images/products/axiom-dad-hat-side-profile.jpg', caption: 'Side profile showing relaxed pre-curved visor and 6-panel twill crown construction.' },
      { title: '04 Embroidery Thread Macro', src: '/images/products/axiom-dad-hat-embroidery-macro.jpg', caption: 'Macro thread detail showing authentic embroidery texture and contact shadow.' },
      { title: '05 Closure & Rear Specifications', src: '/images/products/axiom-dad-hat-closure-specs.jpg', caption: 'Rear view showing self-fabric strap with antique brass tri-glide buckle and tuck-in grommet.' }
    ]
  },
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Richardson 112 Genuine Leather Patch Trucker Snapback',
    slug: 'axiom-r112-patch-01',
    productBlank: 'Authentic Richardson 112 Structured Mid-Profile 6-Panel Trucker',
    decorationMethod: 'Laser-Debossed 100% Genuine 5 oz Full-Grain Veg-Tan Cowhide Leather Patch',
    supplierRoute: 'Specialized Contract Supplier (Lone Star Leather / CustomCaps / Richardson Direct Decorator)',
    singleLogoCheck: 'PASS: Exactly ONE laser-debossed Axiom Owl housed in hexagonal full-grain leather patch with perimeter saddle stitching. Monochromatic deboss truthfully presented.',
    images: [
      { title: '01 Studio Hero Cognac Patch', src: '/images/products/axiom-r112-leather-patch-charcoal.jpg', caption: 'Structured charcoal/black Richardson 112 with genuine cognac leather patch.' },
      { title: '02 Worn Outdoor Lifestyle', src: '/images/products/axiom-r112-worn-lifestyle.jpg', caption: 'Outdoor lifestyle view showcasing structured mid-profile silhouette and contrast stitching.' },
      { title: '03 Trucker Mesh Profile', src: '/images/products/axiom-r112-mesh-profile.jpg', caption: 'Breathable nylon mesh rear panels and adjustable heavy-duty snapback closure.' },
      { title: '04 Leather Grain Macro', src: '/images/products/axiom-r112-leather-macro.jpg', caption: 'Close-up macro of natural full-grain leather texture, burnt-edge laser relief, and saddle stitching.' },
      { title: '05 Supplier & Material Specs', src: '/images/products/axiom-r112-supplier-specs.jpg', caption: 'Authentic blank disclosure: 60/40 cotton-poly front, nylon mesh back, industrial thermo-bonded patch.' }
    ]
  },
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Allegiance Pro Heavyweight 450 GSM Joggers',
    slug: 'axiom-sweatpants-pro',
    productBlank: 'Independent Trading Co. PRM50PTPD (450 GSM Heavyweight French Terry Fleece)',
    decorationMethod: 'Precision Direct-to-Film (DTF) Stretch Heat Transfer',
    supplierRoute: 'Printify Verified / Independent Contract Route',
    singleLogoCheck: 'PASS: Zero ghost owls on studio walls. Single vertical leg typography + single authentic owl on upper left pocket.',
    images: [
      { title: '01 Studio Model Hero (Clean Wall)', src: '/images/products/axiom-sweatpants-pro-model-v10.jpg', caption: 'Studio model on neutral concrete cyclorama with zero floating ghost graphics or wall smudges.' },
      { title: '02 Studio Flat Lay Heavyweight', src: '/images/products/axiom-sweatpants-pro-studio-v10.jpg', caption: 'Full flat-lay garment layout showing tailored taper, ribbed cuffs, and heavy split-stitch construction.' },
      { title: '03 Waistband & Drawcords', src: '/images/products/axiom-joggers-waistband-detail.jpg', caption: 'Close-up of elastic waistband, metal eyelets, and two-tone heavy cotton drawcords.' },
      { title: '04 Leg Print & Fleece Macro', src: '/images/products/axiom-joggers-fabric-macro.jpg', caption: 'Macro detail of flexible DTF graphic placement along outer leg seam.' },
      { title: '05 Core vs Pro Comparison', src: '/images/products/axiom-joggers-core-vs-pro-specs.jpg', caption: 'Comparison chart detailing Pro 450 GSM French Terry vs Core 280 GSM fleece differences.' }
    ]
  },
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Allegiance Heavy Ribbed Tournament Cuffed Beanie',
    slug: 'axiom-beanie-01',
    productBlank: 'Heavy 4-Gauge Hypoallergenic 100% Acrylic Rib Knit (3" Foldover Cuff)',
    decorationMethod: 'Direct High-Density Embroidery on Ribbed Cuff',
    supplierRoute: 'Printify Blueprint 414 / 644 (OTTO Cap / Yupoong)',
    singleLogoCheck: 'PASS: Clean continuous rib-knit stitching under owl crest. Defective rectangular dark patch artifact completely removed.',
    images: [
      { title: '01 Studio Hero Obsidian/Lime', src: '/images/products/axiom-beanie-obsidian-lime-v11.jpg', caption: 'Obsidian black ribbed beanie with crisp lime & purple embroidered owl crest on center cuff.' },
      { title: '02 Worn Tournament Lifestyle', src: '/images/products/axiom-beanie-worn-lifestyle.jpg', caption: 'Cold-weather tournament lifestyle presentation showing snug 3-inch foldover fit.' },
      { title: '03 Royal Purple/Green Edition', src: '/images/products/axiom-beanie-purple-green-v11.jpg', caption: 'Alternate team colorway variant featuring royal purple body with toxic green crest.' },
      { title: '04 Rib Knit & Stitch Macro', src: '/images/products/axiom-beanie-ribknit-macro.jpg', caption: 'Macro zoom confirming seamless continuous rib knitting beneath the embroidery.' },
      { title: '05 Colorway Lineup Specifications', src: '/images/products/axiom-beanie-lineup-specs.jpg', caption: 'Specifications for all 3 colorway options: Obsidian/Lime, Purple/Green, and Volcanic Ember.' }
    ]
  },
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Allegiance Official Crewneck Sweatshirt',
    slug: 'axiom-sweatshirt-01',
    productBlank: 'Gildan 18000 Heavy Blend / Comfort Colors 1566 Garment-Dyed Fleece',
    decorationMethod: 'Direct-to-Garment (DTG) Chest Crest + Left Sleeve Lettering',
    supplierRoute: 'Printify Blueprint 49 (Monster Digital / SwiftPOD)',
    singleLogoCheck: 'PASS: Exactly ONE authentic Axiom Owl centered on chest. Overlapping text and doubled contours removed.',
    images: [
      { title: '01 Studio Flat Lay Chest Owl', src: '/images/products/axiom-crewneck-sweatshirt-studio.jpg', caption: 'Studio flat lay featuring single authentic Axiom Owl mascot centered on chest.' },
      { title: '02 Model Worn Lookbook', src: '/images/products/axiom-crewneck-sweatshirt-model.jpg', caption: 'Model worn view showing relaxed streetwear fit and ribbed collar V-stitch accent.' },
      { title: '03 Left Sleeve Lettering Detail', src: '/images/products/axiom-crewneck-sleeve-detail.jpg', caption: 'Vertical Gothic "AXIOM ALLEGIANCE" lettering along the wearer left forearm print zone.' },
      { title: '04 Chest Print & Collar Macro', src: '/images/products/axiom-crewneck-chest-macro.jpg', caption: 'Close-up of ribbed collar, split-stitch seams, and breathable DTG ink absorption.' },
      { title: '05 Original vs New Owl Option', src: '/images/products/axiom-crewneck-option-specs.jpg', caption: 'Verification specifications highlighting original master owl as primary option with new owl alternate.' }
    ]
  },
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Redesigned Gaming Desk Mats (2 New Directions)',
    slug: 'krown-mat-01',
    productBlank: 'Printify Blueprint 488 / 975 (4mm Anti-Slip Natural Rubber + Micro-Weave Cloth)',
    decorationMethod: 'Edge-to-Edge Dye Sublimation with Precision Anti-Fray Black Stitched Edge',
    supplierRoute: 'Printify Verified (Spoke Custom / FYBY)',
    singleLogoCheck: 'PASS: Completely fresh redesigns. Hero owl positioned on right flank so keyboard and mouse never cover it. Zero fake printed LEDs or fake glow borders.',
    images: [
      { title: '01 Studio Hero Desk Setup', src: '/images/products/axiom-mat-hero-desk-setup.jpg', caption: 'Desk setup with mechanical keyboard and mouse proving right-flank mascot remains 100% visible.' },
      { title: '02 Design 1: Tactical Arena Flat Lay', src: '/images/products/axiom-mat-design-a-tactical.jpg', caption: 'Direction A: Tactical Esports Grid with subtle coordinate typography and hero owl.' },
      { title: '03 Design 2: Stealth Sovereign Flat Lay', src: '/images/products/axiom-mat-design-b-sovereign.jpg', caption: 'Direction B: Stealth Sovereign Hexagonal Battle Arena with dark isometric line accents.' },
      { title: '04 Stitched Edge & Fabric Macro', src: '/images/products/axiom-mat-stitched-macro.jpg', caption: 'Macro zoom of black anti-fray perimeter lockstitching and 4mm textured rubber base.' },
      { title: '05 Sizing & Pricing Matrix', src: '/images/products/axiom-mat-sizing-pricing-specs.jpg', caption: 'Dimension matrix for all 5 verified sizes: 14.5x12.2, 18x12, 22x12, 31.5x15.5, and 48x24.' }
    ]
  },
  {
    division: '03_Axiom_Allegiance',
    name: 'Axiom Allegiance Pro Loadout Shaker Bottle',
    slug: 'axiom-shaker-01',
    productBlank: '24 oz BPA-Free Shatterproof Smoke Tritan Shaker with Stainless Whisk Ball',
    decorationMethod: 'Screen Printed / UV Curable Ink Wrap',
    supplierRoute: 'Printify Verified Drinkware Provider',
    singleLogoCheck: 'PASS: Single authentic Axiom Owl mascot on smoke Tritan bottle with embossed measurement markings.',
    images: [
      { title: '01 Studio Hero Front', src: '/images/products/axiom-shaker-lifestyle-desk.jpg', caption: '24 oz smoke Tritan shaker bottle with leak-proof flip cap and single authentic Axiom Owl.' }
    ]
  },

  // 01 KROWN SUPPLY CO
  {
    division: '01_KrowN_Supply_Co',
    name: 'KrowN Supply Co. Comfort Colors 1717 Vintage Heavy Tee',
    slug: 'krown-tee-cc1717',
    productBlank: 'Comfort Colors 1717 (6.1 oz Garment-Dyed 100% Ring-Spun Cotton)',
    decorationMethod: 'Direct-to-Garment (DTG) Left Chest Emblem + Oversized Back Print',
    supplierRoute: 'Printify Blueprint 101483 (SwiftPOD / Monster Digital)',
    singleLogoCheck: 'PASS: Small minimal KrowN Supply crown on left chest, large bold statement graphic on back (Sullen / GBRS aesthetic conventions).',
    images: [
      { title: '01 Studio Front (Small Chest Crown)', src: '/images/products/krown-supply-comfort-colors-1717-tee.jpg', caption: 'Front view showing minimal left chest metallic antique gold crown emblem.' },
      { title: '02 Studio Back (Large Statement Print)', src: '/images/deliveries/01_KrowN_Supply_Co/KrowN_Supply_Streetwear_Tee/02_Studio_Back_Large_Statement_Print.jpg', caption: 'Oversized statement back print featuring arched typography and official geometric crown.' },
      { title: '03 Model Worn Lookbook', src: '/images/deliveries/01_KrowN_Supply_Co/KrowN_Supply_Streetwear_Tee/03_Model_Worn_Streetwear_Lookbook.jpg', caption: 'Relaxed streetwear lookbook fit in vintage mineral-washed Pepper Black.' },
      { title: '04 Mineral Wash & Print Macro', src: '/images/deliveries/01_KrowN_Supply_Co/KrowN_Supply_Streetwear_Tee/04_Mineral_Wash_Print_Macro.jpg', caption: 'Macro of 6.1 oz garment-dyed ring-spun cotton texture and soft-hand ink feel.' },
      { title: '05 Blank Comparison Specs', src: '/images/deliveries/01_KrowN_Supply_Co/KrowN_Supply_Streetwear_Tee/05_Blank_Comparison_Specifications.jpg', caption: 'Comparison of Comfort Colors 1717 premium vs Gildan 64000 Softstyle value option.' }
    ]
  },
  {
    division: '01_KrowN_Supply_Co',
    name: 'KrowN Supply Co. Signature Luxury Shaker Bottle',
    slug: 'krown-shaker-01',
    productBlank: '24 oz Smoke Tritan Shaker Bottle with Matte Obsidian Flip Lid',
    decorationMethod: 'Screen Printed Metallic Gold & Brushed Steel Emblem',
    supplierRoute: 'Printify Verified Drinkware',
    singleLogoCheck: 'PASS: Distinct KrowN Supply Co. geometric crown emblem only. Zero mixed brands.',
    images: [
      { title: '01 Studio Hero Front', src: '/images/products/krown-shaker-front-clean.jpg', caption: '24 oz smoke Tritan luxury shaker with official KrowN Supply Co. geometric brand crest.' }
    ]
  },

  // 02 KROWN CONSTRUCTION
  {
    division: '02_KrowN_Construction',
    name: 'KrowN Construction Tradesman Jobsite Shaker Bottle',
    slug: 'kc-shaker-01',
    productBlank: '24 oz Impact-Resistant Tritan Shaker with Safety Carry Loop',
    decorationMethod: 'High-Visibility White Screen Print',
    supplierRoute: 'Printify Verified Drinkware',
    singleLogoCheck: 'PASS: Official KrowN Construction LLC emblem. Zero mixed brand assets.',
    images: [
      { title: '01 Studio Hero Front', src: '/images/products/kc-shaker-highvis-tritan-v3.jpg', caption: 'Jobsite impact Tritan shaker with official KrowN Construction insignia and measurement lines.' }
    ]
  }
];

export default function AuditGalleryPage() {
  const [activeTab, setActiveTab] = useState<'all' | '01_KrowN_Supply_Co' | '02_KrowN_Construction' | '03_Axiom_Allegiance'>('all');
  const [lightboxImg, setLightboxImg] = useState<{ src: string; title: string; caption: string } | null>(null);

  const filteredPacks = activeTab === 'all' 
    ? PRODUCT_PACKS 
    : PRODUCT_PACKS.filter(p => p.division === activeTab);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0b0e', color: '#e2e8f0', padding: '2rem 1.5rem', fontFamily: 'system-ui, sans-serif' }}>
      {/* Top Header */}
      <div style={{ maxWidth: '1280px', margin: '0 auto 2.5rem auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #1e222d', paddingBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ color: '#39ff14', fontSize: '0.85rem', fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
              Official Production Audit &amp; Catalogue Verification
            </div>
            <h1 style={{ fontSize: '2.2rem', fontWeight: 800, color: '#ffffff', margin: 0 }}>
              Master Product Redesign Gallery
            </h1>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <Link 
              href="/"
              style={{ backgroundColor: '#161922', color: '#cbd5e1', padding: '0.6rem 1.2rem', borderRadius: '6px', fontSize: '0.85rem', fontWeight: 600, border: '1px solid #2a2e3d', textDecoration: 'none' }}
            >
              Back to Store
            </Link>
          </div>
        </div>

        {/* Quality Audit Overview Banner */}
        <div style={{ marginTop: '1.5rem', backgroundColor: '#12141c', border: '1px solid #242938', borderRadius: '10px', padding: '1.25rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
          <div>
            <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Wrist Rest Removal</div>
            <div style={{ color: '#39ff14', fontSize: '1.1rem', fontWeight: 800, marginTop: '0.25rem' }}>100% UNPUBLISHED</div>
            <p style={{ color: '#64748b', fontSize: '0.8rem', margin: '0.25rem 0 0 0' }}>Removed from catalogue, feeds, search, and live shops.</p>
          </div>
          <div>
            <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Doubled Owl Fix</div>
            <div style={{ color: '#39ff14', fontSize: '1.1rem', fontWeight: 800, marginTop: '0.25rem' }}>RESOLVED (1:1 RATIO)</div>
            <p style={{ color: '#64748b', fontSize: '0.8rem', margin: '0.25rem 0 0 0' }}>Single authentic owl per intended placement across all items.</p>
          </div>
          <div>
            <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Richardson 112 &amp; Dad Hat</div>
            <div style={{ color: '#39ff14', fontSize: '1.1rem', fontWeight: 800, marginTop: '0.25rem' }}>GENUINE LEATHER &amp; CHINO</div>
            <p style={{ color: '#64748b', fontSize: '0.8rem', margin: '0.25rem 0 0 0' }}>Laser-debossed veg-tan leather + bio-washed twill.</p>
          </div>
          <div>
            <div style={{ color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>Redesigned Desk Mats</div>
            <div style={{ color: '#39ff14', fontSize: '1.1rem', fontWeight: 800, marginTop: '0.25rem' }}>2 NEW DIRECTIONS</div>
            <p style={{ color: '#64748b', fontSize: '0.8rem', margin: '0.25rem 0 0 0' }}>Right-flank mascot + 5 proportional size formats.</p>
          </div>
        </div>

        {/* Division Filter Tabs */}
        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem', borderBottom: '1px solid #1e222d', paddingBottom: '0.75rem', overflowX: 'auto' }}>
          {[
            { id: 'all', label: 'All Divisions (12 Products)' },
            { id: '03_Axiom_Allegiance', label: '03 Axiom Allegiance (Esports)' },
            { id: '01_KrowN_Supply_Co', label: '01 KrowN Supply Co. (Streetwear)' },
            { id: '02_KrowN_Construction', label: '02 KrowN Construction (Tradesman)' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              style={{
                backgroundColor: activeTab === tab.id ? '#39ff14' : '#141720',
                color: activeTab === tab.id ? '#0a0b0e' : '#94a3b8',
                border: activeTab === tab.id ? '1px solid #39ff14' : '1px solid #232838',
                padding: '0.5rem 1rem',
                borderRadius: '6px',
                fontSize: '0.85rem',
                fontWeight: 700,
                cursor: 'pointer',
                whiteSpace: 'nowrap'
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Product Packs Grid */}
      <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        {filteredPacks.map((pack, pIdx) => (
          <div key={pIdx} style={{ backgroundColor: '#11131a', border: '1px solid #1e2330', borderRadius: '12px', overflow: 'hidden' }}>
            {/* Product Meta Header */}
            <div style={{ backgroundColor: '#161922', padding: '1.25rem 1.5rem', borderBottom: '1px solid #1e2330', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <span style={{ 
                  display: 'inline-block',
                  fontSize: '0.7rem', 
                  fontWeight: 800, 
                  letterSpacing: '0.05em',
                  padding: '0.2rem 0.6rem', 
                  borderRadius: '4px',
                  backgroundColor: pack.division.includes('Axiom') ? '#39ff1415' : (pack.division.includes('Supply') ? '#d4af3715' : '#ea580c15'),
                  color: pack.division.includes('Axiom') ? '#39ff14' : (pack.division.includes('Supply') ? '#eab308' : '#f97316'),
                  marginBottom: '0.4rem',
                  textTransform: 'uppercase'
                }}>
                  {pack.division.replace(/_/g, ' ')}
                </span>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#ffffff', margin: '0 0 0.5rem 0' }}>
                  {pack.name}
                </h2>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.25rem', fontSize: '0.8rem', color: '#94a3b8' }}>
                  <div><strong>Blank:</strong> {pack.productBlank}</div>
                  <div><strong>Decoration:</strong> {pack.decorationMethod}</div>
                  <div><strong>Supplier:</strong> {pack.supplierRoute}</div>
                </div>
              </div>
              <Link 
                href={`/products/${pack.slug}`}
                style={{ backgroundColor: '#212634', color: '#e2e8f0', padding: '0.5rem 1rem', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 600, border: '1px solid #333a4c', textDecoration: 'none' }}
              >
                View Live Store SKU &rarr;
              </Link>
            </div>

            {/* Quality Gate Verification Pill */}
            <div style={{ backgroundColor: '#0d1017', padding: '0.75rem 1.5rem', borderBottom: '1px solid #1b202c', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <span style={{ color: '#39ff14', fontWeight: 800 }}>&#x2713; QUALITY VERIFICATION:</span>
              <span style={{ color: '#cbd5e1' }}>{pack.singleLogoCheck}</span>
            </div>

            {/* 5-Image Photo Pack Grid */}
            <div style={{ padding: '1.5rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '1.25rem' }}>
              {pack.images.map((img, iIdx) => (
                <div 
                  key={iIdx} 
                  style={{ backgroundColor: '#161922', border: '1px solid #232838', borderRadius: '8px', overflow: 'hidden', cursor: 'pointer', display: 'flex', flexDirection: 'column' }}
                  onClick={() => setLightboxImg(img)}
                >
                  <div style={{ position: 'relative', width: '100%', paddingTop: '100%', backgroundColor: '#0c0d12' }}>
                    <img 
                      src={img.src} 
                      alt={img.title}
                      style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                    <div style={{ position: 'absolute', top: '8px', left: '8px', backgroundColor: '#000000bb', color: '#39ff14', fontSize: '0.65rem', fontWeight: 700, padding: '2px 6px', borderRadius: '4px' }}>
                      VIEW {iIdx + 1}
                    </div>
                  </div>
                  <div style={{ padding: '0.85rem', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                    <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#ffffff', marginBottom: '0.35rem' }}>
                      {img.title}
                    </div>
                    <p style={{ fontSize: '0.75rem', color: '#94a3b8', margin: 0, lineHeight: 1.35 }}>
                      {img.caption}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Lightbox Modal */}
      {lightboxImg && (
        <div 
          style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', backgroundColor: '#000000ee', zIndex: 9999, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}
          onClick={() => setLightboxImg(null)}
        >
          <div 
            style={{ maxWidth: '900px', width: '100%', backgroundColor: '#12141c', border: '1px solid #2a3142', borderRadius: '12px', overflow: 'hidden' }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ position: 'relative', width: '100%', paddingTop: '80%', backgroundColor: '#0c0d12' }}>
              <img 
                src={lightboxImg.src} 
                alt={lightboxImg.title} 
                style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', objectFit: 'contain' }}
              />
            </div>
            <div style={{ padding: '1.25rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #1e2330' }}>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: '#ffffff', margin: '0 0 0.25rem 0' }}>{lightboxImg.title}</h3>
                <p style={{ fontSize: '0.85rem', color: '#94a3b8', margin: 0 }}>{lightboxImg.caption}</p>
              </div>
              <button 
                onClick={() => setLightboxImg(null)}
                style={{ backgroundColor: '#212634', color: '#cbd5e1', border: '1px solid #333a4c', padding: '0.5rem 1rem', borderRadius: '6px', fontSize: '0.85rem', fontWeight: 700, cursor: 'pointer' }}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
