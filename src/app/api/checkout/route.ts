import { NextRequest, NextResponse } from 'next/server';
import { stripe, isStripeConfigured } from '@/lib/stripe';
import { CartItem } from '@/context/CartContext';
import { validateDiscountCode } from '@/lib/discounts';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const { items, discountCode } = (await req.json()) as { items: CartItem[]; discountCode?: string };

    if (!items || !Array.isArray(items) || items.length === 0) {
      return NextResponse.json(
        { error: 'Cart is empty or invalid.' },
        { status: 400 }
      );
    }

    const discount = validateDiscountCode(discountCode);

    const origin = req.headers.get('origin') || process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';

    // When Stripe live credentials are not yet populated, provide smooth mock checkout testing
    if (!isStripeConfigured()) {
      console.warn('STRIPE_SECRET_KEY is not configured or using placeholder. Redirecting to mock success.');
      const mockSessionId = `mock_krown_session_${Date.now()}`;
      const discountQuery = discount ? `&discount_code=${encodeURIComponent(discount.code)}&discount_pct=${discount.percentage}` : '';
      return NextResponse.json({
        url: `${origin}/checkout/success?session_id=${mockSessionId}&mode=mock_sandbox${discountQuery}`,
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
      if (item.personalization?.notes) {
        descParts.push(`Upgrades: ${item.personalization.notes}`);
      }
      if (discount) {
        descParts.push(`Promo ${discount.code}: -${discount.percentage}% applied`);
      }

      const effectivePrice = discount ? item.price * (1 - discount.percentage / 100) : item.price;

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
              upgrades: item.personalization?.notes || '',
              original_price: item.price.toFixed(2),
              discount_code: discount?.code || '',
            },
          },
          unit_amount: Math.round(effectivePrice * 100), // Stripe expects amounts in cents
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
      allow_promotion_codes: !discount, // If discount is already applied at cart, don't double discount
      success_url: `${origin}/checkout/success?session_id={CHECKOUT_SESSION_ID}${discount ? `&discount_code=${encodeURIComponent(discount.code)}&discount_pct=${discount.percentage}` : ''}`,
      cancel_url: `${origin}/checkout/cancel`,
      metadata: {
        brand: 'KrowN Supply Co.',
        discount_code: discount?.code || 'NONE',
        discount_percentage: discount ? discount.percentage.toString() : '0',
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
