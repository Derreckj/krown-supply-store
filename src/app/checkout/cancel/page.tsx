import React from 'react';
import Link from 'next/link';
import '@/app/checkout/success/SuccessPage.css';

export default function CheckoutCancelPage() {
  return (
    <div className="checkout-status-page container">
      <div className="status-card" style={{ borderTopColor: 'var(--text-muted)' }}>
        <div className="status-icon">🛡️</div>
        <span className="brand-badge">KrowN Supply Co.</span>
        <h1>Checkout Incomplete</h1>
        <p className="status-tagline" style={{ color: 'var(--text-muted)' }}>YOUR CART IS PRESERVED</p>

        <p className="status-description">
          No charges were processed. Your items remain saved in your cart so you can resume whenever you are ready.
        </p>

        <div className="action-buttons">
          <Link href="/cart" className="btn-primary">
            Return to Cart
          </Link>
          <Link href="/collections/all" className="btn-secondary">
            Continue Browsing
          </Link>
        </div>
      </div>
    </div>
  );
}
