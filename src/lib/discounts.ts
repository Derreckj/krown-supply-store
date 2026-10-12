// Canonical discount rules are shared with legacy config consumers.
export {
  HARD_EXCLUDED_PRODUCT_IDS,
  ALLOWED_DISCOUNT_CATEGORIES,
  VALID_DISCOUNT_CODES,
  validateDiscountCode,
  isCustomHatItem,
  isExcludedDiscountItem,
  getDiscountedUnitAmount,
  calculateKrown10Discount,
  calculateCartDiscount,
} from '@/config/discounts';
export type { CartLineItem, DiscountCodeConfig, CartDiscountBreakdown } from '@/config/discounts';
