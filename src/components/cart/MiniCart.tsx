"use client";

import React from 'react';
import Link from 'next/link';
import { useCart } from '@/context/CartContext';
import './MiniCart.css';

export default function MiniCart() {
  const { items, isCartOpen, setIsCartOpen, cartTotal, removeItem, updateQuantity } = useCart();

  if (!isCartOpen) return null;

  return (
    <>
      <div className="mini-cart-overlay" onClick={() => setIsCartOpen(false)} />
      <div className="mini-cart-drawer">
        <div className="mini-cart-header">
          <h2>Your Cart</h2>
          <button className="mini-cart-close" onClick={() => setIsCartOpen(false)}>&times;</button>
        </div>

        <div className="mini-cart-content">
          {items.length === 0 ? (
            <div className="mini-cart-empty">
              <p>Your cart is empty.</p>
              <button className="btn-primary" onClick={() => setIsCartOpen(false)}>Continue Shopping</button>
            </div>
          ) : (
            <div className="mini-cart-items">
              {items.map((item) => (
                <div key={item.id} className="mini-cart-item">
                  <div className="mini-cart-item-img-wrap">
                    <img src={item.image} alt={item.name} className="mini-cart-item-img" />
                  </div>
                  <div className="mini-cart-item-details">
                    <h4>{item.name}</h4>
                    <p className="mini-cart-item-variant">{item.variant.color} / {item.variant.size}</p>
                    {item.personalization && (item.personalization.gamertag || item.personalization.playerNumber) && (
                      <p className="mini-cart-item-custom" style={{
                        fontSize: '0.75rem',
                        color: '#39FF14',
                        marginTop: '0.25rem',
                        fontWeight: 600,
                        letterSpacing: '0.04em'
                      }}>
                        ⚡ Custom Tag: {item.personalization.gamertag || 'NONE'}{item.personalization.playerNumber ? ` | No. #${item.personalization.playerNumber}` : ''}
                      </p>
                    )}
                    <div className="mini-cart-item-actions">
                      <div className="mini-cart-qty">
                        <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
                        <span>{item.quantity}</span>
                        <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                      </div>
                      <span className="mini-cart-item-price">${(item.price * item.quantity).toFixed(2)}</span>
                    </div>
                    <button className="mini-cart-item-remove" onClick={() => removeItem(item.id)}>Remove</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {items.length > 0 && (
          <div className="mini-cart-footer">
            <div className="mini-cart-timeline" style={{
              background: 'rgba(212, 175, 55, 0.08)',
              border: '1px solid rgba(212, 175, 55, 0.25)',
              borderRadius: '6px',
              padding: '0.5rem 0.75rem',
              marginBottom: '0.75rem',
              fontSize: '0.75rem',
              color: 'var(--accent-gold)',
              lineHeight: '1.4'
            }}>
              ⚡ Custom items made-to-order: 3–5 business days production
            </div>
            <div className="mini-cart-subtotal">
              <span>Subtotal</span>
              <span>${cartTotal.toFixed(2)}</span>
            </div>
            <p className="mini-cart-taxes">Taxes and shipping calculated at checkout.</p>
            <Link href="/cart" className="btn-primary mini-cart-checkout" onClick={() => setIsCartOpen(false)}>
              Checkout &rarr;
            </Link>
          </div>
        )}
      </div>
    </>
  );
}
