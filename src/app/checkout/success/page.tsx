"use client";

import React, { useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { useCart } from '@/context/CartContext';
import './SuccessPage.css';

function SuccessContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const isMock = searchParams.get('mode') === 'mock_sandbox';
  const { clearCart } = useCart();

  useEffect(() => {
    // Clear cart once order is confirmed
    clearCart();
  }, [clearCart]);

  return (
    <div className="checkout-status-page container">
      <div className="status-card">
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
          <img 
            src="/images/branding/krown-definitive-logo.png" 
            alt="KrowN Supply Co." 
            style={{ width: '80px', height: '80px', borderRadius: '16px', objectFit: 'contain' }}
          />
        </div>
        <span className="brand-badge">KrowN Supply Co.</span>
        <h1>Order Confirmed</h1>
        <p className="status-tagline">WEAR THE KROWN.</p>

        <p className="status-description">
          Thank you for joining the Reign. Your order has been placed into our production queue.
          You will receive a confirmation email with live tracking as soon as fulfillment commences.
        </p>

        {sessionId && (
          <div className="reference-box">
            <span className="reference-label">Order Reference / Session:</span>
            <code className="reference-id">{sessionId}</code>
            {isMock && (
              <span className="mock-note">
                (Simulated Checkout Sandbox Mode — Ready for Live Stripe Credentials)
              </span>
            )}
          </div>
        )}

        <div className="next-steps-box">
          <h3>Fulfillment Workflow</h3>
          <ul>
            <li><strong>Automated Production:</strong> Routed to Printify certified print facilities.</li>
            <li><strong>Quality Inspection:</strong> Garments and embroidery inspected prior to dispatch.</li>
            <li><strong>Tracking Notification:</strong> Real-time carrier tracking dispatched directly to your inbox.</li>
          </ul>
        </div>

        <div className="action-buttons">
          <Link href="/collections/all" className="btn-primary">
            Continue Shopping
          </Link>
          <Link href="/" className="btn-secondary">
            Return Home
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function CheckoutSuccessPage() {
  return (
    <Suspense fallback={
      <div className="checkout-status-page container">
        <div className="status-card">
          <h1>Loading Order Confirmation...</h1>
        </div>
      </div>
    }>
      <SuccessContent />
    </Suspense>
  );
}
