/**
 * KrowN Supply Co. - Etsy Bulk Upload CSV Generator
 * 
 * Converts `docs/etsy-launch-catalog.json` into a standard Etsy-compatible CSV
 * formatted for bulk importing into the Etsy Shop Manager.
 * 
 * Strict Brand Rule: "KrowN" capitalization preserved.
 */

import * as fs from 'fs';
import * as path from 'path';

interface EtsyListingJson {
  id: string;
  sku: string;
  brandDivision: string;
  seoTitle: string;
  tags: string[];
  price: number;
  customerShipping: number;
  productionCost: number;
  materialDetails: string;
  sizingChartSummary: string;
  careInstructions: string;
  customOrderingInstructions?: string;
  fullDescription: string;
  images: string[];
}

function escapeCsvField(field: string | number | undefined): string {
  if (field === undefined || field === null) return '""';
  const str = String(field);
  // Double quotes inside fields must be escaped as two double quotes
  const escaped = str.replace(/"/g, '""');
  return `"${escaped}"`;
}

export function generateEtsyCsv(): { csvPath: string; rowsCount: number } {
  const jsonPath = path.resolve(process.cwd(), 'docs', 'etsy-launch-catalog.json');
  const csvOutputPath = path.resolve(process.cwd(), 'docs', 'etsy-bulk-catalog.csv');

  if (!fs.existsSync(jsonPath)) {
    throw new Error(`Source JSON file not found at ${jsonPath}`);
  }

  const raw = fs.readFileSync(jsonPath, 'utf-8');
  const items = JSON.parse(raw) as EtsyListingJson[];

  // Official Etsy bulk upload compatible CSV column headers
  const headers = [
    'Title',
    'Description',
    'Price',
    'Quantity',
    'SKU',
    'Tags',
    'Materials',
    'Shop Section',
    'Item Type',
    'Who Made It',
    'When Made',
    'Customizable',
    'Personalization Instructions',
    'Primary Image',
    'Secondary Images',
    'Shipping Profile',
  ];

  const rows: string[] = [headers.join(',')];

  for (const item of items) {
    const isCustom = Boolean(item.customOrderingInstructions);
    const primaryImg = item.images[0] || '';
    const otherImgs = item.images.slice(1).join(' | ');
    const formattedTags = item.tags.join(', ');

    const row = [
      escapeCsvField(item.seoTitle),
      escapeCsvField(item.fullDescription),
      escapeCsvField(item.price.toFixed(2)),
      escapeCsvField(999), // POD inventory
      escapeCsvField(item.sku),
      escapeCsvField(formattedTags),
      escapeCsvField(item.materialDetails),
      escapeCsvField(item.brandDivision),
      escapeCsvField('physical'),
      escapeCsvField('someone_else'), // POD production partner
      escapeCsvField('made_to_order'),
      escapeCsvField(isCustom ? 'true' : 'false'),
      escapeCsvField(item.customOrderingInstructions || 'N/A - Standard Item'),
      escapeCsvField(primaryImg),
      escapeCsvField(otherImgs),
      escapeCsvField('Standard US Free Shipping (3-5 Days)'),
    ];

    rows.push(row.join(','));
  }

  const csvContent = rows.join('\r\n');
  fs.writeFileSync(csvOutputPath, csvContent, 'utf-8');

  console.log(`✅ Etsy Bulk CSV successfully created at: ${csvOutputPath}`);
  console.log(`   Total items converted: ${items.length}`);

  return {
    csvPath: csvOutputPath,
    rowsCount: items.length,
  };
}

if (require.main === module || process.argv[1]?.includes('generate-etsy-csv')) {
  generateEtsyCsv();
}
