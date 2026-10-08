/* eslint-disable @typescript-eslint/no-require-imports */
const fs = require('fs');

const env = fs.readFileSync('.env.local', 'utf8');
const keyMatch = env.match(/PRINTIFY_API_KEY=(.*)/);
if (!keyMatch) {
  console.error('No PRINTIFY_API_KEY found');
  process.exit(1);
}
const apiKey = keyMatch[1].trim();
const shopId = '29241235';

// Uploaded asset IDs from our previous sync:
const ASSETS = {
  axiomOwlMascot: '6ac70061b193f868adb8a466',
  axiomOwlDisplay: '6ac7007408e4cece8eaa2594',
  kcLogoBW: '6ac7007a5f4cf1b1cf651aa5',
  kcLogoBlack: '6ac7007b585dbaac12017033',
  kcLogoWhite: '6ac7007c6886de57cfdc0cb2',
  kcEmblemColor: '6ac7007d077755cc444de3b2',
};

async function createProduct(title, description, blueprintId, imageId, scale = 1.0) {
  console.log(`\nCreating "${title}" (Blueprint ${blueprintId})...`);

  // 1. Fetch print providers
  const pRes = await fetch(`https://api.printify.com/v1/catalog/blueprints/${blueprintId}/print_providers.json`, {
    headers: { 'Authorization': 'Bearer ' + apiKey }
  });
  const providers = await pRes.json();
  if (!providers || providers.length === 0) {
    console.error(`No print providers for blueprint ${blueprintId}`);
    return null;
  }

  // Use top provider
  const provider = providers[0];
  console.log(`  Using Print Provider: ${provider.title} (ID ${provider.id})`);

  // 2. Fetch variants
  const vRes = await fetch(`https://api.printify.com/v1/catalog/blueprints/${blueprintId}/print_providers/${provider.id}/variants.json`, {
    headers: { 'Authorization': 'Bearer ' + apiKey }
  });
  const vData = await vRes.json();
  if (!vData.variants || vData.variants.length === 0) {
    console.error(`No variants found for blueprint ${blueprintId}`);
    return null;
  }

  // Pick up to 5 popular variants
  const selectedVariants = vData.variants.slice(0, 5);
  const variantPayload = selectedVariants.map(v => ({
    id: v.id,
    price: 1999, // placeholder default price (in cents)
    is_enabled: true
  }));

  const variantIds = selectedVariants.map(v => v.id);

  const payload = {
    title,
    description: `<p>${description}</p>`,
    blueprint_id: blueprintId,
    print_provider_id: provider.id,
    variants: variantPayload,
    print_areas: [
      {
        variant_ids: variantIds,
        placeholders: [
          {
            position: 'front',
            images: [
              {
                id: imageId,
                x: 0.5,
                y: 0.5,
                scale: scale,
                angle: 0
              }
            ]
          }
        ]
      }
    ]
  };

  const createRes = await fetch(`https://api.printify.com/v1/shops/${shopId}/products.json`, {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + apiKey,
      'Content-Type': 'application/json',
      'User-Agent': 'KrowN-Supply/1.0'
    },
    body: JSON.stringify(payload)
  });

  const data = await createRes.json();
  if (createRes.ok && data.id) {
    console.log(`  ✓ Created successfully! Product ID: ${data.id}`);
    return data;
  } else {
    console.error(`  ✗ Creation failed:`, JSON.stringify(data, null, 2));
    return null;
  }
}

async function main() {
  console.log('=== CREATING PRODUCT BLUEPRINTS IN PRINTIFY SHOP 29241235 ===');

  // 1. Axiom Owl Kiss-Cut Stickers (Blueprint 400)
  await createProduct(
    'Axiom Owl Holographic Kiss-Cut Vinyl Stickers',
    'Official esports die-cut stickers for Axiom Allegiance. High-density vinyl with UV and scratch resistance. Perfect for PCs, consoles, laptops, and hardhats.',
    400,
    ASSETS.axiomOwlMascot,
    0.85
  );

  // 2. KrowN Construction Tradesman Decal (Blueprint 400)
  await createProduct(
    'KrowN Construction Tradesman Hardhat Decal',
    'Official heavy-duty vinyl decal for KrowN Construction LLC. Built to Reign. Engineered to withstand jobsite grit, rain, and UV sunlight.',
    400,
    ASSETS.kcLogoBW,
    0.85
  );

  // 3. KrowN 20oz Vacuum Jobsite Tumbler (Blueprint 353)
  await createProduct(
    'KrowN 20oz Vacuum Insulated Jobsite Tumbler',
    'Double-wall vacuum insulated stainless steel tumbler with clear slider lid. Keeps beverages piping hot for 8 hours or ice-cold for 24 hours. Built to Reign.',
    353,
    ASSETS.kcLogoWhite,
    0.65
  );

  // 4. Comfort Colors 1717 Vintage Tee (Blueprint 706)
  await createProduct(
    'KrowN "Wear The Krown" Comfort Colors 1717 Vintage Heavy Tee',
    'Authentic Comfort Colors 1717 garment-dyed 100% ring-spun cotton tee with vintage broken-in wash. Relaxed boxy streetwear fit. Wear the KrowN.',
    706,
    ASSETS.kcLogoBlack,
    0.75
  );

  console.log('\n=== PRINTIFY PRODUCT BLUEPRINTS CREATED SUCCESSFULLY ===');
}

main();
