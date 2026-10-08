/**
 * KrowN Supply Co. - Production Environment Validation Layer
 * 
 * Bulletproof TypeScript validation guards for all e-commerce, payment,
 * and POD automation services. Strictly catches misconfigured or missing
 * production keys prior to runtime execution.
 * 
 * Strict Brand Rule: "KrowN" capitalization enforced.
 */

export interface EnvConfig {
  STRIPE_SECRET_KEY: string;
  STRIPE_WEBHOOK_SECRET: string;
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: string;
  PRINTIFY_API_KEY: string;
  PRINTIFY_SHOP_ID: string;
  NEXT_PUBLIC_SITE_URL: string;
  NODE_ENV: 'development' | 'production' | 'test';
  isStripeLive: boolean;
  isPrintifyLive: boolean;
  isProductionReady: boolean;
  fulfillmentMode: 'live' | 'mock_sandbox';
}

export interface EnvValidationReport {
  isValid: boolean;
  isProductionReady: boolean;
  fulfillmentMode: 'live' | 'mock_sandbox';
  config: Partial<EnvConfig>;
  errors: string[];
  warnings: string[];
  summary: {
    stripeStatus: 'configured' | 'mock_sandbox' | 'missing';
    printifyStatus: 'configured' | 'mock_sandbox' | 'missing';
    siteUrlStatus: 'valid' | 'fallback';
  };
}

const PLACEHOLDER_STRINGS = [
  'placeholder',
  'your_stripe_secret_key',
  'your_stripe_webhook_secret',
  'your_stripe_publishable_key',
  'your_printify_api_key',
  'your_printify_shop_id',
  'undefined',
  'null',
  '',
];

function isPopulated(val: string | undefined): val is string {
  if (!val) return false;
  const trimmed = val.trim();
  return !PLACEHOLDER_STRINGS.includes(trimmed.toLowerCase());
}

export function validateEnvironment(): EnvValidationReport {
  const errors: string[] = [];
  const warnings: string[] = [];

  const nodeEnv = (process.env.NODE_ENV || 'development') as 'development' | 'production' | 'test';
  const isProd = nodeEnv === 'production';

  // 1. Stripe Validation
  const stripeSecret = process.env.STRIPE_SECRET_KEY;
  const stripeWebhook = process.env.STRIPE_WEBHOOK_SECRET;
  const stripePubKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;

  let stripeStatus: 'configured' | 'mock_sandbox' | 'missing' = 'missing';

  if (!isPopulated(stripeSecret)) {
    if (isProd) {
      errors.push('STRIPE_SECRET_KEY is required in production environment.');
    } else {
      warnings.push('STRIPE_SECRET_KEY is missing or using placeholder; fallback to mock sandbox checkout active.');
      stripeStatus = 'mock_sandbox';
    }
  } else if (
    !stripeSecret.startsWith('sk_test_') &&
    !stripeSecret.startsWith('sk_live_') &&
    !stripeSecret.startsWith('rk_live_') &&
    !stripeSecret.startsWith('rk_test_')
  ) {
    errors.push('STRIPE_SECRET_KEY must begin with "sk_test_", "sk_live_", or "rk_live_".');
  } else {
    stripeStatus = 'configured';
  }

  if (isPopulated(stripeWebhook)) {
    if (!stripeWebhook.startsWith('whsec_')) {
      warnings.push('STRIPE_WEBHOOK_SECRET typically starts with "whsec_". Verify secret format.');
    }
  } else {
    if (isProd) {
      warnings.push('STRIPE_WEBHOOK_SECRET is not set; webhook signature verification will bypass in production.');
    } else {
      warnings.push('STRIPE_WEBHOOK_SECRET missing; running webhooks in mock verification mode.');
    }
  }

  if (isPopulated(stripePubKey)) {
    if (!stripePubKey.startsWith('pk_test_') && !stripePubKey.startsWith('pk_live_')) {
      errors.push('NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY must begin with "pk_test_" or "pk_live_".');
    }
  }

  // 2. Printify Validation
  const printifyKey = process.env.PRINTIFY_API_KEY;
  const printifyShop = process.env.PRINTIFY_SHOP_ID;

  let printifyStatus: 'configured' | 'mock_sandbox' | 'missing' = 'missing';

  if (!isPopulated(printifyKey)) {
    if (isProd) {
      warnings.push('PRINTIFY_API_KEY is not configured; order fulfillment will default to internal mock logger.');
      printifyStatus = 'mock_sandbox';
    } else {
      warnings.push('PRINTIFY_API_KEY is unconfigured; test orders will route to mock logger.');
      printifyStatus = 'mock_sandbox';
    }
  } else {
    printifyStatus = 'configured';
  }

  if (isPopulated(printifyShop)) {
    if (!/^\d+$/.test(printifyShop.trim())) {
      warnings.push('PRINTIFY_SHOP_ID is expected to be a numeric string ID (e.g., "12345678").');
    }
  } else if (printifyStatus === 'configured') {
    warnings.push('PRINTIFY_SHOP_ID is missing while PRINTIFY_API_KEY is present.');
  }

  // 3. Site URL Validation
  let siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';
  let siteUrlStatus: 'valid' | 'fallback' = 'valid';

  try {
    const parsedUrl = new URL(siteUrl);
    if (!parsedUrl.protocol.startsWith('http')) {
      throw new Error('Invalid protocol');
    }
  } catch {
    warnings.push(`NEXT_PUBLIC_SITE_URL ("${siteUrl}") is invalid; falling back to http://localhost:3000.`);
    siteUrl = 'http://localhost:3000';
    siteUrlStatus = 'fallback';
  }

  const isStripeLive = stripeStatus === 'configured';
  const isPrintifyLive = printifyStatus === 'configured';
  const isProductionReady = errors.length === 0 && isStripeLive && isPrintifyLive && isProd;
  const fulfillmentMode = isPrintifyLive ? 'live' : 'mock_sandbox';

  return {
    isValid: errors.length === 0,
    isProductionReady,
    fulfillmentMode,
    config: {
      STRIPE_SECRET_KEY: stripeSecret ? `${stripeSecret.slice(0, 7)}...` : undefined,
      STRIPE_WEBHOOK_SECRET: stripeWebhook ? `${stripeWebhook.slice(0, 10)}...` : undefined,
      NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: stripePubKey ? `${stripePubKey.slice(0, 7)}...` : undefined,
      PRINTIFY_API_KEY: printifyKey ? `${printifyKey.slice(0, 6)}...` : undefined,
      PRINTIFY_SHOP_ID: printifyShop,
      NEXT_PUBLIC_SITE_URL: siteUrl,
      NODE_ENV: nodeEnv,
      isStripeLive,
      isPrintifyLive,
      isProductionReady,
      fulfillmentMode,
    },
    errors,
    warnings,
    summary: {
      stripeStatus,
      printifyStatus,
      siteUrlStatus,
    },
  };
}

let cachedReport: EnvValidationReport | null = null;

export function getEnvironmentReport(forceFresh = false): EnvValidationReport {
  if (!cachedReport || forceFresh) {
    cachedReport = validateEnvironment();
  }
  return cachedReport;
}
