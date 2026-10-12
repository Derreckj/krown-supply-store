// Reversible incident guard: new website orders wait for verified production and fulfilment.
// This literal cannot be bypassed by an environment variable or checkout request.
export const WEBSITE_ORDERING_PAUSED = true;

// These offers remain visible for review, but cannot be ordered until fulfilment is verified.
// Keep product and external listing IDs intact so they can be resumed without duplicates.
const PURCHASE_HOLDS: Record<string, string> = {
  'custom-krown-works-hat': 'Ordering paused while the leather-patch supplier is confirmed.',
  'axiom-r112-patch-01': 'Ordering paused while the leather-patch supplier is confirmed.',
  '6ac80dc2f4d488e1be0b0902': 'Ordering paused while the leather-patch supplier is confirmed.',
  '6ac8f2e9b0b07f13520b055c': 'Ordering paused while the leather-patch supplier is confirmed.',
  'kc-stickers-01': 'Ordering paused until the five-design sticker bundle is ready.',
  '6ac7ed44fea4d4e68e0a0f80': 'Ordering paused until the five-design sticker bundle is ready.',
  '6ac700d0e586b62fb50465ad': 'Ordering paused until the five-design sticker bundle is ready.',
};

export function getCatalogPurchaseHold(productId: string): string | null {
  const specificHold = PURCHASE_HOLDS[productId.toLowerCase()];
  if (specificHold) return specificHold;
  return WEBSITE_ORDERING_PAUSED
    ? 'Ordering is temporarily paused while we verify production details. Please check back soon.'
    : null;
}
