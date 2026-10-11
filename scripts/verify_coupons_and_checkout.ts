import { validateDiscountCode } from '../src/lib/discounts';
import { stripe } from '../src/lib/stripe';

async function verifyCouponsAndCheckout() {
  console.log("=== 1. VERIFYING COUPON CODES ===");
  const testCodes = ['Krown10', 'krown10', 'KROWN10', 'krown15', 'Krown15', 'KROWN15', 'invalid10'];
  
  for (const c of testCodes) {
    const res = validateDiscountCode(c);
    if (res) {
      console.log(`✓ '${c}' -> VALID! Percentage: ${res.percentage}% (${res.label})`);
    } else {
      console.log(`✗ '${c}' -> Invalid (as expected)`);
    }
  }

  console.log("\n=== 2. VERIFYING STRIPE CHECKOUT WITH Krown10 ===");
  const disc10 = validateDiscountCode('Krown10')!;
  const originalPrice = 49.99;
  const discountedPrice = originalPrice * (1 - disc10.percentage / 100);

  const session10 = await stripe.checkout.sessions.create({
    mode: 'payment',
    line_items: [
      {
        price_data: {
          currency: 'usd',
          product_data: {
            name: 'Axiom Allegiance Official Crewneck Sweatshirt',
            description: `Size: L | Obsidian Black | Promo ${disc10.code}: -${disc10.percentage}% applied`,
          },
          unit_amount: Math.round(discountedPrice * 100),
        },
        quantity: 1,
      },
    ],
    invoice_creation: { enabled: true },
    shipping_address_collection: { allowed_countries: ['US', 'CA'] },
    billing_address_collection: 'required',
    success_url: 'https://www.krownsupplyco.com/checkout/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url: 'https://www.krownsupplyco.com/checkout/cancel',
    metadata: {
      discount_code: disc10.code,
      discount_percentage: disc10.percentage.toString(),
    },
  });

  console.log(`✓ Stripe Session with Krown10 created successfully!`);
  console.log(`  Amount: $${(session10.amount_total! / 100).toFixed(2)} (Original: $${originalPrice}, Discounted: $${discountedPrice.toFixed(2)})`);
  console.log(`  Checkout URL: ${session10.url?.slice(0, 75)}...`);

  console.log("\n=== 3. VERIFYING STRIPE CHECKOUT WITH krown15 ===");
  const disc15 = validateDiscountCode('krown15')!;
  const discountedPrice15 = originalPrice * (1 - disc15.percentage / 100);

  const session15 = await stripe.checkout.sessions.create({
    mode: 'payment',
    line_items: [
      {
        price_data: {
          currency: 'usd',
          product_data: {
            name: 'Axiom Allegiance Official Crewneck Sweatshirt',
            description: `Size: L | Obsidian Black | Promo ${disc15.code}: -${disc15.percentage}% applied`,
          },
          unit_amount: Math.round(discountedPrice15 * 100),
        },
        quantity: 1,
      },
    ],
    invoice_creation: { enabled: true },
    shipping_address_collection: { allowed_countries: ['US', 'CA'] },
    billing_address_collection: 'required',
    success_url: 'https://www.krownsupplyco.com/checkout/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url: 'https://www.krownsupplyco.com/checkout/cancel',
    metadata: {
      discount_code: disc15.code,
      discount_percentage: disc15.percentage.toString(),
    },
  });

  console.log(`✓ Stripe Session with krown15 created successfully!`);
  console.log(`  Amount: $${(session15.amount_total! / 100).toFixed(2)} (Original: $${originalPrice}, Discounted: $${discountedPrice15.toFixed(2)})`);
  console.log(`  Checkout URL: ${session15.url?.slice(0, 75)}...`);
}

verifyCouponsAndCheckout().catch(console.error);
