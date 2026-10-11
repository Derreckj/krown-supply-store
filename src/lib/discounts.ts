export interface DiscountCodeConfig {
  code: string;
  percentage: number;
  label: string;
  description: string;
}

export const VALID_DISCOUNT_CODES: Record<string, DiscountCodeConfig> = {
  // 10% Off Friends & Family Codes
  'KROWN10': {
    code: 'KROWN10',
    percentage: 10,
    label: '10% Friends & Family Discount',
    description: '10% off entire order for KrowN friends & family',
  },
  'FAMILY10': {
    code: 'FAMILY10',
    percentage: 10,
    label: '10% Friends & Family Discount',
    description: '10% off entire order for KrowN friends & family',
  },
  'FRIENDS10': {
    code: 'FRIENDS10',
    percentage: 10,
    label: '10% Friends & Family Discount',
    description: '10% off entire order for KrowN friends & family',
  },

  // 15% Off Friends & Family Codes
  'KROWN15': {
    code: 'KROWN15',
    percentage: 15,
    label: '15% Friends & Family VIP Discount',
    description: '15% off entire order for KrowN inner circle and VIP family',
  },
  'FAMILY15': {
    code: 'FAMILY15',
    percentage: 15,
    label: '15% Friends & Family VIP Discount',
    description: '15% off entire order for KrowN inner circle and VIP family',
  },
  'VIP15': {
    code: 'VIP15',
    percentage: 15,
    label: '15% Friends & Family VIP Discount',
    description: '15% off entire order for KrowN inner circle and VIP family',
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
export function isCustomHatItem(item: { productId?: string; name?: string; variant?: { color?: string; size?: string } } | null | undefined): boolean {
  if (!item) return false;
  const pid = (item.productId || '').toLowerCase();
  const name = (item.name || '').toLowerCase();
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

export interface CartDiscountBreakdown {
  cartTotal: number;
  discountableSubtotal: number;
  customHatSubtotal: number;
  discountAmount: number;
  finalTotal: number;
  hasCustomHats: boolean;
  hasEligibleItems: boolean;
}

/**
 * Computes exact breakdown of cart total, discountable portion, and promotional discount.
 * Custom hats are strictly excluded from promotional discounts (such as Krown10 and Krown15).
 */
export function calculateCartDiscount(
  items: Array<{ productId?: string; name?: string; price: number; quantity: number; variant?: { color?: string; size?: string } }>,
  discountConfig: DiscountCodeConfig | null | undefined
): CartDiscountBreakdown {
  let discountableSubtotal = 0;
  let customHatSubtotal = 0;
  let hasCustomHats = false;

  for (const item of items) {
    const lineTotal = item.price * item.quantity;
    if (isCustomHatItem(item)) {
      hasCustomHats = true;
      customHatSubtotal += lineTotal;
    } else {
      discountableSubtotal += lineTotal;
    }
  }

  const cartTotal = discountableSubtotal + customHatSubtotal;
  const hasEligibleItems = discountableSubtotal > 0;

  let discountAmount = 0;
  if (discountConfig && discountConfig.percentage > 0 && discountableSubtotal > 0) {
    discountAmount = (discountableSubtotal * discountConfig.percentage) / 100;
  }

  const finalTotal = Math.max(0, cartTotal - discountAmount);

  return {
    cartTotal,
    discountableSubtotal,
    customHatSubtotal,
    discountAmount,
    finalTotal,
    hasCustomHats,
    hasEligibleItems,
  };
}
