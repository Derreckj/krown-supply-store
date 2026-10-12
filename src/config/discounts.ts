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

export interface DiscountCodeConfig {
  code: string;
  percentage: number;
  label: string;
  description: string;
}

// Codes share the same exclusions across the storefront and checkout.
export const VALID_DISCOUNT_CODES: Record<string, DiscountCodeConfig> = {
  'KROWN10': {
    code: 'KROWN10',
    percentage: 10,
    label: '10% Eligible Item Discount',
    description: '10% off eligible items',
  },
  'KROWN15': {
    code: 'KROWN15',
    percentage: 15,
    label: '15% Eligible Item Discount',
    description: '15% off eligible items',
  },
};

export function validateDiscountCode(rawCode: string | null | undefined): DiscountCodeConfig | null {
  if (!rawCode) return null;
  const clean = rawCode.trim().toUpperCase();
  return VALID_DISCOUNT_CODES[clean] || null;
}

/**
 * Checks whether an item represents a custom hat from the configurator or catalogue.
 * Evaluates product ID, title/name, and variant specifications against trusted custom hat identifiers.
 */
export function isCustomHatItem(item: { productId?: string; id?: string; name?: string; title?: string; variant?: { color?: string; size?: string } } | null | undefined): boolean {
  if (!item) return false;
  const pid = (item.productId || item.id || '').toLowerCase();
  const name = (item.name || item.title || '').toLowerCase();
  const color = (item.variant?.color || '').toLowerCase();
  const size = (item.variant?.size || '').toLowerCase();

  // Trusted catalogue ID check
  if (pid === 'custom-krown-works-hat' || pid.includes('custom-hat') || pid.includes('custom-richardson')) {
    return true;
  }

  // Name or title matching
  if (
    name.includes('custom richardson') ||
    name.includes('custom crew') ||
    name.includes('richardson 112 leather patch') ||
    (name.includes('richardson 112') && name.includes('custom'))
  ) {
    return true;
  }

  // Configurator variant check (e.g., "Placement", "Hats", leather patch finishes)
  if (size.includes('placement') || size.includes('pack') || color.includes('leather patch')) {
    if (name.includes('richardson') || pid.includes('hat') || name.includes('hat')) {
      return true;
    }
  }

  return false;
}

/**
 * Checks if an item is strictly excluded from promotions (e.g. axiom-hoodie-01 luxury 3-location DTG outerwear).
 */
export function isExcludedDiscountItem(item: { productId?: string; id?: string; name?: string; title?: string } | null | undefined): boolean {
  if (!item) return false;
  const pid = (item.productId || item.id || '').toLowerCase();
  const name = (item.name || item.title || '').toLowerCase();

  if (HARD_EXCLUDED_PRODUCT_IDS.some(id => pid === id.toLowerCase())) {
    return true;
  }
  if (name.includes('axiom allegiance statement hoodie') || name.includes('statement hoodie 01') || (name.includes('hoodie') && pid.includes('hoodie'))) {
    return true;
  }
  return false;
}

export interface CartDiscountBreakdown {
  cartTotal: number;
  discountableSubtotal: number;
  excludedSubtotal: number;
  customHatSubtotal: number;
  discountAmount: number;
  finalTotal: number;
  hasCustomHats: boolean;
  hasExcludedHoodie: boolean;
  hasEligibleItems: boolean;
  errorMessage?: string | null;
}

/** Match Stripe's per-unit cent rounding so the cart and checkout totals agree. */
export function getDiscountedUnitAmount(price: number, discount?: DiscountCodeConfig | null): number {
  return Math.round(price * (1 - (discount?.percentage || 0) / 100) * 100);
}

/** Legacy entry point uses the same code validation and exclusions as checkout. */
export function calculateKrown10Discount(code: string, items: CartLineItem[]) {
  const discount = validateDiscountCode(code);
  if (!discount) {
    return { isValid: false, discountAmount: 0, error: 'Invalid discount code.' };
  }
  const breakdown = calculateCartDiscount(items, discount);
  return {
    isValid: !breakdown.errorMessage,
    discountAmount: breakdown.discountAmount,
    error: breakdown.errorMessage || null,
  };
}

/**
 * Computes exact breakdown of cart total, discountable portion, and promotional discount.
 * Enforces all valid codes with the existing hoodie and custom hat exclusions.
 */
export function calculateCartDiscount(
  items: Array<{ productId?: string; id?: string; name?: string; title?: string; price: number; quantity: number; variant?: { color?: string; size?: string } }>,
  discountConfig: DiscountCodeConfig | null | undefined
): CartDiscountBreakdown {
  let discountableSubtotal = 0;
  let excludedSubtotal = 0;
  let customHatSubtotal = 0;
  let hasCustomHats = false;
  let hasExcludedHoodie = false;
  let discountAmount = 0;

  for (const item of items) {
    const unitAmount = getDiscountedUnitAmount(item.price);
    const lineTotal = unitAmount * item.quantity / 100;
    const isHat = isCustomHatItem(item);
    const isHoodie = isExcludedDiscountItem(item);

    if (isHat) {
      hasCustomHats = true;
      customHatSubtotal += lineTotal;
    } else if (isHoodie) {
      hasExcludedHoodie = true;
      excludedSubtotal += lineTotal;
    } else {
      discountableSubtotal += lineTotal;
      if (discountConfig) {
        discountAmount += (unitAmount - getDiscountedUnitAmount(item.price, discountConfig)) * item.quantity / 100;
      }
    }
  }

  const cartTotal = discountableSubtotal + excludedSubtotal + customHatSubtotal;
  const hasEligibleItems = discountableSubtotal > 0;

  discountAmount = Math.round(discountAmount * 100) / 100;
  let errorMessage: string | null = null;

  if (discountConfig) {
    if (discountableSubtotal === 0) {
      if (hasExcludedHoodie) {
        errorMessage = 'Discount cannot be applied to luxury 3-location DTG outerwear (Hoodie excluded).';
      } else {
        errorMessage = 'No eligible items found in cart for this discount.';
      }
    }
  }

  const finalTotal = Math.max(0, Math.round((cartTotal - discountAmount) * 100) / 100);

  return {
    cartTotal,
    discountableSubtotal,
    excludedSubtotal,
    customHatSubtotal,
    discountAmount,
    finalTotal,
    hasCustomHats,
    hasExcludedHoodie,
    hasEligibleItems,
    errorMessage,
  };
}
