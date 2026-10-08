import { NextResponse } from 'next/server';
import { getEnvironmentReport } from '@/lib/env';
import { printifyService } from '@/services/printify';

export const dynamic = 'force-dynamic';

export async function GET() {
  const envReport = getEnvironmentReport(true);
  
  let catalogCount = 0;
  let catalogStatus: 'online' | 'degraded' = 'online';

  try {
    const products = await printifyService.getProducts();
    catalogCount = products.length;
  } catch (err) {
    console.error('Health check catalog error:', err);
    catalogStatus = 'degraded';
  }

  const isHealthy = envReport.isValid && catalogStatus === 'online';

  const healthData = {
    status: isHealthy ? 'healthy' : 'degraded',
    brand: 'KrowN Supply Co.',
    version: '1.0.0',
    nextVersion: '16.4.0',
    timestamp: new Date().toISOString(),
    uptimeSeconds: Math.floor(process.uptime()),
    environment: process.env.NODE_ENV || 'development',
    fulfillmentMode: envReport.fulfillmentMode,
    services: {
      stripe: {
        status: envReport.summary.stripeStatus,
        isLive: envReport.config.isStripeLive,
      },
      printify: {
        status: envReport.summary.printifyStatus,
        isLive: envReport.config.isPrintifyLive,
        shopIdConfigured: Boolean(envReport.config.PRINTIFY_SHOP_ID),
      },
      catalog: {
        status: catalogStatus,
        totalProducts: catalogCount,
      },
    },
    diagnostics: {
      isProductionReady: envReport.isProductionReady,
      errors: envReport.errors,
      warnings: envReport.warnings,
    },
  };

  return NextResponse.json(healthData, {
    status: isHealthy ? 200 : 503,
    headers: {
      'Cache-Control': 'no-store, no-cache, must-revalidate',
    },
  });
}
