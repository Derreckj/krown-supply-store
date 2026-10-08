const fs = require('fs');

const env = fs.readFileSync('.env.local', 'utf8');
const keyMatch = env.match(/PRINTIFY_API_KEY=(.*)/);
if (!keyMatch) {
  console.error('No PRINTIFY_API_KEY found');
  process.exit(1);
}
const apiKey = keyMatch[1].trim();
const sourceShopId = 29241235;
const targetEtsyShopId = 29252381;

const productOverrides = {
  '6ac700d2e586b62fb50465b2': {
    title: '20oz Vacuum Insulated Jobsite Tumbler - Matte Black Stainless Steel Coffee Travel Mug with Laser Engraved Gold Crest, Construction Gift',
    tags: [
      'construction tumbler', 'jobsite coffee mug', 'tradesman gift', 'blue collar gift',
      'insulated tumbler', 'stainless steel mug', 'travel coffee mug', '20oz tumbler',
      'carpenter gift', 'laser engraved mug', 'electrician gift', 'workwear tumbler', 'built to reign'
    ]
  },
  '6ac700d0e586b62fb50465ad': {
    title: 'Hardhat Sticker Pack (5-Pack) - Weatherproof Vinyl Decals for Tool Box, Construction Tradesman Gift, Blue Collar Pride, Built to Reign',
    tags: [
      'hardhat stickers', 'tradesman decals', 'blue collar gift', 'construction stickers',
      'tool box decals', 'lineman gift', 'carpenter sticker', 'electrician hardhat',
      'welder stickers', 'weatherproof decal', 'hard hat accessories', 'workwear stickers', 'built to reign'
    ]
  },
  '6ac700cf826b7669c103bbda': {
    title: 'Axiom Owl Holographic Kiss-Cut Vinyl Stickers - Esports Decal for PC Case, Laptop, Water Bottle, Streamer Gaming Gift',
    tags: [
      'holographic sticker', 'gaming sticker', 'esports decal', 'pc gamer gift',
      'laptop sticker', 'streamer decal', 'owl gaming decal', 'battle station decor',
      'water bottle decal', 'anime gaming decal', 'twitch streamer gift', 'vinyl decal', 'axiom allegiance'
    ]
  },
  '6ac700b20a223533b30704f4': {
    title: 'Axiom Owl Panoramic Gaming Desk Mat (32x16) - Large Extended Mouse Pad for PC Battle Station, Non-Slip Esports Mousepad',
    tags: [
      'gaming desk mat', 'large mouse pad', '32x16 desk pad', 'esports mousepad',
      'streamer desk setup', 'pc gamer gift', 'owl desk mat', 'battle station mat',
      'extended mousepad', 'gaming accessories', 'purple desk mat', 'clean desk setup', 'axiom allegiance'
    ]
  }
};

async function syncAll() {
  console.log(`Starting automated sync from Shop ${sourceShopId} to Etsy Shop ${targetEtsyShopId}...`);

  for (const [prodId, override] of Object.entries(productOverrides)) {
    try {
      console.log(`\nFetching product ${prodId}...`);
      const getRes = await fetch(`https://api.printify.com/v1/shops/${sourceShopId}/products/${prodId}.json`, {
        headers: { 'Authorization': 'Bearer ' + apiKey }
      });
      if (!getRes.ok) {
        console.error(`Failed to fetch ${prodId}: ${getRes.status} ${getRes.statusText}`);
        continue;
      }
      const prod = await getRes.json();

      // Clean print areas by removing empty placeholder image arrays
      const cleanedPrintAreas = prod.print_areas.map(pa => ({
        variant_ids: pa.variant_ids,
        placeholders: pa.placeholders.filter(pl => pl.images && pl.images.length > 0)
      }));

      const payload = {
        title: override.title || prod.title,
        description: prod.description,
        tags: override.tags || prod.tags,
        blueprint_id: prod.blueprint_id,
        print_provider_id: prod.print_provider_id,
        variants: prod.variants.map(v => ({
          id: v.id,
          price: v.price,
          is_enabled: v.is_enabled
        })),
        print_areas: cleanedPrintAreas
      };

      console.log(`Creating "${payload.title.slice(0, 50)}..." in Etsy Shop...`);
      const createRes = await fetch(`https://api.printify.com/v1/shops/${targetEtsyShopId}/products.json`, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + apiKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const newProd = await createRes.json();
      if (!newProd.id) {
        console.error(`Error creating product:`, newProd);
        continue;
      }

      console.log(`✓ Created in Etsy Shop with ID: ${newProd.id}`);

      // Publish directly to Etsy
      console.log(`Publishing ${newProd.id} to Etsy...`);
      const pubRes = await fetch(`https://api.printify.com/v1/shops/${targetEtsyShopId}/products/${newProd.id}/publish.json`, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + apiKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: true,
          description: true,
          images: true,
          variants: true,
          tags: true,
          keyFeatures: true,
          shipping_template: true
        })
      });

      if (pubRes.ok) {
        console.log(`★ Successfully published to Etsy: "${payload.title.slice(0, 50)}..."`);
      } else {
        const pubErr = await pubRes.text();
        console.error(`Publish error for ${newProd.id}:`, pubErr);
      }
    } catch (err) {
      console.error(`Exception syncing ${prodId}:`, err);
    }
  }

  console.log('\n--- Sync Pipeline Complete ---');
}

syncAll();
