/**
 * KrowN Supply Co. - Product Economics Engine
 * Calculates true product margins, transaction fees, fulfillment costs,
 * and recommends profitable retail pricing before promotions or ad spend.
 */

export interface ProductCostInputs {
  baseCost: number; // Blank garment or raw item cost from Printify
  printCost: number; // Print provider decoration / DTG / embroidery charge
  retailPrice: number; // Listed retail price
  shippingChargedToCustomer?: number; // What customer pays for shipping (0 if free shipping)
  estimatedShippingCost?: number; // Real Printify shipping fee (average ~$5.50 for shirts/hats)
  platformFeeRate?: number; // Processing fee rate (Stripe default: 2.9% = 0.029)
  platformFixedFee?: number; // Processing fixed fee (Stripe default: $0.30)
  estimatedAdCostPerSale?: number; // Target CAC allocation per order
  discountPercent?: number; // Optional promotional discount (e.g. 15 for 15% off)
}

export interface ProductEconomicsResult {
  retailPrice: number;
  discountAmount: number;
  effectiveRetailPrice: number;
  totalPrintifyCost: number;
  estimatedShippingCost: number;
  shippingChargedToCustomer: number;
  shippingDelta: number; // Profit or loss on shipping fee
  paymentProcessingFee: number;
  adCostAllocation: number;
  totalExpenses: number;
  grossRevenue: number;
  netProfit: number;
  marginPercentage: number;
  isProfitable: boolean;
  healthStatus: 'STRONG' | 'ACCEPTABLE' | 'SLIM' | 'LOSS';
  recommendedActions: string[];
}

export const DEFAULT_SHIPPING_ESTIMATE = 5.50;
export const STRIPE_PERCENTAGE_FEE = 0.029;
export const STRIPE_FIXED_FEE = 0.30;

/**
 * Calculates complete unit economics for a product variant.
 */
export function calculateProductEconomics(inputs: ProductCostInputs): ProductEconomicsResult {
  const {
    baseCost,
    printCost,
    retailPrice,
    shippingChargedToCustomer = 0,
    estimatedShippingCost = DEFAULT_SHIPPING_ESTIMATE,
    platformFeeRate = STRIPE_PERCENTAGE_FEE,
    platformFixedFee = STRIPE_FIXED_FEE,
    estimatedAdCostPerSale = 0,
    discountPercent = 0,
  } = inputs;

  const discountAmount = (retailPrice * (Math.max(0, Math.min(100, discountPercent)))) / 100;
  const effectiveRetailPrice = Math.max(0, retailPrice - discountAmount);
  const grossRevenue = effectiveRetailPrice + shippingChargedToCustomer;

  // Processing fee based on gross payment collected (price + shipping)
  const paymentProcessingFee = grossRevenue > 0
    ? (grossRevenue * platformFeeRate) + platformFixedFee
    : 0;

  const totalPrintifyCost = baseCost + printCost;
  const shippingDelta = shippingChargedToCustomer - estimatedShippingCost;

  const totalExpenses = totalPrintifyCost + estimatedShippingCost + paymentProcessingFee + estimatedAdCostPerSale;
  const netProfit = grossRevenue - totalExpenses;
  const marginPercentage = grossRevenue > 0 ? (netProfit / grossRevenue) * 100 : 0;

  let healthStatus: ProductEconomicsResult['healthStatus'] = 'LOSS';
  const recommendedActions: string[] = [];

  if (netProfit <= 0) {
    healthStatus = 'LOSS';
    recommendedActions.push('CRITICAL: Item operates at a loss. Increase retail price or switch print providers.');
  } else if (marginPercentage < 20) {
    healthStatus = 'SLIM';
    recommendedActions.push('WARNING: Margin under 20% leaves little buffer for refunds, returns, or paid ads.');
  } else if (marginPercentage < 35) {
    healthStatus = 'ACCEPTABLE';
    recommendedActions.push('Healthy direct-to-consumer baseline. Monitor ad costs carefully.');
  } else {
    healthStatus = 'STRONG';
    recommendedActions.push('Excellent margin. Suitable for paid acquisition and promotional sales.');
  }

  return {
    retailPrice,
    discountAmount: Number(discountAmount.toFixed(2)),
    effectiveRetailPrice: Number(effectiveRetailPrice.toFixed(2)),
    totalPrintifyCost: Number(totalPrintifyCost.toFixed(2)),
    estimatedShippingCost: Number(estimatedShippingCost.toFixed(2)),
    shippingChargedToCustomer: Number(shippingChargedToCustomer.toFixed(2)),
    shippingDelta: Number(shippingDelta.toFixed(2)),
    paymentProcessingFee: Number(paymentProcessingFee.toFixed(2)),
    adCostAllocation: Number(estimatedAdCostPerSale.toFixed(2)),
    totalExpenses: Number(totalExpenses.toFixed(2)),
    grossRevenue: Number(grossRevenue.toFixed(2)),
    netProfit: Number(netProfit.toFixed(2)),
    marginPercentage: Number(marginPercentage.toFixed(1)),
    isProfitable: netProfit > 0,
    healthStatus,
    recommendedActions,
  };
}

/**
 * Calculates recommended retail price based on printify production costs and a target margin percentage.
 * Target margin default: 40% (healthy premium apparel/workwear benchmark).
 */
export function calculateRecommendedRetailPrice(
  baseCost: number,
  printCost: number,
  targetMarginPercent: number = 40,
  estimatedShippingCost: number = DEFAULT_SHIPPING_ESTIMATE,
  chargeShippingToCustomer: boolean = false
): number {
  const totalCost = baseCost + printCost;
  const effectiveShipping = chargeShippingToCustomer ? 0 : estimatedShippingCost;
  const targetMarginDecimal = targetMarginPercent / 100;

  // Revenue = (Costs + FixedFee) / (1 - TargetMargin - PercentageFee)
  const denominator = 1 - targetMarginDecimal - STRIPE_PERCENTAGE_FEE;
  if (denominator <= 0) {
    return Number((totalCost * 2.5).toFixed(2));
  }

  const rawRecommended = (totalCost + effectiveShipping + STRIPE_FIXED_FEE) / denominator;
  
  // Clean to psychological price point (.99 or .00)
  const rounded = Math.ceil(rawRecommended);
  return Number((rounded - 0.01).toFixed(2));
}
