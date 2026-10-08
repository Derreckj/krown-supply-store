import React from 'react';
import Link from 'next/link';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-grid">
        <div className="footer-brand">
          <h2>KrowN Supply Co.</h2>
          <p className="text-muted mt-2">WEAR THE KROWN.</p>
        </div>
        <div className="footer-links">
          <h3>Shop</h3>
          <ul>
            <li><Link href="/collections/supply">KrowN Supply Co.</Link></li>
            <li><Link href="/collections/gaming">AXA Esports // Gaming</Link></li>
            <li><Link href="/collections/construction">KrowN Construction LLC</Link></li>
            <li><Link href="/collections/accessories">Accessories & Decals</Link></li>
            <li><Link href="/custom-crew" style={{ color: 'var(--accent-gold)' }}>Custom Hats (B2B)</Link></li>
          </ul>
        </div>
        <div className="footer-links">
          <h3>Support</h3>
          <ul>
            <li><Link href="/faq">FAQ</Link></li>
            <li><Link href="/shipping">Shipping</Link></li>
            <li><Link href="/returns">Returns & Exchanges</Link></li>
            <li><Link href="/contact">Contact</Link></li>
            <li><Link href="/size-guide">Size Guide</Link></li>
          </ul>
        </div>
        <div className="footer-links">
          <h3>Legal</h3>
          <ul>
            <li><Link href="/privacy-policy">Privacy Policy</Link></li>
            <li><Link href="/terms">Terms of Service</Link></li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom container">
        <p className="text-muted">&copy; 2026 KrowN Supply Co. All rights reserved.</p>
      </div>
    </footer>
  );
}
