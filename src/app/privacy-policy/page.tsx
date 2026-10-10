import React from 'react';
import Link from 'next/link';

export const metadata = {
  title: 'Privacy Policy | KrowN Supply Co.',
  description: 'Official privacy policy for KrowN Supply Co. detailing secure checkout, data encryption, and cookie usage.',
};

export default function PrivacyPolicyPage() {
  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '3.5rem 1.5rem', color: 'var(--foreground)' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-gold)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          Legal // Data Protection
        </span>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 900, marginTop: '0.5rem', marginBottom: '0.75rem', letterSpacing: '-0.02em' }}>
          Privacy Policy
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
          Last Updated: October 2026 • Effective Immediately
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', color: '#d1d5db', lineHeight: 1.75, fontSize: '0.95rem' }}>
        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>1. Overview &amp; Scope</h2>
          <p>
            KrowN Supply Co. (&ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;) operates krownsupplyco.com and affiliated storefronts. We respect your personal privacy and are committed to protecting your sensitive information through transparent compliance with applicable United States consumer privacy standards.
          </p>
        </section>

        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>2. Information We Collect</h2>
          <p>When you visit or purchase from our website, we collect necessary transactional information including:</p>
          <ul style={{ paddingLeft: '1.25rem', marginTop: '0.5rem' }}>
            <li><strong>Order Information:</strong> Full name, billing address, shipping address, email, phone number, and custom order metadata (such as gamertag and jersey squad number).</li>
            <li><strong>Payment Information:</strong> All payment transactions are encrypted and processed through PCI-DSS Level 1 certified processors (Stripe). We never store or have access to your raw credit card numbers.</li>
            <li><strong>Device &amp; Usage Data:</strong> IP address, browser type, referring pages, and session cookies used to maintain your cart and secure authentication.</li>
          </ul>
        </section>

        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>3. How We Use Your Information</h2>
          <p>We use your information exclusively to:</p>
          <ul style={{ paddingLeft: '1.25rem', marginTop: '0.5rem' }}>
            <li>Fulfill and route your customized order to certified production and shipping carriers.</li>
            <li>Send order confirmations, proof validations, tracking updates, and support responses.</li>
            <li>Prevent fraudulent transactions and protect our storefront integrity.</li>
          </ul>
          <p style={{ marginTop: '0.75rem' }}><strong>We never sell, rent, or monetize your personal data to third-party data brokers under any circumstances.</strong></p>
        </section>

        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>4. Security &amp; Data Rights</h2>
          <p>
            Our website utilizes end-to-end SSL/TLS 256-bit encryption. You maintain the right to access, rectify, or request deletion of your personal account data at any time by contacting our privacy compliance team at <strong style={{ color: '#fff' }}>privacy@krownsupplyco.com</strong>.
          </p>
        </section>
      </div>

      <div style={{ textAlign: 'center', marginTop: '3rem' }}>
        <Link href="/terms" style={{ color: 'var(--accent-gold)', textDecoration: 'underline', fontSize: '0.95rem' }}>
          View Terms of Service &rarr;
        </Link>
      </div>
    </div>
  );
}
