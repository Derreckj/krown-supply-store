/**
 * KrowN Supply Co. - Transactional & Customer Email Templates
 *
 * Fully responsive, luxury-styled HTML email templates featuring the
 * definitive brand identity and logo assets.
 */

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://krown-supply-store.vercel.app';
const LOGO_URL = `${SITE_URL}/images/branding/krown-definitive-logo.png`;

export interface EmailOrderDetails {
  orderId: string;
  customerName: string;
  items: Array<{
    name: string;
    variant: string;
    quantity: number;
    price: number;
    gamertag?: string;
  }>;
  totalAmount: number;
  shippingAddress: string;
}

export interface EmailShippingDetails {
  orderId: string;
  customerName: string;
  carrier: string;
  trackingNumber: string;
  trackingUrl: string;
}

export function generateOrderConfirmationEmail(order: EmailOrderDetails): string {
  const itemsHtml = order.items
    .map(
      (item) => `
    <tr>
      <td style="padding: 12px 0; border-bottom: 1px solid #222; color: #fff;">
        <strong>${item.name}</strong><br />
        <span style="color: #999; font-size: 13px;">${item.variant}</span>
        ${item.gamertag ? `<br /><span style="color: #D4AF37; font-size: 12px;">Tag: ${item.gamertag}</span>` : ''}
      </td>
      <td style="padding: 12px 0; border-bottom: 1px solid #222; text-align: center; color: #bbb;">
        ${item.quantity}
      </td>
      <td style="padding: 12px 0; border-bottom: 1px solid #222; text-align: right; color: #D4AF37; font-weight: 600;">
        $${(item.price * item.quantity).toFixed(2)}
      </td>
    </tr>`
    )
    .join('');

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Order Confirmation - KrowN Supply Co.</title>
  <style>
    body { margin: 0; padding: 0; background-color: #0b0b0c; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e5e5e5; }
    .container { max-width: 600px; margin: 40px auto; background: #121214; border: 1px solid #222; border-radius: 12px; overflow: hidden; }
    .header { padding: 32px; text-align: center; background: #000; border-bottom: 1px solid #222; }
    .logo { width: 90px; height: 90px; border-radius: 16px; margin-bottom: 16px; }
    .title { color: #fff; font-size: 24px; font-weight: 700; margin: 0 0 8px 0; }
    .slogan { color: #D4AF37; font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin: 0; }
    .body { padding: 32px; }
    .badge { display: inline-block; background: #1a1915; border: 1px solid #D4AF37; color: #D4AF37; padding: 6px 14px; border-radius: 999px; font-size: 12px; font-weight: 600; margin-bottom: 20px; }
    .table { width: 100%; border-collapse: collapse; margin-top: 16px; }
    .btn { display: inline-block; background: #D4AF37; color: #000; text-decoration: none; padding: 14px 28px; font-weight: 700; border-radius: 8px; margin-top: 24px; text-align: center; }
    .footer { padding: 24px 32px; text-align: center; font-size: 12px; color: #666; border-top: 1px solid #1a1a1a; background: #0c0c0d; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="${LOGO_URL}" alt="KrowN Supply Co." class="logo" />
      <h1 class="title">ORDER CONFIRMED</h1>
      <p class="slogan">WEAR THE KROWN.</p>
    </div>
    <div class="body">
      <span class="badge">ORDER REFERENCE: ${order.orderId}</span>
      <p>Salute, <strong>${order.customerName}</strong>,</p>
      <p style="color: #aaa; line-height: 1.6;">
        Your order has entered our automated production pipeline. Each garment and accessory is produced with precision craftsmanship and rigorously inspected before dispatch.
      </p>

      <table class="table">
        <thead>
          <tr style="border-bottom: 2px solid #2a2a2a; color: #888; font-size: 12px; text-transform: uppercase;">
            <th style="text-align: left; padding-bottom: 8px;">Item</th>
            <th style="text-align: center; padding-bottom: 8px;">Qty</th>
            <th style="text-align: right; padding-bottom: 8px;">Price</th>
          </tr>
        </thead>
        <tbody>
          ${itemsHtml}
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2" style="padding-top: 16px; text-align: right; font-weight: 700; color: #fff;">TOTAL:</td>
            <td style="padding-top: 16px; text-align: right; font-weight: 700; color: #D4AF37; font-size: 18px;">$${order.totalAmount.toFixed(2)}</td>
          </tr>
        </tfoot>
      </table>

      <div style="margin-top: 24px; padding: 16px; background: #161619; border-radius: 8px; font-size: 13px; color: #999;">
        <strong>Shipping Destination:</strong><br />
        ${order.shippingAddress}
      </div>

      <center>
        <a href="${SITE_URL}/orders/${order.orderId}" class="btn">VIEW ORDER STATUS</a>
      </center>
    </div>
    <div class="footer">
      &copy; 2026 KrowN Supply Co. All rights reserved.<br />
      Austin, TX • Streetwear • Workwear • Esports
    </div>
  </div>
</body>
</html>`;
}

export function generateShippingNotificationEmail(shipping: EmailShippingDetails): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Your Order Has Shipped - KrowN Supply Co.</title>
  <style>
    body { margin: 0; padding: 0; background-color: #0b0b0c; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e5e5e5; }
    .container { max-width: 600px; margin: 40px auto; background: #121214; border: 1px solid #222; border-radius: 12px; overflow: hidden; }
    .header { padding: 32px; text-align: center; background: #000; border-bottom: 1px solid #222; }
    .logo { width: 90px; height: 90px; border-radius: 16px; margin-bottom: 16px; }
    .title { color: #fff; font-size: 24px; font-weight: 700; margin: 0 0 8px 0; }
    .slogan { color: #D4AF37; font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin: 0; }
    .body { padding: 32px; }
    .btn { display: inline-block; background: #D4AF37; color: #000; text-decoration: none; padding: 14px 28px; font-weight: 700; border-radius: 8px; margin-top: 24px; text-align: center; }
    .footer { padding: 24px 32px; text-align: center; font-size: 12px; color: #666; border-top: 1px solid #1a1a1a; background: #0c0c0d; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="${LOGO_URL}" alt="KrowN Supply Co." class="logo" />
      <h1 class="title">YOUR ORDER HAS SHIPPED</h1>
      <p class="slogan">WEAR THE KROWN.</p>
    </div>
    <div class="body">
      <p>Salute, <strong>${shipping.customerName}</strong>,</p>
      <p style="color: #aaa; line-height: 1.6;">
        Your custom order (<strong>#${shipping.orderId}</strong>) has completed production inspection and has been dispatched via <strong>${shipping.carrier}</strong>.
      </p>

      <div style="background: #18181c; border-left: 4px solid #D4AF37; padding: 16px; border-radius: 6px; margin: 24px 0;">
        <span style="color: #888; font-size: 12px; text-transform: uppercase;">Tracking Number</span><br />
        <span style="font-family: monospace; font-size: 16px; color: #fff; font-weight: 700;">${shipping.trackingNumber}</span>
      </div>

      <center>
        <a href="${shipping.trackingUrl}" class="btn">TRACK YOUR SHIPMENT</a>
      </center>
    </div>
    <div class="footer">
      &copy; 2026 KrowN Supply Co. All rights reserved.<br />
      Austin, TX • Streetwear • Workwear • Esports
    </div>
  </div>
</body>
</html>`;
}

export function generatePasswordResetEmail(name: string, resetUrl: string): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Security Notice - KrowN Supply Co.</title>
  <style>
    body { margin: 0; padding: 0; background-color: #0b0b0c; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e5e5e5; }
    .container { max-width: 600px; margin: 40px auto; background: #121214; border: 1px solid #222; border-radius: 12px; overflow: hidden; }
    .header { padding: 32px; text-align: center; background: #000; border-bottom: 1px solid #222; }
    .logo { width: 90px; height: 90px; border-radius: 16px; margin-bottom: 16px; }
    .title { color: #fff; font-size: 24px; font-weight: 700; margin: 0 0 8px 0; }
    .slogan { color: #D4AF37; font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin: 0; }
    .body { padding: 32px; }
    .btn { display: inline-block; background: #D4AF37; color: #000; text-decoration: none; padding: 14px 28px; font-weight: 700; border-radius: 8px; margin-top: 24px; text-align: center; }
    .footer { padding: 24px 32px; text-align: center; font-size: 12px; color: #666; border-top: 1px solid #1a1a1a; background: #0c0c0d; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="${LOGO_URL}" alt="KrowN Supply Co." class="logo" />
      <h1 class="title">ACCOUNT SECURITY</h1>
      <p class="slogan">WEAR THE KROWN.</p>
    </div>
    <div class="body">
      <p>Salute, <strong>${name}</strong>,</p>
      <p style="color: #aaa; line-height: 1.6;">
        A request was received to reset the credentials for your KrowN Supply Co. account. Click the button below to establish a new password. This link expires in 60 minutes.
      </p>

      <center>
        <a href="${resetUrl}" class="btn">RESET CREDENTIALS</a>
      </center>

      <p style="color: #666; font-size: 12px; margin-top: 32px;">
        If you did not request this change, you can safely disregard this email.
      </p>
    </div>
    <div class="footer">
      &copy; 2026 KrowN Supply Co. All rights reserved.<br />
      Austin, TX • Streetwear • Workwear • Esports
    </div>
  </div>
</body>
</html>`;
}
