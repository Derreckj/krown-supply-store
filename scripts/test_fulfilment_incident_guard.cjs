// No network: verify held checkouts cannot reach Stripe line-item retrieval or Printify.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ts = require('typescript');
const root = path.resolve(__dirname, '..');
let lineItemCalls = 0;
let supplierCalls = 0;
let verifiedEvents = 0;
const originalEnv = { NODE_ENV: process.env.NODE_ENV, STRIPE_WEBHOOK_SECRET: process.env.STRIPE_WEBHOOK_SECRET };
const logs = [];
const stripe = {
  webhooks: { constructEvent(body, signature, secret) {
    assert.equal(secret, 'whsec_mock_test_only');
    if (signature !== 'mock-valid-signature') throw new Error('Invalid test signature');
    verifiedEvents++;
    return JSON.parse(body);
  } },
  checkout: { sessions: { listLineItems() { lineItemCalls++; throw new Error('Held webhook must not retrieve line items'); } } },
};
function load(relativePath) {
  const mod = { exports: {} };
  const code = ts.transpileModule(fs.readFileSync(path.join(root, relativePath), 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
  }).outputText;
  new Function('require', 'module', 'exports', 'process', 'console', code)((name) => {
    if (name === '@/lib/stripe') return { stripe };
    if (name === '@/config/catalog-holds') return load('src/config/catalog-holds.ts');
    if (name === 'next/server') return { NextResponse: { json: (body, options) => ({ body, status: options?.status || 200 }) } };
    if (name === '@/services/printify') return { printifyService: { createPrintifyOrder() { supplierCalls++; throw new Error('No supplier call authorized'); } } };
    throw new Error(`Unexpected dependency ${name}`);
  }, mod, mod.exports, process, { log: (...args) => logs.push(args), warn: (...args) => logs.push(args), error: (...args) => logs.push(args) });
  return mod.exports;
}
const { POST } = load('src/app/api/webhooks/stripe/route.ts');
const event = (type) => ({ id: 'evt_mock_incident', type, data: { object: { id: 'cs_mock_incident', payment_status: 'paid', customer_details: { email: 'private-customer@example.invalid' } } } });
const request = (type, signature = 'mock-valid-signature') => ({ text: async () => JSON.stringify(event(type)), headers: { get: () => signature } });
(async () => {
  process.env.NODE_ENV = 'production';
  delete process.env.STRIPE_WEBHOOK_SECRET;
  assert.equal((await POST(request('checkout.session.completed'))).status, 503);
  process.env.STRIPE_WEBHOOK_SECRET = 'whsec_placeholder';
  assert.equal((await POST(request('checkout.session.completed'))).status, 503);
  process.env.STRIPE_WEBHOOK_SECRET = 'whsec_mock_test_only';
  assert.equal((await POST(request('checkout.session.completed', null))).status, 400);
  assert.equal((await POST(request('checkout.session.completed', 'bad'))).status, 400);
  for (const type of ['checkout.session.completed', 'checkout.session.async_payment_succeeded']) {
    const response = await POST(request(type));
    assert.equal(response.status, 503);
    assert.equal(response.body.code, 'FULFILMENT_ON_HOLD');
    assert.equal(response.body.received, undefined);
  }
  const unrelated = await POST(request('customer.created'));
  assert.equal(unrelated.status, 200);
  assert.equal(unrelated.body.received, true);
  process.env.NODE_ENV = 'development';
  process.env.STRIPE_WEBHOOK_SECRET = 'whsec_placeholder';
  assert.equal((await POST(request('checkout.session.completed'))).status, 503);
  assert.equal(lineItemCalls, 0);
  assert.equal(supplierCalls, 0);
  assert.equal(verifiedEvents, 3);
  assert.ok(!JSON.stringify(logs).includes('private-customer@example.invalid'));
  console.log('PASS: 8 webhook cases; held signed sync/async checkouts503, missing production secret503, missing/bad signatures400, unrelated event200, local mock remainsheld. Zero supplier/Stripe retrieval/network calls; customer PII absent from logs.');
})().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => {
  for (const [key, value] of Object.entries(originalEnv)) {
    if (value === undefined) delete process.env[key]; else process.env[key] = value;
  }
});
