# KrowN Supply Store - Brand & Catalog Asset Integrity Bible

## CRITICAL DIRECTIVE: ZERO BRAND CROSSOVER & ZERO LOW-QUALITY MOCKUPS
This project manages three distinct, strictly separated brands. Violating brand boundaries or producing low-quality mockups (pasted rectangles, artificial ellipses, pillarboxed images) breaks the live production store and is strictly prohibited.

---

### 1. STRICT BRAND SILOS & SEPARATION CONTRACT

#### Brand 1: Axiom Allegiance (Esports & Gaming Division)
- **Primary Mascot**: Official Axiom Owl Crest only.
- **Brand Colors**: Royal Purple (`#8B5CF6`), Toxic Neon Green (`#22C55E` / `#10B981`), Midnight Obsidian Black.
- **Environment & Theme**: High-tier competitive esports, dark gaming battlestations, neon studio lighting, tournament apparel.
- **STRICT PROHIBITIONS**:
  - **NEVER** place a gold crown on Axiom Allegiance items.
  - **NEVER** mix KrowN Supply Co. or KrowN Construction logos, slogans, or marks into Axiom products.
  - **NEVER** use construction tools, workbenches, or hardhat decals on Axiom gear.

#### Brand 2: KrowN Construction (Heavy-Duty Jobsite Division)
- **Primary Mark**: Official KC Monogram with hammer/trowel icon & laser gold "BUILT TO REIGN" typography.
- **Brand Colors**: Laser Etched Gold (`#D4AF37`), Industrial Steel (`#A0A5B0`), High-Vis Safety Gold/Orange, Slate Charcoal.
- **Environment & Theme**: Heavy-duty industrial jobsite, workshop steel workbench, pegboard with tools, construction gear.
- **STRICT PROHIBITIONS**:
  - **NEVER** place an Axiom Owl or gaming owl mascot on KrowN Construction products.
  - **NEVER** place products on esports gaming desks, beside Razer mice, mechanical keyboards, or purple RGB lights.
  - **NEVER** use purple/neon green esports color schemes.

#### Brand 3: KrowN Supply Co. (Flagship Luxury Streetwear)
- **Primary Mark**: 3D Metallic Antique Gold K-Crown Monogram, "K R O W N SUPPLY CO.", "WEAR THE KROWN".
- **Brand Colors**: Antique Metallic Gold (`#D4AF37` / `#F5E182`), Matte Obsidian Black, French Terry Vintage Washed Charcoal.
- **Environment & Theme**: Architectural minimalist luxury studio, clean slate/stone surfaces, high-end designer streetwear aesthetic.
- **STRICT PROHIBITIONS**:
  - **NEVER** place products in gaming setups (no keyboards, mice, monitors).
  - **NEVER** draw artificial background shapes, arches, or olive ellipses (e.g. `fill=(48, 38, 16)`).
  - **NEVER** use Axiom Owl mascots or construction slogans.

---

### 2. PRODUCT IMAGE QUALITY STANDARDS

1. **Full-Bleed 1024×1024 Dimensions**:
   - All product images and thumbnails MUST be full-bleed 1024×1024 square images.
   - Zero black side pillarboxes, zero letterboxes, zero vertical narrow strips.

2. **No Pasted Sticker Bounding Boxes**:
   - Any graphic on fabric or bottles must have a clean alpha mask with realistic blending, subtle fabric weave interaction, ambient occlusion contact shadow, and directional light wrap.
   - NEVER paste opaque rectangular image crops onto clothing or products.

3. **Master Vault Single Source of Truth**:
   - All approved product photos are stored in `public/images/products/masters/`.
   - Never run unverified bulk regeneration scripts that overwrite approved catalog files.
   - Always run `python scripts/verify_catalog_integrity.py` before any deployment.

4. **Visual Verification Protocol**:
   - Before deploying any updated product image, visually inspect the image using `view_file` to confirm realistic rendering, correct branding, and zero artifacts.
