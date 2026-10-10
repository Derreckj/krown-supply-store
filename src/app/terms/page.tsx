import React from 'react';
import Link from 'next/link';

export const metadata = {
  title: 'Terms of Service | KrowN Supply Co.',
  description: 'Official terms of service for purchases, custom gamertag orders, and intellectual property on KrowN Supply Co.',
};

export default function TermsPage() {
  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '3.5rem 1.5rem', color: 'var(--foreground)' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-gold)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          Legal // Agreement
        </span>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 900, marginTop: '0.5rem', marginBottom: '0.75rem', letterSpacing: '-0.02em' }}>
          Terms of Service
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
          Last Updated: October 2026 • Effective Immediately
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', color: '#d1d5db', lineHeight: 1.75, fontSize: '0.95rem' }}>
        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>1. Agreement to Terms</h2>
          <p>
            By accessing or purchasing from krownsupplyco.com (&ldquo;KrowN Supply Co.&rdquo;), you agree to be bound by these Terms of Service. If you disagree with any portion of these terms, you must discontinue use of the site.
          </p>
        </section>

        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>2. Custom Orders &amp; Personalization</h2>
          <p>
            For items incorporating custom personalization (including gamertags, squad numbers, and custom uploaded artwork for B2B hat orders):
          </p>
          <ul style={{ paddingLeft: '1.25rem', marginTop: '0.5rem' }}>
            <li>You warrant that you own or possess legal rights to any submitted logos, trade names, or copyrighted assets.</li>
            <li>We reserve the right to decline text or imagery containing hate speech, illegal content, or unlawful infringement.</li>
            <li>Because custom goods cannot be re-stocked, sales are final once production begins, as governed by our <Link href="/returns" style={{ color: 'var(--accent-gold)', textDecoration: 'underline' }}>Returns Policy</Link>.</li>
          </ul>
        </section>

        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>3. Pricing &amp; Availability</h2>
          <p>
            All prices are listed in USD. While we make every effort to display accurate pricing, errors may occasionally occur. If a pricing error is discovered after order placement, we reserve the right to cancel the order and provide a full refund.
          </p>
        </section>

        <section style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '10px', padding: '1.75rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem' }}>4. Intellectual Property</h2>
          <p>
            All original graphics, brand names, slogans (&ldquo;WEAR THE KROWN&rdquo;, &ldquo;BUILT TO REIGN&rdquo;, &ldquo;PLAY TO REIGN&rdquo;), Axiom Allegiance owl mascots, and website code are the exclusive intellectual property of KrowN Supply Co. and its subsidiaries. Unauthorized reproduction or scraping is strictly prohibited.
          </p>
        </section>
      </div>

      <div style={{ textAlign: 'center', marginTop: '3rem' }}>
        <Link href="/privacy-policy" style={{ color: 'var(--accent-gold)', textDecoration: 'underline', fontSize: '0.95rem' }}>
          View Privacy Policy &rarr;
        </Link>
      </div>
    </div>
  );
}
