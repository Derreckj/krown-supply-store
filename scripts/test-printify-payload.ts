/**
 * Test Harness: Printify Order Payload Validator & Resilient Fallback Runner
 */
import { printifyService, PrintifyOrderInput } from '../src/services/printify';

async function runPrintifyPayloadTest() {
  console.log('--- PRINTIFY ORDER PAYLOAD VALIDATION TEST ---');

  const sampleOrder: PrintifyOrderInput = {
    externalId: 'test_krown_order_9981',
    shippingMethod: 1,
    addressTo: {
      first_name: 'Marcus',
      last_name: 'Vance',
      email: 'mvance@example.com',
      phone: '5125550199',
      country: 'US',
      region: 'TX',
      address1: '401 Congress Ave Ste 1500',
      city: 'Austin',
      zip: '78701',
    },
    lineItems: [
      {
        productId: 'axiom-jersey-home',
        size: 'L',
        color: 'Obsidian Black / Royal Purple / Silver (Custom Gamertag)',
        quantity: 2,
        gamertag: 'VORTEX',
        playerNumber: '07',
      },
      {
        productId: 'krown-hat-btr-leather',
        size: 'OSFA',
        quantity: 1,
      },
      {
        productId: 'krown-hoodie-premium',
        size: 'XL',
        quantity: 1,
      },
    ],
  };

  const validation = printifyService.validatePrintifyOrderPayload(sampleOrder);
  console.log('1. Payload Validation Status:', validation.isValid ? 'VALID ✅' : 'INVALID ❌');
  if (validation.errors.length > 0) {
    console.log('Validation Errors/Warnings:', validation.errors);
  }

  console.log('2. Exact JSON Transmitted to Printify (/v1/shops/{shop_id}/orders.json):');
  console.log(JSON.stringify(validation.payload, null, 2));

  console.log('\n3. Execution through resilient createPrintifyOrder pipeline:');
  const executionResult = await printifyService.createPrintifyOrder(sampleOrder);
  console.log('Fulfillment Execution Result:', executionResult);
}

runPrintifyPayloadTest().catch(console.error);
