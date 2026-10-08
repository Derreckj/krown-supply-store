import { NextRequest, NextResponse } from 'next/server';
import { stripe, isStripeConfigured } from '@/lib/stripe';
import { CartItem } from '@/context/CartContext';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const { items } = (await req.json()) as { items: CartItem[] };

    if (!items || !Array.isArray(items) || items.length === 0) {
      return NextResponse.json(
        { error: 'Cart is empty or invalid.' },
        { status: 400 }
      );
    }

    const origin = req.headers.get('origin') || process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';

    // When Stripe live credentials are not yet populated, provide smooth mock checkout testing
    if (!isStripeConfigured()) {
      console.warn('STRIPE_SECRET_KEY is not configured or using placeholder. Redirecting to mock success.');
      const mockSessionId = `mock_krown_session_${Date.now()}`;
      return NextResponse.json({
        url: `${origin}/checkout/success?session_id=${mockSessionId}&mode=mock_sandbox`,
        isMock: true,
      });
    }

    // Prepare line items for Stripe Checkout Session with full personalization metadata
    const line_items = items.map((item) => {
      const descParts = [`${item.variant.color} - Size: ${item.variant.size}`];
      if (item.personalization?.gamertag) {
        descParts.push(`Gamertag: ${item.personalization.gamertag}`);
      }
      if (item.personalization?.playerNumber) {
        descParts.push(`No: #${item.personalization.playerNumber}`);
      }

      return {
        price_data: {
          currency: 'usd',
          product_data: {
            name: item.name,
            description: descParts.join(' | '),
            images: [
              item.image
                ? (item.image.startsWith('http') ? item.image : `${origin}${item.image}`)
                : `${origin}/images/branding/krown-definitive-logo.png`
            ],
            metadata: {
              productId: item.productId,
              color: item.variant.color,
              size: item.variant.size,
              gamertag: item.personalization?.gamertag || '',
              player_number: item.personalization?.playerNumber || '',
              edition: item.personalization?.edition || item.variant.color,
            },
          },
          unit_amount: Math.round(item.price * 100), // Stripe expects amounts in cents
        },
        quantity: item.quantity,
      };
    });

    const session = await stripe.checkout.sessions.create({
      line_items,
      mode: 'payment',
      shipping_address_collection: {
        allowed_countries: ['US', 'CA'],
      },
      billing_address_collection: 'required',
      success_url: `${origin}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${origin}/checkout/cancel`,
      metadata: {
        brand: 'KrowN Supply Co.',
        total_items: items.reduce((acc, it) => acc + it.quantity, 0).toString(),
        custom_orders: items
          .filter(i => i.personalization?.gamertag)
          .map(i => `${i.productId}:${i.personalization?.gamertag}#${i.personalization?.playerNumber || ''}`)
          .join(',')
          .slice(0, 500),
      },
    });

    return NextResponse.json({ url: session.url });
  } catch (error) {
    console.error('Stripe Checkout session creation error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Internal error creating checkout session.' },
      { status: 500 }
    );
  }
}
