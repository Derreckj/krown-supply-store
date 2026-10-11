"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useCart } from '@/context/CartContext';
import { validateDiscountCode, DiscountCodeConfig } from '@/lib/discounts';
import './CartPage.css';

export default function CartPage() {
  const { items, removeItem, updateQuantity, cartTotal } = useCart();
  const [isCheckingOut, setIsCheckingOut] = useState(false);
  const [checkoutError, setCheckoutError] = useState<string | null>(null);

  // Friends & Family Discount Code State
  const [discountInput, setDiscountInput] = useState('');
  const [appliedDiscount, setAppliedDiscount] = useState<DiscountCodeConfig | null>(null);
  const [discountError, setDiscountError] = useState<string | null>(null);

  const discountAmount = appliedDiscount ? (cartTotal * appliedDiscount.percentage) / 100 : 0;
  const finalTotal = Math.max(0, cartTotal - discountAmount);

  const handleApplyDiscount = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const trimmed = discountInput.trim();
    if (!trimmed) return;

    const validated = validateDiscountCode(trimmed);
    if (validated) {
      setAppliedDiscount(validated);
      setDiscountError(null);
    } else {
      setDiscountError('Invalid code. Please enter a valid Friends & Family discount code (e.g. KROWN10 or KROWN15).');
    }
  };

  const handleRemoveDiscount = () => {
    setAppliedDiscount(null);
    setDiscountInput('');
    setDiscountError(null);
  };

  const handleCheckout = async () => {
    try {
      setIsCheckingOut(true);
      setCheckoutError(null);

      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          items,
          discountCode: appliedDiscount?.code,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.url) {
        throw new Error(data.error || 'Failed to initialize checkout session.');
      }

      // Redirect to Stripe Checkout (or mock checkout in development)
      window.location.href = data.url;
    } catch (err) {
      console.error('Checkout error:', err);
      setCheckoutError(err instanceof Error ? err.message : 'Something went wrong. Please try again.');
      setIsCheckingOut(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="cart-page container cart-empty">
        <h1>Your Cart is Empty</h1>
        <p className="text-muted">Looks like you haven&apos;t added anything yet.</p>
        <Link href="/collections/all" className="btn-primary" style={{ marginTop: '2rem' }}>
          Continue Shopping
        </Link>
      </div>
    );
  }

  const freeShippingThreshold = 75;
  const shippingProgress = Math.min(100, (cartTotal / freeShippingThreshold) * 100);
  const amountToFreeShipping = Math.max(0, freeShippingThreshold - cartTotal);

  return (
    <div className="cart-page container">
      <h1>Your Cart</h1>

      {/* Free Shipping Progress Bar */}
      <div className="shipping-progress-banner">
        <p className="shipping-progress-text">
          {cartTotal >= freeShippingThreshold ? (
            <span>🎉 <strong>Congratulations!</strong> You unlocked <strong>FREE Standard US Shipping</strong>.</span>
          ) : (
            <span>Add <strong>${amountToFreeShipping.toFixed(2)}</strong> more to unlock <strong>FREE US Shipping</strong>!</span>
          )}
        </p>
        <div className="shipping-progress-bar">
          <div className="shipping-progress-fill" style={{ width: `${shippingProgress}%` }} />
        </div>
      </div>
      
      <div className="cart-layout">
        <div className="cart-items">
          <div className="cart-header desktop-only">
            <span>Product</span>
            <span>Quantity</span>
            <span>Total</span>
          </div>
          
          {items.map((item) => (
            <div key={item.id} className="cart-item">
              <div className="cart-item-product">
                <div className="cart-item-image">
                  {item.image ? (
                    <img src={item.image} alt={item.name} className="cart-product-img" />
                  ) : (
                    <div className="placeholder-img" />
                  )}
                </div>
                <div className="cart-item-details">
                  <h3><Link href={`/products/${item.productId}`}>{item.name}</Link></h3>
                  <p className="cart-item-variant">
                    {item.variant.color} / {item.variant.size}
                  </p>
                  {item.personalization && (item.personalization.gamertag || item.personalization.playerNumber || item.personalization.notes) && (
                    <div style={{
                      fontSize: '0.75rem',
                      color: '#39FF14',
                      background: 'rgba(57, 255, 20, 0.08)',
                      border: '1px solid rgba(57, 255, 20, 0.25)',
                      borderRadius: '4px',
                      padding: '0.3rem 0.6rem',
                      marginTop: '0.35rem',
                      display: 'inline-block',
                      fontWeight: 600,
                      letterSpacing: '0.04em'
                    }}>
                      {item.personalization.gamertag && (
                        <div>⚡ Tag: {item.personalization.gamertag}{item.personalization.playerNumber ? ` | #${item.personalization.playerNumber}` : ''}</div>
                      )}
                      {item.personalization.notes && (
                        <div style={{ fontSize: '0.7rem', color: '#D4AF37', marginTop: '0.15rem' }}>
                          {item.personalization.notes}
                        </div>
                      )}
                    </div>
                  )}
                  <p className="cart-item-price mobile-only">${item.price.toFixed(2)}</p>
                  <button 
                    type="button" 
                    className="cart-item-remove"
                    onClick={() => removeItem(item.id)}
                  >
                    Remove
                  </button>
                </div>
              </div>
              
              <div className="cart-item-quantity">
                <div className="quantity-controls">
                  <button 
                    type="button" 
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    disabled={item.quantity <= 1}
                  >-</button>
                  <input 
                    type="number" 
                    value={item.quantity} 
                    readOnly
                  />
                  <button 
                    type="button"
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  >+</button>
                </div>
              </div>
              
              <div className="cart-item-total desktop-only">
                ${(item.price * item.quantity).toFixed(2)}
              </div>
            </div>
          ))}
        </div>
        
        <div className="cart-summary">
          <h2>Order Summary</h2>
          <div className="summary-row">
            <span>Subtotal</span>
            <span>${cartTotal.toFixed(2)}</span>
          </div>

          {appliedDiscount && (
            <div className="summary-row discount-row">
              <span>Friends & Family Discount ({appliedDiscount.code} • {appliedDiscount.percentage}%)</span>
              <span>-${discountAmount.toFixed(2)}</span>
            </div>
          )}

          <div className="summary-row">
            <span>Estimated Shipping</span>
            <span className="text-muted">Calculated at Stripe Checkout</span>
          </div>
          <div className="summary-row summary-total">
            <span>Total</span>
            <span style={{ color: appliedDiscount ? 'var(--accent-gold)' : undefined }}>
              ${finalTotal.toFixed(2)}
            </span>
          </div>

          {/* Friends & Family Discount Code Section */}
          <div className="discount-box">
            <div className="discount-header">
              <span className="discount-title">🎁 Promo / Discount Code</span>
              {appliedDiscount && (
                <span style={{ fontSize: '0.72rem', color: '#39FF14', fontWeight: 700 }}>
                  {appliedDiscount.percentage}% OFF APPLIED
                </span>
              )}
            </div>

            {!appliedDiscount ? (
              <form onSubmit={handleApplyDiscount} className="discount-input-group">
                <input
                  type="text"
                  className="discount-input"
                  placeholder="Code (e.g. KROWN10, KROWN15)"
                  value={discountInput}
                  onChange={(e) => {
                    setDiscountInput(e.target.value);
                    if (discountError) setDiscountError(null);
                  }}
                  aria-label="Discount Code"
                />
                <button
                  type="submit"
                  className="discount-apply-btn"
                  disabled={!discountInput.trim()}
                >
                  Apply
                </button>
              </form>
            ) : (
              <div className="discount-applied-card">
                <div className="discount-applied-info">
                  <span className="discount-applied-code">✓ {appliedDiscount.code} APPLIED</span>
                  <span className="discount-applied-label">
                    {appliedDiscount.label} • Saving ${discountAmount.toFixed(2)}
                  </span>
                </div>
                <button
                  type="button"
                  className="discount-remove-btn"
                  onClick={handleRemoveDiscount}
                  aria-label="Remove discount code"
                >
                  Remove
                </button>
              </div>
            )}

            {discountError && (
              <div className="discount-error-text">
                ⚠️ {discountError}
              </div>
            )}
          </div>

          <div style={{
            background: 'rgba(212, 175, 55, 0.08)',
            border: '1px solid rgba(212, 175, 55, 0.25)',
            borderRadius: '6px',
            padding: '0.65rem 0.85rem',
            marginTop: '0.5rem',
            marginBottom: '1rem',
            fontSize: '0.8rem',
            color: 'var(--accent-gold)',
            lineHeight: '1.4'
          }}>
            ⚡ Custom items made-to-order: 3–5 business days production
          </div>

          {checkoutError && (
            <div style={{
              background: 'rgba(255, 85, 85, 0.1)',
              border: '1px solid rgba(255, 85, 85, 0.3)',
              borderRadius: '6px',
              padding: '0.65rem 0.85rem',
              marginBottom: '1rem',
              fontSize: '0.8rem',
              color: '#ff6b6b',
              lineHeight: '1.4'
            }}>
              ⚠️ {checkoutError}
            </div>
          )}

          <button 
            type="button"
            className="btn-primary checkout-btn"
            onClick={handleCheckout}
            disabled={isCheckingOut}
          >
            {isCheckingOut ? 'Preparing Secure Checkout...' : 'Proceed to Checkout'}
          </button>
          
          <div className="payment-icons">
            <span className="text-muted" style={{ fontSize: '0.75rem', textAlign: 'center', display: 'block', marginTop: '1rem' }}>
              🔒 Powered by Stripe • Encrypted 256-Bit SSL
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
