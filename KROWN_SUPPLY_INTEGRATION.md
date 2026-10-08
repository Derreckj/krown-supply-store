# KrowN Supply Co. — Integration Guide & Architecture Record
**Ecosystem Division:** Ecommerce / Apparel / Merch / Workwear / Gaming / Lifestyle  
**Maintainer:** Antigravity IDE & Gemini  
**Workspace:** Isolated in `krown-supply-store/`

---

## 1. Ecosystem Overview & Boundary Guarantee
- **Construction Team Workspace:** Live WordPress site at `krownconstructionllc.com`, WordPress files, local backups, and SEO assets are completely isolated and untouched.
- **Supply Co. Storefront:** Built in Next.js (TypeScript, App Router, Vanilla CSS design system). Fully standalone and modular.
- **Future Integration Points:** Supports three deployment strategies without code refactoring:
  1. Standalone domain (e.g., `https://krownsupply.com` or `https://krownsupplyco.com`)
  2. Subdomain integration (e.g., `https://shop.krownconstructionllc.com`)
  3. Header/navigation deep linking directly from the WordPress construction site.

---

## 2. Store Routing & Endpoints
| Route | Purpose | Audience |
| :--- | :--- | :--- |
| `/` | Flagship storefront homepage | All |
| `/collections/all` | Master catalog browser | All |
| `/collections/core` | Core KrowN flagship pieces (Signature hats, hoodies) | Lifestyle / Brand |
| `/collections/gaming` | Creator & gaming crossover apparel | Gaming / Creator |
| `/collections/workwear` | Jobsite-tested shirts, high-mobility workwear | Trades & Construction |
| `/collections/reign` | Streetwear & lifestyle line | Streetwear |
| `/collections/limited` | Limited drops & timed releases | Collectors / Followers |
| `/collections/accessories`| Stickers, hardhat decals, accessories | All |
| `/products/[id]` | High-conversion Product Detail Page (PDP) | Shoppers |
| `/cart` | Dynamic cart with instant quantity controls | Shoppers |
| `/checkout/success` | Order confirmation & Printify fulfillment status | Customers |
| `/checkout/cancel` | Safe cancel return preserving cart state | Customers |

---

## 3. Stripe & Printify Integration

### A. Environment Configuration
Duplicate `.env.example` to `.env.local` with real production or sandbox values:
```bash
STRIPE_SECRET_KEY=sk_live_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
PRINTIFY_API_KEY=pr_...
PRINTIFY_SHOP_ID=12345678
NEXT_PUBLIC_SITE_URL=https://shop.krownconstructionllc.com
```

### B. Fallback Sandbox Behavior
- When `STRIPE_SECRET_KEY` is not present or contains `placeholder`, the store runs in **Safe Mock Checkout Mode**. Customers/testers are seamlessly routed to `/checkout/success?mode=mock_sandbox` with simulated order references.
- When `PRINTIFY_API_KEY` is not present, the store automatically serves the **Curated Launch Mock Catalog** with real economics, variants, and out-of-stock simulation. Adding live keys requires **zero UI or component changes**.

### C. Webhook Architecture
- **Stripe Webhook URL:** `https://your-domain.com/api/webhooks/stripe`
- **Supported Event:** `checkout.session.completed`
- Validates cryptographic signature using `STRIPE_WEBHOOK_SECRET` and triggers fulfillment dispatch.

---

## 4. Product Economics Engine
Located at: `src/lib/economics.ts`
Calculates true profit for physical goods:
$$\text{Net Profit} = \text{Gross Revenue} - (\text{Printify Base Cost} + \text{Print Cost} + \text{Actual Shipping} + \text{Stripe 2.9\% + \$0.30 Fee} + \text{Target CAC})$$
Provides automated warnings for any variant generating less than a 20% margin.

---

## 5. Construction Site Cross-Promotion Links (For WordPress Team)
When linking from the main KrowN Construction website navigation bar, footer, or portfolio pages, use the following clean URLs:

- **Store Header Link:**
  `https://[STORE_DOMAIN]/collections/workwear` (Label: *Shop Workwear & Gear*)
- **General Merchandise Link:**
  `https://[STORE_DOMAIN]` (Label: *KrowN Supply Co.*)
- **Hardhat Decals / Stickers Link:**
  `https://[STORE_DOMAIN]/collections/accessories` (Label: *KrowN Stickers & Decals*)
