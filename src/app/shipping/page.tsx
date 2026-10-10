import React from 'react';
import Link from 'next/link';

export const metadata = {
  title: 'Shipping Policy & Delivery Estimates | KrowN Supply Co.',
  description: 'Learn about our custom made-to-order production times, USPS/carrier transit estimates, packaging standards, and tracking.',
};

export default function ShippingPage() {
  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '3.5rem 1.5rem', color: 'var(--foreground)' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-gold)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          Fulfillment // Logistics
        </span>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 900, marginTop: '0.5rem', marginBottom: '0.75rem', letterSpacing: '-0.02em' }}>
          Shipping Policy &amp; Delivery
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', maxWidth: '640px', margin: '0 auto' }}>
          Every piece is crafted on-demand and shipped directly from our certified production partners.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '1.75rem' }}>
          <div style={{ fontSize: '1.8rem', marginBottom: '0.75rem' }}>⚡</div>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f3f4f6', marginBottom: '0.5rem' }}>1. Custom Production</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', lineHeight: 1.6, margin: 0 }}>
            Because our apparel, jerseys, and headwear are made-to-order with custom embroidery, sublimation, and laser etching, production takes <strong>2 to 4 business days</strong> before dispatch.
          </p>
        </div>

        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '1.75rem' }}>
          <div style={{ fontSize: '1.8rem', marginBottom: '0.75rem' }}>📦</div>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f3f4f6', marginBottom: '0.5rem' }}>2. Transit Time</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', lineHeight: 1.6, margin: 0 }}>
            Standard US domestic delivery via USPS Priority or ground carriers typically takes <strong>3 to 5 business days</strong> once dispatched. Total turnaround is typically 5 to 9 business days.
          </p>
        </div>

        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '1.75rem' }}>
          <div style={{ fontSize: '1.8rem', marginBottom: '0.75rem' }}>🛡️</div>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f3f4f6', marginBottom: '0.5rem' }}>3. Tracked Delivery</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', lineHeight: 1.6, margin: 0 }}>
            Every parcel includes full 24/7 online tracking. You will receive an automated dispatch notification with your carrier tracking number as soon as the label is generated.
          </p>
        </div>
      </div>

      <div style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '2rem', marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#fff', marginBottom: '1rem' }}>
          Shipping Rates &amp; Destinations
        </h2>
        <ul style={{ paddingLeft: '1.25rem', color: '#9ca3af', lineHeight: 1.8, fontSize: '0.95rem' }}>
          <li><strong>Domestic US Shipping:</strong> Flat rate standard shipping calculated live at checkout based on weight and destination. Orders over $150 qualify for promotional free standard shipping.</li>
          <li><strong>Split Shipments:</strong> Orders containing multiple product categories (e.g. Richardson 112 leather patch hats crafted in one facility, and sublimated esports jerseys cut in another) may ship in separate protective packages at no extra charge to ensure optimal fulfillment speed.</li>
          <li><strong>Address Verification:</strong> Please double-check your shipping address prior to checkout. Because production is automated, address alterations cannot be guaranteed once fulfillment commences.</li>
        </ul>
      </div>

      <div style={{ textAlign: 'center' }}>
        <Link href="/collections/all" style={{ color: 'var(--accent-gold)', textDecoration: 'underline', fontSize: '0.95rem' }}>
          &larr; Back to Shop All Products
        </Link>
      </div>
    </div>
  );
}
