"use client";

import React from 'react';
import Link from 'next/link';
import { useCart } from '@/context/CartContext';
import './Navbar.css';

export default function Navbar() {
  const { cartCount, setIsCartOpen } = useCart();

  return (
    <header className="navbar">
      <div className="navbar-container container">
        <Link href="/" className="navbar-brand">
          <img 
            src="/images/branding/krown-definitive-logo.png" 
            alt="KrowN Supply Co." 
            className="navbar-logo-icon" 
            style={{ borderRadius: '8px', objectFit: 'contain' }}
          />
          <span>KrowN <span className="text-gold">Supply Co.</span></span>
        </Link>
        <nav className="navbar-links">
          <Link href="/collections/all">The Vault // All</Link>
          <Link href="/collections/supply">KrowN Supply Co.</Link>
          <Link href="/collections/gaming">AXA Esports // Gaming</Link>
          <Link href="/collections/construction">KrowN Construction</Link>
          <Link href="/custom-crew" style={{ color: 'var(--accent-gold)', fontWeight: 700 }}>Custom Hats ★</Link>
        </nav>
        <div className="navbar-actions">
          <Link href="/search" aria-label="Search Catalog">
            <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </Link>
          <button 
            className="navbar-cart-link" 
            aria-label={`View Cart (${cartCount} items)`}
            onClick={() => setIsCartOpen(true)}
            style={{ cursor: 'pointer', background: 'none', border: 'none', color: 'inherit', padding: 0 }}
          >
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            {cartCount > 0 && (
              <span className="navbar-cart-badge">{cartCount}</span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
