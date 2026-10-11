// scripts/verify_discounts.mjs
// Test Runner: Cart Calculation & Profit Margin Check
import { calculateKrown10Discount } from '../src/config/discounts.ts';

const hoodie = { id: 'axiom-hoodie-01', title: 'Axiom Allegiance Legacy Owl Hoodie — Statement Edition', category: 'hoodie', price: 98.00, quantity: 1 };
const sweatshirt = { id: 'axiom-sweatshirt-01', title: 'Axiom Allegiance Legacy Owl Crewneck — Statement Edition', category: 'sweatshirt', price: 54.99, quantity: 1 };
const hat = { id: 'axiom-r112-patch-01', title: 'Axiom Richardson 112 Genuine Leather Patch Trucker Snapback', category: 'hat', price: 34.99, quantity: 1 };
const shaker = { id: 'axiom-shaker-01', title: 'Axiom Allegiance Shaker Bottle', category: 'shaker', price: 27.99, quantity: 1 };

console.log('====================================================');
console.log('   KROWNSUPPLYCO PRODUCTION DISCOUNT VERIFICATION   ');
console.log('====================================================');

let allPassed = true;

function testScenario(name, items, expectedDiscount, expectValid) {
  // Execute validator
  const result = calculateKrown10Discount('KROWN10', items);

  const discount = result.discountAmount || 0;
  const valid = result.isValid;

  const discountMatch = Math.abs(discount - expectedDiscount) < 0.01;
  const statusMatch = valid === expectValid;

  if (discountMatch && statusMatch) {
    console.log(`[PASS] ${name}`);
    console.log(`       Discount: -$${discount.toFixed(2)} | Subtotal: $${items.reduce((s, i) => s + (i.price * i.quantity), 0).toFixed(2)} -> Due: $${(items.reduce((s, i) => s + (i.price * i.quantity), 0) - discount).toFixed(2)}`);
  } else {
    console.error(`[FAIL] ${name}`);
    console.error(`       Expected: Valid=${expectValid}, -$${expectedDiscount} | Got: Valid=${valid}, -$${discount}`);
    allPassed = false;
  }
}

// SCENARIO 1: Solo Sweatshirt (High-Margin)
testScenario('Scenario 1: 1x Statement Sweatshirt ($54.99)', [sweatshirt], 5.50, true);

// SCENARIO 2: Solo Richardson 112 Hat (High-Margin)
testScenario('Scenario 2: 1x Richardson 112 Snapback ($34.99)', [hat], 3.50, true);

// SCENARIO 3: Solo Shaker Bottle (High-Margin)
testScenario('Scenario 3: 1x Shaker Bottle ($27.99)', [shaker], 2.80, true);

// SCENARIO 4: Solo Statement Hoodie (MUST BE STRICTLY REJECTED)
testScenario('Scenario 4: 1x Statement Hoodie ($98.00) [EXCLUSION CHECK]', [hoodie], 0.00, false);

// SCENARIO 5: Mixed Cart (Hoodie $98.00 + Sweatshirt $54.99)
// Must ONLY discount the sweatshirt ($5.50 off). Hoodie must remain $98.00.
testScenario('Scenario 5: Mixed Cart (Hoodie + Sweatshirt)', [hoodie, sweatshirt], 5.50, true);

console.log('====================================================');
if (allPassed) {
  console.log('PROFIT SHIELD VERIFIED: ALL 5 SCENARIOS PASSED 100%');
} else {
  console.error('CRITICAL WARNING: PROFIT LEAK DETECTED. CHECK FAILURES ABOVE.');
  process.exit(1);
}
console.log('====================================================');
