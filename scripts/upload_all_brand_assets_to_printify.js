/* eslint-disable @typescript-eslint/no-require-imports */
const fs = require('fs');
const path = require('path');

const env = fs.readFileSync('.env.local', 'utf8');
const keyMatch = env.match(/PRINTIFY_API_KEY=(.*)/);
if (!keyMatch) {
  console.error('No PRINTIFY_API_KEY found in .env.local');
  process.exit(1);
}
const apiKey = keyMatch[1].trim();

const assetsToUpload = [
  {
    name: 'Axiom Owl Mascot (Transparent High-Res)',
    file_name: 'axiom-owl-mascot.png',
    path: path.join('public', 'images', 'branding', 'gaming', 'axiom-owl-mascot.png')
  },
  {
    name: 'Axiom Owl Panoramic Display Art (Desk Mats & Posters)',
    file_name: 'axiom-owl-display.png',
    path: path.join('public', 'images', 'branding', 'gaming', 'axiom-owl-display.png')
  },
  {
    name: 'Axiom Gorilla Mascot (Transparent)',
    file_name: 'axiom-gorilla-mascot.png',
    path: path.join('public', 'images', 'branding', 'gaming', 'axiom-gorilla-mascot.png')
  },
  {
    name: 'KrowN Construction Monogram Crest (Black & White)',
    file_name: 'KC-logo-black-and-white.png',
    path: path.join('public', 'images', 'branding', 'construction', 'KC logo black and white.png')
  },
  {
    name: 'KrowN Construction Full Logo (Black)',
    file_name: 'Krown-Construction-Black.png',
    path: path.join('public', 'images', 'branding', 'construction', 'Krown ConstructionPNG Black.PNG')
  },
  {
    name: 'KrowN Construction Full Logo (White)',
    file_name: 'Krown-Construction-White.png',
    path: path.join('public', 'images', 'branding', 'construction', 'KrownConstruction PNG white.PNG')
  },
  {
    name: 'KrowN Construction Emblem (Full Color)',
    file_name: 'KC-emblem-full-color.png',
    path: path.join('public', 'images', 'branding', 'construction', 'Krown Construction.png')
  },
  {
    name: 'Axiom Custom Split Arm Sleeve Pattern (Clean Blueprint)',
    file_name: 'axiom-arm-sleeve-pattern.png',
    path: path.join('public', 'images', 'products', 'axiom-arm-sleeve-flat.png')
  }
];

async function uploadFile(asset) {
  if (!fs.existsSync(asset.path)) {
    console.warn(`File does not exist: ${asset.path}`);
    return null;
  }

  const buffer = fs.readFileSync(asset.path);
  const base64 = buffer.toString('base64');
  console.log(`Uploading [${asset.name}] (${(buffer.length / 1024).toFixed(1)} KB)...`);

  try {
    const res = await fetch('https://api.printify.com/v1/uploads/images.json', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'User-Agent': 'KrowN-Supply/1.0'
      },
      body: JSON.stringify({
        file_name: asset.file_name,
        contents: base64
      })
    });

    const data = await res.json();
    if (res.ok && data.id) {
      console.log(`  ✓ Uploaded successfully! ID: ${data.id} (${data.width}x${data.height}px)`);
      return { ...asset, printifyId: data.id, previewUrl: data.preview_url };
    } else {
      console.error(`  ✗ Upload failed:`, data);
      return null;
    }
  } catch (err) {
    console.error(`  ✗ Error:`, err.message);
    return null;
  }
}

async function main() {
  console.log('=== SYNCING ARTWORK TO PRINTIFY "MY LIBRARY" ===\n');
  const results = [];
  for (const asset of assetsToUpload) {
    const res = await uploadFile(asset);
    if (res) results.push(res);
  }

  console.log(`\n=== SYNC COMPLETE: ${results.length}/${assetsToUpload.length} ASSETS UPLOADED ===`);
  const manifestPath = path.join('docs', 'PRINTIFY_UPLOADED_ASSETS.json');
  fs.writeFileSync(manifestPath, JSON.stringify(results, null, 2));
  console.log(`Saved asset manifest to ${manifestPath}`);
}

main();
