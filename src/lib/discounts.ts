import { 
  HARD_EXCLUDED_PRODUCT_IDS, 
  ALLOWED_DISCOUNT_CATEGORIES, 
  calculateKrown10Discount, 
  CartLineItem 
} from '@/config/discounts';

export { HARD_EXCLUDED_PRODUCT_IDS, ALLOWED_DISCOUNT_CATEGORIES, calculateKrown10Discount };
export type { CartLineItem };

export interface DiscountCodeConfig {
  code: string;
  percentage: number;
  label: string;
  description: string;
}

// Single active discount code across storefront
export const VALID_DISCOUNT_CODES: Record<string, DiscountCodeConfig> = {
  'KROWN10': {
    code: 'KROWN10',
    percentage: 10,
    label: '10% Storewide Discount',
    description: '10% off eligible items',
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
 * Checks if an item is strictly excluded from KROWN10 (e.g. axiom-hoodie-01 luxury 3-location DTG outerwear).
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

/**
 * Computes exact breakdown of cart total, discountable portion, and promotional discount.
 * Enforces KROWN10 single code with hard hoodie exclusion and custom hat exclusion.
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

  for (const item of items) {
    const lineTotal = item.price * item.quantity;
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
    }
  }

  const cartTotal = discountableSubtotal + excludedSubtotal + customHatSubtotal;
  const hasEligibleItems = discountableSubtotal > 0;

  let discountAmount = 0;
  let errorMessage: string | null = null;

  if (discountConfig) {
    if (discountConfig.code === 'KROWN10') {
      if (discountableSubtotal > 0) {
        discountAmount = Math.round(discountableSubtotal * 0.10 * 100) / 100;
      } else if (hasExcludedHoodie) {
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
