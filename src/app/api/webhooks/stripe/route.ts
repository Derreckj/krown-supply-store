import { NextRequest, NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import Stripe from 'stripe';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = req.headers.get('stripe-signature');
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let event: Stripe.Event;

  // Verify signature if secret is present and not placeholder
  if (webhookSecret && !webhookSecret.includes('placeholder')) {
    if (!signature) {
      return NextResponse.json(
        { error: 'Missing stripe-signature header' },
        { status: 400 }
      );
    }

    try {
      event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Unknown error';
      console.error(`⚠️ Webhook signature verification failed: ${msg}`);
      return NextResponse.json(
        { error: `Webhook Error: ${msg}` },
        { status: 400 }
      );
    }
  } else {
    // In local dev/mock mode without verified secret
    try {
      event = JSON.parse(body) as Stripe.Event;
      console.warn('Handling Stripe webhook in unverified mock/development mode.');
    } catch {
      return NextResponse.json({ error: 'Invalid JSON payload' }, { status: 400 });
    }
  }

  // Handle specific Stripe events
  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      console.log('✅ Stripe Checkout Session completed successfully:', {
        sessionId: session.id,
        customerEmail: session.customer_details?.email,
        amountTotal: session.amount_total ? session.amount_total / 100 : 0,
        currency: session.currency,
      });

      // Fulfillment: route to Printify service layer with full line item and personalization metadata
      try {
        const { printifyService } = await import('@/services/printify');
        
        let orderLineItems: Array<{
          productId: string;
          size?: string;
          color?: string;
          quantity: number;
          gamertag?: string;
          playerNumber?: string;
        }> = [];

        // If Stripe is live configured, fetch expanded line items
        if (!webhookSecret?.includes('placeholder')) {
          try {
            const lineItemsList = await stripe.checkout.sessions.listLineItems(session.id, {
              expand: ['data.price.product'],
            });

            orderLineItems = lineItemsList.data.map((item) => {
              const product = item.price?.product as Stripe.Product | undefined;
              return {
                productId: product?.metadata?.productId || 'krown-hoodie-premium',
                size: product?.metadata?.size || 'L',
                color: product?.metadata?.color || 'Standard',
                quantity: item.quantity || 1,
                gamertag: product?.metadata?.gamertag || undefined,
                playerNumber: product?.metadata?.player_number || undefined,
              };
            });
          } catch (err) {
            console.warn('Could not fetch Stripe line item details; falling back to session metadata:', err);
          }
        }

        // Fallback line items if none extracted
        if (orderLineItems.length === 0) {
          orderLineItems = [{
            productId: 'axiom-jersey-home',
            size: 'L',
            color: 'Obsidian Black',
            quantity: 1,
            gamertag: session.metadata?.custom_orders || undefined,
          }];
        }

        const shippingAddr = session.customer_details?.address || {
          city: 'Austin',
          country: 'US',
          line1: '100 Congress Ave',
          line2: null,
          postal_code: '78701',
          state: 'TX',
        };

        const printifyResult = await printifyService.createPrintifyOrder({
          externalId: session.id,
          shippingMethod: 1,
          addressTo: {
            first_name: session.customer_details?.name?.split(' ')[0] || 'Valued',
            last_name: session.customer_details?.name?.split(' ').slice(1).join(' ') || 'Customer',
            email: session.customer_details?.email || 'customer@krownsupply.com',
            country: shippingAddr.country || 'US',
            region: shippingAddr.state || 'TX',
            address1: shippingAddr.line1 || '100 Congress Ave',
            address2: shippingAddr.line2 || '',
            city: shippingAddr.city || 'Austin',
            zip: shippingAddr.postal_code || '78701',
          },
          lineItems: orderLineItems,
        });

        console.log(`[Order Fulfillment Routed] Printify Result:`, {
          orderId: printifyResult.orderId,
          isMock: printifyResult.isMock,
          externalId: session.id,
        });
      } catch (fulfillErr) {
        console.error('Error executing Printify fulfillment pipeline:', fulfillErr);
      }
      break;
    }

    case 'payment_intent.payment_failed': {
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      console.warn('❌ Payment failed for PaymentIntent:', paymentIntent.id);
      break;
    }

    default:
      console.log(`Unhandled Stripe event type: ${event.type}`);
  }

  return NextResponse.json({ received: true });
}
