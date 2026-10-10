import React from 'react';
import Link from 'next/link';

export const metadata = {
  title: 'Frequently Asked Questions (FAQ) | KrowN Supply Co.',
  description: 'Find answers regarding custom esports gamertags, luxury streetwear sizing, made-to-order production timelines, and order tracking.',
};

export default function FAQPage() {
  const faqs = [
    {
      q: 'How does custom personalization work for jerseys and apparel?',
      a: 'When customizing our Pro League Cut-and-Sew Sublimated Jerseys or Official Crewnecks, enter your exact gamertag, select your preferred casing style (Exact Case or ALL CAPS), squad number (00–99), and desired sleeve / crest placements before adding to cart. Your customizations are permanently infused into the fabric using tournament-grade sublimation and high-density embroidery.',
    },
    {
      q: 'What are your production and fulfillment timelines?',
      a: 'Every piece at KrowN Supply Co., KrowN Construction, and AXA Axiom Allegiance is custom-engineered and made-to-order to eliminate dead inventory and deliver pristine, unworn quality. Standard production takes 2 to 4 business days. Once crafted and quality-inspected, orders ship with tracking and typically arrive within 3 to 5 business days in the US.',
    },
    {
      q: 'How do I know what size to choose?',
      a: 'We provide comprehensive, product-specific measurement guides with exact dimensions for every sized product across our catalog (chest width laid flat, body length, sleeve length, waist circumference, and compression bicep girth). You can view the full guide at our Size Guide page or click "Size Guide" on any product page.',
    },
    {
      q: 'What is your return and exchange policy?',
      a: 'Because every item is custom printed, cut, and sewn to order specifically for you, all sales are final and we cannot accept returns or exchanges for buyer\'s remorse or incorrect size selection. However, if your order arrives damaged, defective, or with a manufacturing misprint, we guarantee a 100% free reprint replacement or full refund upon photo verification within 14 days of delivery.',
    },
    {
      q: 'Are KrowN Construction garments built for real jobsites?',
      a: 'Yes. Our KrowN Construction line features heavy 380–480 GSM French terry cotton, triple-needle reinforced stress points, high-visibility contrast accents, industrial brass hardware, and laser-etched genuine leather patches designed to withstand tough jobsite conditions.',
    },
    {
      q: 'How do I care for and wash my garments?',
      a: 'To maintain the vibrancy of sublimated graphics, embroidery, and heavy French terry fleece: machine wash cold inside out with like colors using mild detergent. Tumble dry on low or hang dry for maximum lifespan. Never iron directly over prints, embroidery, or leather patches.',
    },
    {
      q: 'How can I track my shipment?',
      a: 'As soon as your order completes production and leaves our facility, an automated shipping confirmation email containing your direct USPS/carrier tracking number will be sent to your email address.',
    },
  ];

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '3.5rem 1.5rem', color: 'var(--foreground)' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-gold)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          Customer Support // Knowledge Base
        </span>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 900, marginTop: '0.5rem', marginBottom: '0.75rem', letterSpacing: '-0.02em' }}>
          Frequently Asked Questions
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', maxWidth: '640px', margin: '0 auto' }}>
          Everything you need to know about custom gamertag orders, jobsite gear specs, production timelines, and care.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {faqs.map((faq, i) => (
          <div 
            key={i} 
            style={{ 
              background: 'rgba(255, 255, 255, 0.03)', 
              border: '1px solid rgba(255, 255, 255, 0.08)', 
              borderRadius: '10px', 
              padding: '1.5rem',
              transition: 'border-color 0.2s ease'
            }}
          >
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#f3f4f6', marginBottom: '0.65rem' }}>
              {faq.q}
            </h2>
            <p style={{ fontSize: '0.95rem', color: '#9ca3af', lineHeight: 1.6, margin: 0 }}>
              {faq.a}
            </p>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '3.5rem', padding: '2rem', background: 'rgba(212, 175, 55, 0.06)', border: '1px solid rgba(212, 175, 55, 0.25)', borderRadius: '12px', textAlign: 'center' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--accent-gold)', marginBottom: '0.5rem' }}>
          Still have questions?
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginBottom: '1.25rem' }}>
          Our support team is ready to assist you with order status, sizing inquiries, or B2B volume pricing.
        </p>
        <Link 
          href="/contact" 
          style={{ 
            display: 'inline-block', 
            background: 'var(--accent-gold)', 
            color: '#000', 
            fontWeight: 700, 
            padding: '0.75rem 1.75rem', 
            borderRadius: '6px', 
            textDecoration: 'none' 
          }}
        >
          Contact Support &rarr;
        </Link>
      </div>
    </div>
  );
}
