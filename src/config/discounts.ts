export const HARD_EXCLUDED_PRODUCT_IDS = ['axiom-hoodie-01'];

export const ALLOWED_DISCOUNT_CATEGORIES = [
  'sweatshirt',
  'crewneck',
  'hat',
  'trucker',
  'headwear',
  'snapback',
  'cap',
  'shaker',
  'bottle',
  'drinkware',
  'mug',
  'tee',
  't-shirt',
  'shirt',
  'apparel',
  'esports apparel',
  'desk accessories',
  'mousepad',
  'mat'
];

export interface CartLineItem {
  id: string;
  title: string;
  category?: string;
  price: number;
  quantity: number;
}

export function calculateKrown10Discount(code: string, items: CartLineItem[]) {
  const normalized = (code || '').trim().toUpperCase();
  if (normalized !== 'KROWN10') {
    return { isValid: false, discountAmount: 0, error: 'Invalid discount code.' };
  }

  let eligibleSubtotal = 0;
  let hasExcludedHoodie = false;

  for (const item of items) {
    const isExcluded = HARD_EXCLUDED_PRODUCT_IDS.includes(item.id);
    if (isExcluded) {
      hasExcludedHoodie = true;
      continue;
    }

    const categoryMatch = ALLOWED_DISCOUNT_CATEGORIES.some(cat =>
      (item.category || '').toLowerCase().includes(cat) ||
      (item.title || '').toLowerCase().includes(cat)
    );

    if (categoryMatch) {
      eligibleSubtotal += item.price * item.quantity;
    }
  }

  if (eligibleSubtotal === 0) {
    return {
      isValid: false,
      discountAmount: 0,
      error: hasExcludedHoodie 
        ? 'Discount cannot be applied to luxury 3-location DTG outerwear (Hoodie excluded).' 
        : 'No eligible items found in cart for this discount.'
    };
  }

  const discountAmount = Math.round(eligibleSubtotal * 0.10 * 100) / 100;
  return { isValid: true, discountAmount, error: null };
}
