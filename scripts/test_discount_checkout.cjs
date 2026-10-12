// Run: node scripts/test_discount_checkout.cjs
// Transpile the actual route and replace Stripe with an in-memory capture: no network or charges.
/* eslint-disable @typescript-eslint/no-require-imports -- Standalone Node CommonJS test harness. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ts = require('typescript');

const root = path.resolve(__dirname, '..');
const cache = new Map();
let capturedSession;
let sessionCount = 0;
let heldCheckoutCount = 0;
function loadSource(relativePath, isolation = 'default-source-hold') {
  const cacheKey = `${isolation}:${relativePath}`;
  if (cache.has(cacheKey)) return cache.get(cacheKey);
  const sourceModule = { exports: {} };
  cache.set(cacheKey, sourceModule.exports);
  const { outputText } = ts.transpileModule(fs.readFileSync(path.join(root, relativePath), 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
    fileName: relativePath,
  });
  const requireMock = (name) => {
    if (name === '@/config/discounts') return loadSource('src/config/discounts.ts', isolation);
    if (name === '@/config/catalog-holds') {
      // Test-only dependency replacement isolates discount calculations from readiness.
      // The default route below always loads the real incident gate.
      if (isolation === 'discount-pricing-only') return { getCatalogPurchaseHold: () => null };
      return loadSource('src/config/catalog-holds.ts', isolation);
    }
    if (name === '@/lib/discounts') return loadSource('src/lib/discounts.ts', isolation);
    if (name === 'next/server') return { NextResponse: { json: (body, options) => ({ body, status: options?.status || 200 }) } };
    if (name === '@/lib/stripe') return {
      isStripeConfigured: () => true,
      stripe: { checkout: { sessions: { create: async (params) => {
        capturedSession = params;
        sessionCount++;
        return { url: 'https://example.invalid/mock-checkout' };
      } } } },
    };
    throw new Error(`Unexpected dependency in isolated checkout test: ${name}`);
  };
  vm.runInNewContext(outputText, { module: sourceModule, exports: sourceModule.exports, require: requireMock, process: { env: {} }, console }, { filename: relativePath });
  return sourceModule.exports;
}

const { POST } = loadSource('src/app/api/checkout/route.ts');
const { POST: pricingPOST } = loadSource('src/app/api/checkout/route.ts', 'discount-pricing-only');
const holds = loadSource('src/config/catalog-holds.ts');
assert.equal(holds.WEBSITE_ORDERING_PAUSED, true);
const discounts = loadSource('src/lib/discounts.ts');
const config = loadSource('src/config/discounts.ts');
const heldHat = { id: 'custom-krown-works-hat-Black-One Size', productId: 'custom-krown-works-hat', name: 'Custom Crew Hat', price: 34.99, quantity: 2, image: '/hat.jpg', variant: { color: 'Black', size: 'One Size' } };
// Hypothetical nonheld fixture isolates pricing behavior from the current supplier hold.
const hat = { ...heldHat, id: 'custom-hat-test-fixture-Black-One Size', productId: 'custom-hat-test-fixture' };
const tee = { id: 'supply-tee-Black-M', productId: 'supply-tee', name: 'Supply Tee', price: 11.95, quantity: 3, image: '/tee.jpg', variant: { color: 'Black', size: 'M' } };
const hoodie = { id: 'axiom-hoodie-01-Black-L', productId: 'axiom-hoodie-01', name: 'Axiom Allegiance Statement Hoodie', price: 98, quantity: 1, image: '/hoodie.jpg', variant: { color: 'Black', size: 'L' } };

async function checkout(items, discountCode) {
  capturedSession = undefined;
  const response = await pricingPOST({ json: async () => ({ items, discountCode }), headers: { get: () => 'https://www.krownsupplyco.com' } });
  assert.equal(response.status, 200);
  assert.equal(response.body.url, 'https://example.invalid/mock-checkout');
  assert.ok(capturedSession);
  return capturedSession;
}

(async () => {
  for (const [code, percentage, teeCents] of [
    ['Krown10', 10, 1076], ['kRoWn10', 10, 1076], [' KROWN10 ', 10, 1076],
    ['KrowN15', 15, 1016], ['krown15', 15, 1016], [' KROWN15 ', 15, 1016],
  ]) {
    const canonical = discounts.validateDiscountCode(code);
    assert.equal(canonical.percentage, percentage);
    const mixed = await checkout([hat, tee, hoodie], code);
    assert.deepEqual(Array.from(mixed.line_items, line => line.price_data.unit_amount), [3499, teeCents, 9800]);
    assert.equal(mixed.allow_promotion_codes, false);
    assert.equal(mixed.line_items[0].price_data.product_data.metadata.discount_code, 'EXCLUDED_OR_NONE');
    assert.equal(mixed.line_items[1].price_data.product_data.metadata.discount_code, code.trim().toUpperCase());
    const expectedTotal = (3499 * 2 + teeCents * 3 + 9800) / 100;
    // Even while this current product is held, both discount helpers must exclude its price.
    const breakdown = discounts.calculateCartDiscount([heldHat, tee, hoodie], canonical);
    assert.equal(breakdown.finalTotal, expectedTotal);
    assert.equal(breakdown.discountAmount, (1195 - teeCents) * 3 / 100);
    assert.equal(breakdown.hasCustomHats, true);
    assert.equal(breakdown.hasExcludedHoodie, true);
    const legacy = config.calculateKrown10Discount(code, [heldHat, tee, hoodie].map(item => ({ id: item.productId, title: item.name, price: item.price, quantity: item.quantity })));
    assert.equal(legacy.isValid, true);
    assert.equal(legacy.discountAmount, breakdown.discountAmount);

    const hatsOnly = await checkout([hat], code);
    assert.equal(hatsOnly.line_items[0].price_data.unit_amount, 3499);
    assert.equal(hatsOnly.allow_promotion_codes, false);
    assert.equal(discounts.calculateCartDiscount([heldHat], canonical).discountAmount, 0);
    assert.equal(config.calculateKrown10Discount(code, [{ id: heldHat.productId, title: heldHat.name, price: heldHat.price, quantity: heldHat.quantity }]).isValid, false);
  }
  for (const code of [undefined, 'BADCODE']) {
    const mixed = await checkout([hat, tee], code);
    assert.deepEqual(Array.from(mixed.line_items, line => line.price_data.unit_amount), [3499, 1195]);
    assert.equal(mixed.allow_promotion_codes, false);
    const hatsOnly = await checkout([hat], code);
    assert.equal(hatsOnly.allow_promotion_codes, false);
    assert.equal(hatsOnly.line_items[0].price_data.unit_amount, 3499);
    const hoodieOnly = await checkout([hoodie], code);
    assert.equal(hoodieOnly.allow_promotion_codes, false);
  }
  assert.equal((await checkout([tee])).allow_promotion_codes, true);
  for (const [code, unitAmount] of [['Krown10', 1076], ['KrowN15', 1016]]) {
    const eligibleOnly = await checkout([tee], code);
    assert.equal(eligibleOnly.line_items[0].price_data.unit_amount, unitAmount);
    assert.equal(eligibleOnly.allow_promotion_codes, false);
  }
  const heldProductIds = [
    'custom-krown-works-hat', 'axiom-r112-patch-01',
    '6ac80dc2f4d488e1be0b0902', '6ac8f2e9b0b07f13520b055c',
    'kc-stickers-01', '6ac7ed44fea4d4e68e0a0f80', '6ac700d0e586b62fb50465ad',
  ];
  // Derive the IDs from the current actual catalogue, not a stale hand-maintained copy.
  const productSource = fs.readFileSync(path.join(root, 'src/services/printify.ts'), 'utf8');
  const catalogueStart = productSource.indexOf('const INITIAL_MOCK_CATALOG');
  const catalogueEnd = productSource.indexOf('\n];', catalogueStart);
  assert.ok(catalogueStart >= 0 && catalogueEnd > catalogueStart);
  const websiteProductIds = Array.from(productSource.slice(catalogueStart, catalogueEnd).matchAll(/^    id: '([^']+)'/gm), match => match[1]);
  assert.equal(websiteProductIds.length, 26, 'Review coverage if the actual catalogue changes');
  assert.equal(new Set(websiteProductIds).size, 26);
  const allBlockedIds = [...new Set([...websiteProductIds, ...heldProductIds, 'unknown-product-id'])];
  const genericMessage = 'Ordering is temporarily paused while we verify production details. Please check back soon.';
  for (const productId of allBlockedIds) {
    const specificReason = holds.getCatalogPurchaseHold(productId);
    assert.ok(specificReason);
    if (heldProductIds.includes(productId)) assert.match(specificReason, /^Ordering paused/);
    else assert.equal(specificReason, genericMessage);
    for (const code of [undefined, 'Krown10', 'kRoWn10', 'KrowN15', 'kRoWn15', 'BADCODE']) {
      // Singles and mixed carts in either order include upper-case ID and discount attempts.
      const blockedItem = { ...heldHat, productId };
      const upperCaseItem = { ...blockedItem, productId: productId.toUpperCase() };
      for (const items of [[blockedItem], [upperCaseItem], [tee, upperCaseItem], [upperCaseItem, tee]]) {
        capturedSession = undefined;
        const previousSessionCount = sessionCount;
        const response = await POST({ json: async () => ({ items, discountCode: code }), headers: { get: () => 'https://www.krownsupplyco.com' } });
        assert.equal(response.status, 409);
        assert.equal(response.body.productId, items[0].productId);
        assert.equal(response.body.error, holds.getCatalogPurchaseHold(items[0].productId));
        assert.equal(response.body.url, undefined);
        assert.equal(capturedSession, undefined);
        assert.equal(sessionCount, previousSessionCount, 'Production incident gate must reject before ANY Stripe session creation');
        heldCheckoutCount++;
      }
    }
  }
  // Each entry in a mixed cart is held individually; the first explains the rejection.
  capturedSession = undefined;
  const previousSessionCount = sessionCount;
  const allProductsResponse = await POST({ json: async () => ({ items: websiteProductIds.map(productId => ({ ...tee, productId })), discountCode: 'KROWN15' }), headers: { get: () => 'https://www.krownsupplyco.com' } });
  assert.equal(allProductsResponse.status, 409);
  assert.equal(sessionCount, previousSessionCount);
  assert.equal(capturedSession, undefined);
  heldCheckoutCount++;
  assert.equal(config.calculateKrown10Discount('invalid', []).isValid, false);
  for (const item of [
    { productId: 'CUSTOM-KROWN-WORKS-HAT' },
    { id: 'custom-hat-Black' },
    { name: 'Custom Richardson 112' },
    { title: 'Custom Crew Hat' },
    { name: 'Hat', variant: { color: 'Leather Patch', size: 'One Size' } },
  ]) assert.equal(discounts.isCustomHatItem(item), true);
  assert.equal(discounts.isExcludedDiscountItem({ productId: 'AXIOM-HOODIE-01' }), true);
  console.log(`PASS: ${sessionCount} discount-only checkout route calls mocked with an isolated test stub and ${heldCheckoutCount} real-default-source checkout calls rejected before Stripe (all 26 catalogue IDs, seven existing hold IDs/aliases, unknown ID, case variants and mixed carts). Both codes, case variants, held legacy/current IDs, mixed/hat-only carts, eligible-only carts, cent rounding, hoodie policy and Stripe bypass checked. No real sessions or charges.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
