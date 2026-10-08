# KrowN Supply Co. — Production Live Launch Runbook (v1.0.0)

> **Document Classification**: Mission-Critical Operations Runbook  
> **Brand Nomenclature Rule**: Exact capitalization **"KrowN"** strictly enforced across all platforms, payloads, and communications.  
> **Brand Separation**:
> - **KrowN Supply Co.** (`/collections/supply`) — Slogan: *"WEAR THE KROWN."* (Luxury Streetwear)
> - **KrowN Construction LLC** (`/collections/construction`) — Slogan: *"BUILT TO REIGN."* (Tradesman Jobsite Gear)
> - **AXA / Axiom Allegiance** (`/collections/gaming`) — Slogan: *"PLAY TO REIGN."* (Official Esports & Pro Gaming)

---

## 1. Production Deployment on Vercel

### Step 1.1: Project Import & Root Settings
1. Log in to [Vercel](https://vercel.com) using the organization account.
2. Click **"Add New..."** > **"Project"** and import the GitHub repository: `krown-supply-store`.
3. Framework Preset: **Next.js**
4. Root Directory: `./` (or project root)
5. Build Command: `next build`
6. Output Directory: `.next`

### Step 1.2: Environment Variable Configuration
Configure the following environment variables in **Project Settings > Environment Variables** (set for **Production** and **Preview**):

| Variable Name | Example Value | Description |
| :--- | :--- | :--- |
| `STRIPE_SECRET_KEY` | `sk_live_...` | Stripe Production Secret Key |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_live_...` | Stripe Production Publishable Key |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | Stripe Webhook Signing Secret |
| `PRINTIFY_API_KEY` | `eyJ...` | Printify Production Access Token |
| `PRINTIFY_SHOP_ID` | `29241235` | Printify Numeric Shop ID |
| `NEXT_PUBLIC_SITE_URL` | `https://krownsupply.com` | Production Canonical Storefront URL |
| `NODE_ENV` | `production` | Node Runtime Environment |

---

## 2. Stripe Live Mode Activation Runbook

### Step 2.1: Retrieve Live API Keys
1. Access the [Stripe Dashboard](https://dashboard.stripe.com).
2. Ensure the top toggle is switched **OFF** from Test Mode to **Live Mode**.
3. Navigate to **Developers > API keys**:
   - Copy **Secret key** (`sk_live_...`).
   - Copy **Publishable key** (`pk_live_...`).
4. Update Vercel environment variables immediately.

### Step 2.2: Register Stripe Production Webhook
1. In the Stripe Dashboard, go to **Developers > Webhooks**.
2. Click **"Add an endpoint"**.
3. **Endpoint URL**: `https://krownsupply.com/api/webhooks/stripe`
4. **Description**: `KrowN Supply Co. Production Order Fulfillment Dispatcher`
5. **Events to Send**:
   - `checkout.session.completed` *(triggers Printify order dispatch)*
   - `payment_intent.payment_failed` *(triggers failure alert)*
6. Click **"Add endpoint"**.
7. Under the new endpoint details, click **"Reveal"** under **Signing secret** (`whsec_...`).
8. Add this value to Vercel as `STRIPE_WEBHOOK_SECRET`.

---

## 3. Printify Live Production Activation Runbook

### Step 3.1: Verify Printify Merchant Funding
Printify charges base production and shipping costs at the moment orders are sent to production:
1. Log in to [Printify](https://printify.com).
2. Go to **Wallet / Billing**:
   - Link a primary business credit card or ACH debit.
   - Set up auto-reload (recommended: $200 threshold with $500 reload) to avoid order holds during sales volume surges.

### Step 3.2: Configure Order Approval Window
1. In Printify, navigate to **Settings > Order Settings > Order Approval**:
   - **First 48 Hours Post-Launch**: Select **"Manual"**.
     *Rationale*: Permits visual verification of customer Gamertags and Richardson 112 leather patch proofs before committing printing resources.
   - **Post 48-Hour Scale Phase**: Select **"Automatically after 1 hour"**.
     *Rationale*: Zero-touch fulfillment with a built-in 60-minute window for customer address edits or cancelations.

### Step 3.3: Verify Print Provider Routing
Confirm primary print providers under **My Products**:
- **AXA Pro League Custom Jersey**: Blueprint `872` → Cut-and-Sew Sublimation Specialist (Provider 16).
- **KrowN 480 GSM French Terry Hoodie**: Blueprint `1035` → Monster Digital / SwiftPOD (Provider 29).
- **Richardson 112 Trucker Hat**: Blueprint `112` → Headwear & Leatherette Specialist (Provider 42).
- **Axiom Pro Loadout Shaker Bottle**: Blueprint `540` → Drinkware Specialist (Provider 10).

---

## 4. Etsy Direct CSV Bulk Import & Personalization Setup

### Step 4.1: Import Catalog CSV
1. In the project directory, verify that the bulk CSV is generated:
   - File path: [`docs/etsy-bulk-catalog.csv`](file:///C:/Users/derre/.gemini/antigravity-ide/scratch/krown-supply-store/docs/etsy-bulk-catalog.csv)
2. Log into the **Etsy Shop Manager** (`https://www.etsy.com/your/shops/me/dashboard`).
3. Navigate to **Listings > Add a listing** (or use Etsy CSV bulk upload tool if enabled on your tier).
4. Verify standard fields populated from our generator:
   - **Titles**: SEO-optimized and under 140 characters.
   - **Tags**: 13 unique tags per product, all under 20 characters.
   - **Materials**: 100% French Terry cotton, Bird-Eye micro-poly, Eastar Tritan polymer.
   - **Shop Sections**: Segmented into *KrowN Supply Co.*, *KrowN Construction*, and *AXA Pro Esports*.

### Step 4.2: Configure Item Personalization
For the **AXA Pro League Custom Esports Jersey**:
1. Open the listing editor in Etsy.
2. Scroll to the **Personalization** section and toggle **ON**.
3. Set **Buyer Instructions**:
   > *"Enter your custom Gamertag (max 16 characters) and Squad Number (0–99). All text is rendered in official team capital typography."*
4. Check **Personalization is required**.

### Step 4.3: Connect Printify to Etsy
1. In Printify, go to the store selector > **"Add a new store"** > **"Etsy"**.
2. Click **"Connect to Etsy"** and accept OAuth permissions.
3. Order details and custom buyer personalization notes will now automatically ingest into the Printify dashboard every 15 minutes.

---

## 5. Post-Launch Verification & Health Diagnostics

### Step 5.1: Health Check Endpoint
Query the live production health endpoint:
```bash
curl -s https://krownsupply.com/api/health | jq
```
Expected output:
```json
{
  "status": "healthy",
  "brand": "KrowN Supply Co.",
  "version": "1.0.0",
  "nextVersion": "16.4.0",
  "fulfillmentMode": "live",
  "services": {
    "stripe": { "status": "configured", "isLive": true },
    "printify": { "status": "configured", "isLive": true, "shopIdConfigured": true },
    "catalog": { "status": "online", "totalProducts": 34 }
  }
}
```

### Step 5.2: Live Dry-Run Simulation Check
Run the CLI validation test to verify local pipeline health:
```bash
npx tsx scripts/simulate-checkout-e2e.ts
```

---

## 6. Incident Response & Rollback Procedures

- **Stripe Webhook Failure**: If events return 400/500, verify `STRIPE_WEBHOOK_SECRET` matches the active endpoint secret in Stripe Dashboard. The fallback logger ensures no customer payments are lost.
- **Printify API Outage / Rate Limit**: The order pipeline gracefully catches API timeouts, records a mock fulfillment ID (`krown_mock_pfy_*`), and alerts store administrators without terminating the customer checkout session.
- **Deployment Rollback**: In Vercel, navigate to **Deployments**, select the previous green build, and click **"Rollback"** for instant 0-second downtime recovery.
