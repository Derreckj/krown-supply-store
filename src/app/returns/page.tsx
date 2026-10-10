import React from 'react';
import Link from 'next/link';

export const metadata = {
  title: 'Returns & Replacement Policy | KrowN Supply Co.',
  description: 'Official made-to-order return and quality guarantee policy for KrowN Supply Co., KrowN Construction, and Axiom Gaming.',
};

export default function ReturnsPage() {
  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '3.5rem 1.5rem', color: 'var(--foreground)' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-gold)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          Customer Assurance // Quality Guarantee
        </span>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 900, marginTop: '0.5rem', marginBottom: '0.75rem', letterSpacing: '-0.02em' }}>
          Returns &amp; Replacement Policy
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', maxWidth: '640px', margin: '0 auto' }}>
          Our transparent, print-on-demand policy engineered to guarantee product perfection and fair protection.
        </p>
      </div>

      {/* Primary Policy Banner */}
      <div style={{ background: 'rgba(212, 175, 55, 0.08)', border: '1px solid rgba(212, 175, 55, 0.35)', borderRadius: '12px', padding: '2rem', marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--accent-gold)', marginBottom: '0.75rem' }}>
          👑 Custom Made-To-Order Policy Notice
        </h2>
        <p style={{ color: '#e5e7eb', fontSize: '0.98rem', lineHeight: 1.7, margin: 0 }}>
          Every garment, headwear piece, and esports battle accessory at KrowN Supply Co. is custom-printed, embroidered, and crafted strictly to order based on your exact color, size, and custom gamertag selection. As a result, <strong>all sales are final</strong>. We do not accept returns or exchanges for buyer&apos;s remorse, changes of mind, or incorrect size selection. Please reference our detailed <Link href="/size-guide" style={{ color: 'var(--accent-gold)', textDecoration: 'underline' }}>Official Size Guide</Link> before placing your order.
        </p>
      </div>

      {/* 100% Quality & Defect Guarantee */}
      <div style={{ background: 'rgba(57, 255, 20, 0.06)', border: '1px solid rgba(57, 255, 20, 0.3)', borderRadius: '12px', padding: '2rem', marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#39FF14', marginBottom: '0.75rem' }}>
          ⚡ 100% Defect &amp; Damage Protection Guarantee
        </h2>
        <p style={{ color: '#e5e7eb', fontSize: '0.98rem', lineHeight: 1.7, marginBottom: '1rem' }}>
          We hold our cut-and-sew manufacturing partners to the highest tournament standards. If your product arrives:
        </p>
        <ul style={{ paddingLeft: '1.25rem', color: '#d1d5db', lineHeight: 1.8, fontSize: '0.95rem', marginBottom: '1.25rem' }}>
          <li>Physically damaged during transit (torn fabric, shattered drinkware, dented rim)</li>
          <li>Manufactured with a printing flaw or embroidery defect</li>
          <li>Mismatched from the size, color, or gamertag submitted in your original order</li>
        </ul>
        <p style={{ color: '#e5e7eb', fontSize: '0.98rem', lineHeight: 1.7, margin: 0 }}>
          <strong>We will replace your item 100% free of charge or issue a full refund immediately.</strong> You do not need to ship the damaged item back to us.
        </p>
      </div>

      {/* How to Claim Replacement */}
      <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', padding: '2rem', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', marginBottom: '1rem' }}>
          How to Request a Replacement or Refund
        </h2>
        <ol style={{ paddingLeft: '1.25rem', color: '#9ca3af', lineHeight: 1.8, fontSize: '0.95rem', margin: 0 }}>
          <li>Notify our support team at <strong style={{ color: '#fff' }}>support@krownsupplyco.com</strong> within <strong>14 days of delivery</strong>.</li>
          <li>Include your Order Number and full name.</li>
          <li>Attach a clear photo or short video showing the damaged or misprinted area alongside the order packaging slip.</li>
          <li>Our quality team will review your ticket within 24 hours. Upon verification, an expedited reprint order will be dispatched to your address immediately with fresh tracking.</li>
        </ol>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
        <Link 
          href="/contact" 
          style={{ 
            background: 'var(--accent-gold)', 
            color: '#000', 
            fontWeight: 700, 
            padding: '0.75rem 1.75rem', 
            borderRadius: '6px', 
            textDecoration: 'none' 
          }}
        >
          Contact Support Team
        </Link>
        <Link 
          href="/size-guide" 
          style={{ 
            border: '1px solid rgba(255, 255, 255, 0.2)', 
            color: '#fff', 
            fontWeight: 600, 
            padding: '0.75rem 1.75rem', 
            borderRadius: '6px', 
            textDecoration: 'none' 
          }}
        >
          View Fit &amp; Size Guide
        </Link>
      </div>
    </div>
  );
}
