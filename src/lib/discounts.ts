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
